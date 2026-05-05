from langgraph.graph import END, START, StateGraph

from agents.planner import planner_node
from graph.state import CodeAnalysisState


def build_pipeline():
    """
    Phase 1: single-node pipeline (planner only).
    Subsequent phases will add parser, scanner, fix_generator, report_writer nodes.
    """
    graph = StateGraph(CodeAnalysisState)

    # ── Nodes ────────────────────────────────────────────────
    graph.add_node("planner", planner_node)

    # ── Edges ────────────────────────────────────────────────
    graph.add_edge(START, "planner")
    graph.add_edge("planner", END)

    return graph.compile()


# Module-level compiled pipeline (imported by run.py and the Streamlit app)
pipeline = build_pipeline()
