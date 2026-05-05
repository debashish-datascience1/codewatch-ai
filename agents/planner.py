import json
import re

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq

from config.settings import GROQ_API_KEY, GROQ_MODEL
from graph.state import CodeAnalysisState

SYSTEM_PROMPT = """You are a senior security architect and code analyst with deep expertise in \
application security, OWASP Top 10, and CWE vulnerability taxonomy.

Your job is to perform the PLANNING phase of a multi-agent code security analysis pipeline.
Given a piece of source code you must:
  1. Detect the programming language precisely.
  2. Assess the overall security risk level based on patterns you can already see.
  3. Define the scope — which areas of the code need the closest scrutiny.
  4. Write a clear, step-by-step analysis plan that the downstream agents will follow.
  5. List the key vulnerability categories to check (reference OWASP / CWE where possible).

Respond ONLY with a single valid JSON object — no markdown, no explanation outside the JSON.
Use this exact schema:
{
  "language": "<detected language, e.g. Python>",
  "risk_level": "<CRITICAL | HIGH | MEDIUM | LOW>",
  "scope": "<one sentence describing what will be analysed>",
  "analysis_plan": "<numbered steps the scanner should follow>",
  "key_areas": ["<area 1>", "<area 2>", "..."]
}"""


def _extract_json(raw: str) -> dict:
    """
    Robustly extract a JSON object from an LLM response.
    Tries three strategies in order:
      1. Direct parse (LLM obeyed the instruction perfectly)
      2. Strip markdown fences then parse
      3. Find the first {...} block with regex
    """
    text = raw.strip()

    # Strategy 1: direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Strategy 2: strip ``` fences
    fenced = re.sub(r"```(?:json)?\s*", "", text, flags=re.IGNORECASE).strip()
    try:
        return json.loads(fenced)
    except json.JSONDecodeError:
        pass

    # Strategy 3: pull the first {...} block from anywhere in the response
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        return json.loads(match.group())

    raise ValueError(f"No valid JSON found in LLM response:\n{raw[:500]}")


def planner_node(state: CodeAnalysisState) -> dict:
    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model=GROQ_MODEL,
        temperature=0,
        model_kwargs={"response_format": {"type": "json_object"}},
    )

    code_preview = state["raw_code"][:4000]

    human_prompt = (
        f"File: {state.get('filename', 'unknown')}\n\n"
        f"```\n{code_preview}\n```\n\n"
        "Return ONLY the JSON object described in the system prompt. No extra text."
    )

    response = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=human_prompt),
    ])

    try:
        plan = _extract_json(response.content)
    except (json.JSONDecodeError, ValueError) as exc:
        print(f"[planner] JSON parse failed: {exc}")
        plan = {
            "language": "unknown",
            "risk_level": "MEDIUM",
            "scope": "Full code review",
            "analysis_plan": "1. Review all code for common vulnerability patterns.",
            "key_areas": ["Injection", "Authentication", "Data Exposure"],
        }

    # Normalize analysis_plan — LLM sometimes returns a list instead of a string
    raw_plan = plan.get("analysis_plan", "")
    if isinstance(raw_plan, list):
        steps = [s for s in raw_plan if isinstance(s, str)]
        analysis_plan = "\n".join(f"{i}. {s}" for i, s in enumerate(steps, 1))
    else:
        analysis_plan = str(raw_plan)

    return {
        "language": plan.get("language", "unknown"),
        "risk_level": plan.get("risk_level", "MEDIUM"),
        "scope": plan.get("scope", ""),
        "analysis_plan": analysis_plan,
        "key_areas": plan.get("key_areas", []),
        "current_agent": "planner",
    }
