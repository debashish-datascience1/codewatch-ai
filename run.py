"""
CodeWatch AI — CLI entry point.

Usage:
    python run.py --file tests/sample_code/vulnerable_app.py
    python run.py --code "import os; os.system(user_input)"
"""

import argparse
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich import print as rprint

console = Console()

BANNER = """
 ██████╗ ██████╗ ██████╗ ███████╗██╗    ██╗ █████╗ ████████╗ ██████╗██╗  ██╗
██╔════╝██╔═══██╗██╔══██╗██╔════╝██║    ██║██╔══██╗╚══██╔══╝██╔════╝██║  ██║
██║     ██║   ██║██║  ██║█████╗  ██║ █╗ ██║███████║   ██║   ██║     ███████║
██║     ██║   ██║██║  ██║██╔══╝  ██║███╗██║██╔══██║   ██║   ██║     ██╔══██║
╚██████╗╚██████╔╝██████╔╝███████╗╚███╔███╔╝██║  ██║   ██║   ╚██████╗██║  ██║
 ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝ ╚══╝╚══╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝
                  Multi-Agent Code Security Intelligence
"""

SEVERITY_COLORS = {
    "CRITICAL": "bold red",
    "HIGH": "red",
    "MEDIUM": "yellow",
    "LOW": "cyan",
    "INFO": "dim",
}


def _initial_state(code: str, filename: str) -> dict:
    return {
        "raw_code": code,
        "filename": filename,
        "language": "",
        "risk_level": "",
        "scope": "",
        "analysis_plan": "",
        "key_areas": [],
        "code_chunks": [],
        "functions": [],
        "dependencies": [],
        "vulnerabilities": [],
        "fixes": [],
        "report": None,
        "current_agent": "start",
        "error": None,
    }


def _print_planner_results(result: dict) -> None:
    console.print(Rule("[bold green]Planner Agent — Results[/bold green]"))

    # Risk level badge
    risk = result.get("risk_level", "UNKNOWN")
    color = SEVERITY_COLORS.get(risk, "white")
    console.print(f"\n  Language  : [bold cyan]{result.get('language', 'unknown')}[/bold cyan]")
    console.print(f"  Risk Level: [{color}]{risk}[/{color}]")
    console.print(f"  Scope     : {result.get('scope', '')}\n")

    # Key areas table
    areas = result.get("key_areas", [])
    if areas:
        table = Table(title="Key Areas to Analyse", show_lines=True, style="dim")
        table.add_column("#", style="bold", width=4)
        table.add_column("Area")
        for i, area in enumerate(areas, 1):
            table.add_row(str(i), area)
        console.print(table)

    # Analysis plan
    plan = result.get("analysis_plan", "")
    if plan:
        console.print(Panel(plan, title="[bold]Analysis Plan[/bold]", border_style="cyan"))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="CodeWatch AI — Multi-Agent Code Security Scanner"
    )
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--file", "-f", metavar="PATH", help="Path to source file")
    input_group.add_argument("--code", "-c", metavar="CODE", help="Inline code string")
    args = parser.parse_args()

    # ── Load code ────────────────────────────────────────────
    if args.file:
        path = Path(args.file)
        if not path.exists():
            console.print(f"[red]Error: file not found — {args.file}[/red]")
            sys.exit(1)
        code = path.read_text(encoding="utf-8")
        filename = path.name
    else:
        code = args.code
        filename = "inline_code.txt"

    # ── Banner ───────────────────────────────────────────────
    console.print(f"[bold cyan]{BANNER}[/bold cyan]")
    console.print(Panel(
        f"[bold]File:[/bold] {filename}    [bold]Lines:[/bold] {len(code.splitlines())}",
        border_style="cyan",
    ))

    # ── Import pipeline (imports Groq — validate key first) ──
    try:
        from graph.pipeline import pipeline
    except EnvironmentError as e:
        console.print(f"\n[red]{e}[/red]")
        sys.exit(1)

    # ── Run pipeline ─────────────────────────────────────────
    initial = _initial_state(code, filename)

    with console.status("[bold green]Running Planner Agent...[/bold green]", spinner="dots"):
        result = pipeline.invoke(initial)

    _print_planner_results(result)

    console.print("\n[dim]Phase 1 complete. Phases 2-5 (parser, scanner, fix generator, report) coming soon.[/dim]\n")


if __name__ == "__main__":
    main()
