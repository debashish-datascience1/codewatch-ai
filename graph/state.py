import operator
from typing import Annotated, Optional
from typing_extensions import TypedDict


class Vulnerability(TypedDict):
    id: str
    cwe_id: str
    title: str
    severity: str          # CRITICAL | HIGH | MEDIUM | LOW | INFO
    line: int
    code_snippet: str
    description: str
    fix: str


class Fix(TypedDict):
    vulnerability_id: str
    original_code: str
    fixed_code: str
    explanation: str


class CodeAnalysisState(TypedDict):
    # ── Input ────────────────────────────────────────────────
    raw_code: str
    filename: str

    # ── Planner output ───────────────────────────────────────
    language: str
    risk_level: str          # CRITICAL | HIGH | MEDIUM | LOW
    scope: str
    analysis_plan: str
    key_areas: list[str]

    # ── Parser output ────────────────────────────────────────
    code_chunks: list[str]
    functions: list[str]
    dependencies: list[str]

    # ── Scanner output (append-merge across nodes) ───────────
    vulnerabilities: Annotated[list[Vulnerability], operator.add]

    # ── Fix generator output ─────────────────────────────────
    fixes: list[Fix]

    # ── Report writer output ─────────────────────────────────
    report: Optional[dict]

    # ── Control ──────────────────────────────────────────────
    current_agent: str
    error: Optional[str]
