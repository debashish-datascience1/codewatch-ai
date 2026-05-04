# 🔍 CodeWatch AI

> **Multi-Agent Code Intelligence & Security Analysis System**
> Built with LangGraph · Groq (Llama 3.3 70B) · ChromaDB · Streamlit · 100% Free

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.2+-orange?logo=langchain)](https://langchain-ai.github.io/langgraph/)
[![Groq](https://img.shields.io/badge/Groq-Llama_3.3_70B-green)](https://groq.com)
[![ChromaDB](https://img.shields.io/badge/VectorDB-ChromaDB-purple)](https://www.trychroma.com/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-red?logo=streamlit)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## What is CodeWatch AI?

CodeWatch AI is a **production-grade, multi-agent agentic system** that autonomously analyzes source code for security vulnerabilities, explains findings with contextual reasoning, and generates actionable auto-fix suggestions — all powered by free, open-source LLMs.

Upload a file, paste code, or point it at a GitHub URL. The agent pipeline takes over from there.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CODEWATCH AI SYSTEM                          │
│                                                                     │
│   User Input (File / Paste / GitHub URL)                            │
│          │                                                          │
│          ▼                                                          │
│   ┌─────────────────┐      ┌──────────────────────────────────┐    │
│   │   Streamlit UI  │      │     RAG Knowledge Base           │    │
│   │   (Frontend)    │      │  ┌──────────┐  ┌─────────────┐  │    │
│   └────────┬────────┘      │  │ OWASP    │  │  CWE/CVE    │  │    │
│            │               │  │ Top 10   │  │  Patterns   │  │    │
│            ▼               │  └──────────┘  └─────────────┘  │    │
│   ┌─────────────────┐      │  ┌──────────┐  ┌─────────────┐  │    │
│   │  LangGraph      │◄────►│  │ Secure   │  │ Anti-Pattern│  │    │
│   │  State Machine  │      │  │ Coding   │  │ Examples    │  │    │
│   └────────┬────────┘      │  └──────────┘  └─────────────┘  │    │
│            │               │         ChromaDB + HF Embeddings  │    │
│            ▼               └──────────────────────────────────┘    │
│   ╔═════════════════════════════════════════════════════╗          │
│   ║              MULTI-AGENT PIPELINE                   ║          │
│   ║                                                     ║          │
│   ║  ┌──────────┐   ┌──────────┐   ┌──────────────┐   ║          │
│   ║  │  Agent 1 │──►│  Agent 2 │──►│   Agent 3    │   ║          │
│   ║  │ Planner  │   │  Code    │   │  Security    │   ║          │
│   ║  │          │   │  Parser  │   │  Scanner     │   ║          │
│   ║  └──────────┘   └──────────┘   └──────┬───────┘   ║          │
│   ║                                        │           ║          │
│   ║  ┌──────────┐   ┌──────────┐          │           ║          │
│   ║  │  Agent 5 │◄──│  Agent 4 │◄─────────┘           ║          │
│   ║  │  Report  │   │  Fix     │                       ║          │
│   ║  │  Writer  │   │  Generator│                      ║          │
│   ║  └──────────┘   └──────────┘                       ║          │
│   ║                                                     ║          │
│   ║           LLM: Groq API → Llama 3.3 70B             ║          │
│   ╚═════════════════════════════════════════════════════╝          │
│            │                                                        │
│            ▼                                                        │
│   ┌─────────────────────────────────────────────────────┐          │
│   │  Structured Output: Vulnerability Report + Fixes    │          │
│   │  Severity: CRITICAL / HIGH / MEDIUM / LOW / INFO    │          │
│   └─────────────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────────────────┘
```

### LangGraph State Flow

```
START
  │
  ▼
[planner_node] ──► decides scope, language, and risk level
  │
  ▼
[parser_node] ──► AST parsing, function/class extraction, dependency mapping
  │
  ▼
[scanner_node] ──► RAG retrieval + LLM reasoning over code chunks
  │             ──► returns: list of vulnerabilities with CWE IDs
  │
  ▼
[fix_generator_node] ──► per-vulnerability fix with before/after diff
  │
  ▼
[report_writer_node] ──► compiles final structured JSON + markdown report
  │
  ▼
END
```

---

## Agents

| Agent | Role | Key Capability |
|---|---|---|
| **Planner** | Orchestrates the entire pipeline | Determines language, scope, risk level; sets routing conditions |
| **Code Parser** | Structural analysis | AST extraction, function/class mapping, dependency graph |
| **Security Scanner** | Vulnerability detection | RAG over OWASP/CWE KB + LLM reasoning; assigns CWE IDs and severity |
| **Fix Generator** | Auto-remediation | Produces before/after diffs with explanation per vulnerability |
| **Report Writer** | Output synthesis | Compiles structured JSON + human-readable markdown report |

---

## Tech Stack

| Layer | Technology | Cost |
|---|---|---|
| LLM | Groq API — Llama 3.3 70B | Free tier |
| Agent Orchestration | LangGraph | Free / Open Source |
| Vector DB | ChromaDB | Free / Open Source |
| Embeddings | HuggingFace `all-MiniLM-L6-v2` | Free / Local |
| Code Parsing | Python `ast` + `tree-sitter` | Free / Open Source |
| UI | Streamlit | Free |
| Knowledge Base | OWASP Top 10 + CWE patterns (custom curated) | Free |
| Containerization | Docker | Free |

---

## Features

- [x] Multi-language support: Python, JavaScript, PHP, Java
- [x] 5-agent LangGraph pipeline with typed state
- [x] RAG over OWASP Top 10 + CWE vulnerability knowledge base
- [x] Severity classification: CRITICAL / HIGH / MEDIUM / LOW / INFO
- [x] Auto-fix suggestions with before/after code diffs
- [x] Structured JSON + Markdown report export
- [x] Streamlit web UI with file upload and paste support
- [x] GitHub URL input support (fetch and analyze public repos)
- [x] Docker containerization for one-command deployment
- [ ] Batch analysis (multiple files / full repo scan)
- [ ] CI/CD GitHub Action integration
- [ ] VS Code Extension

---

## Project Structure

```
codewatch-ai/
│
├── agents/
│   ├── planner.py            # Agent 1: Orchestrator & scope planner
│   ├── parser.py             # Agent 2: AST-based code parser
│   ├── scanner.py            # Agent 3: RAG-powered security scanner
│   ├── fix_generator.py      # Agent 4: Auto-fix suggestion generator
│   └── report_writer.py      # Agent 5: Report synthesis agent
│
├── graph/
│   ├── state.py              # LangGraph TypedDict state schema
│   ├── pipeline.py           # LangGraph StateGraph definition
│   └── router.py             # Conditional edge routing logic
│
├── rag/
│   ├── knowledge_base/
│   │   ├── owasp_top10.md    # OWASP Top 10 vulnerability descriptions
│   │   ├── cwe_patterns.json # CWE ID → pattern → example mapping
│   │   └── secure_coding.md  # Secure coding guidelines per language
│   ├── embeddings.py         # HuggingFace embedding setup
│   ├── vectorstore.py        # ChromaDB init + retriever
│   └── ingest.py             # KB ingestion script
│
├── tools/
│   ├── ast_parser.py         # Python AST + tree-sitter utilities
│   ├── github_fetcher.py     # GitHub URL → raw code fetcher
│   └── diff_generator.py     # Before/after diff utility
│
├── ui/
│   └── app.py                # Streamlit frontend
│
├── config/
│   └── settings.py           # Groq API key, model config, thresholds
│
├── tests/
│   ├── sample_code/          # Deliberately vulnerable code samples
│   └── test_pipeline.py      # End-to-end pipeline tests
│
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── .env.example
├── requirements.txt
└── README.md
```

---

## Roadmap

### Phase 1 — Foundation (Week 1)
- [ ] Repo setup, virtual environment, `.env` config
- [ ] Groq API integration + basic LLM call
- [ ] LangGraph state schema (`CodeAnalysisState`)
- [ ] Single-node pipeline (planner only) running end-to-end
- [ ] ChromaDB setup + HuggingFace embeddings working locally

### Phase 2 — Core Pipeline (Week 2)
- [ ] Code Parser agent: AST extraction for Python + JS
- [ ] Security Scanner agent with RAG retrieval
- [ ] Ingest OWASP Top 10 + basic CWE patterns into ChromaDB
- [ ] Full 5-node LangGraph pipeline connected
- [ ] CLI runner: `python run.py --file sample.py`

### Phase 3 — Intelligence Layer (Week 3)
- [ ] Fix Generator agent producing before/after diffs
- [ ] Report Writer agent generating structured JSON report
- [ ] Conditional routing: skip fix generation for INFO severity
- [ ] CWE ID tagging on each vulnerability finding
- [ ] Severity scoring logic

### Phase 4 — UI & UX (Week 4)
- [ ] Streamlit app: file upload, code paste, GitHub URL input
- [ ] Results dashboard: severity breakdown, vulnerability cards
- [ ] Export report as Markdown / JSON / PDF
- [ ] Progress indicators for each agent step

### Phase 5 — Hardening & DevEx (Week 5)
- [ ] Expand KB: PHP, Java vulnerability patterns
- [ ] Docker + docker-compose for one-command setup
- [ ] GitHub Actions workflow for CI testing
- [ ] Batch scan: accept zip file or GitHub repo URL
- [ ] README polish, demo GIF, sample reports

### Phase 6 — Stretch Goals
- [ ] VS Code Extension wrapper
- [ ] Webhook support for GitHub PR auto-scan
- [ ] Leaderboard / scoring across scans
- [ ] Fine-tuned embeddings on security-specific corpus

---

## Quickstart (coming soon)

```bash
git clone https://github.com/debashish-datascience1/codewatch-ai
cd codewatch-ai
cp .env.example .env          # add your free Groq API key
pip install -r requirements.txt
python rag/ingest.py          # build the vector knowledge base
streamlit run ui/app.py
```

Get your **free** Groq API key at [console.groq.com](https://console.groq.com) — no credit card required.

---

## Sample Output

```json
{
  "file": "app.py",
  "language": "Python",
  "scan_duration_sec": 4.2,
  "total_vulnerabilities": 3,
  "severity_breakdown": {
    "CRITICAL": 1,
    "HIGH": 1,
    "MEDIUM": 1
  },
  "findings": [
    {
      "id": "VLN-001",
      "cwe_id": "CWE-89",
      "title": "SQL Injection via unsanitized user input",
      "severity": "CRITICAL",
      "line": 42,
      "description": "User-controlled input is directly concatenated into SQL query without parameterization.",
      "fix": "Use parameterized queries: cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))"
    }
  ]
}
```

---

## Author

**Debashish Mohapatra** — Cloud AI Engineer · NCIIPC AI Grand Challenge Winner

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](https://linkedin.com/in/debashish--mohapatra)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?logo=github)](https://github.com/debashish-datascience1)
[![Portfolio](https://img.shields.io/badge/Portfolio-Visit-green)](https://mohapatradebashish.vercel.app)

---

## License

MIT License — free to use, fork, and build upon.
