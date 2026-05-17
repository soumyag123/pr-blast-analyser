from app.agents.langgraph_workflow import run_langgraph_analysis
from app.domain.findings import ImpactFinding
from app.domain.report import AnalysisReport


def run_blast_radius_analysis() -> tuple[AnalysisReport, list[ImpactFinding], str]:
    """Run the full local blast radius analysis workflow."""
    state = run_langgraph_analysis()
    return state["report"], state["findings"], state["report_path"]
