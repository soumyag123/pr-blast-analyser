from pathlib import Path

from langgraph.graph import END, StateGraph

from app.agents.state import AnalysisState
from app.analyzers.impact_analyzer import analyze_impact
from app.services.code_scanner_service import scan_service_for_change
from app.services.contract_service import analyze_openapi_contract
from app.services.dependency_service import find_candidate_consumers
from app.services.report_service import build_and_save_report


def load_changes(_: AnalysisState) -> AnalysisState:
    """Load contract changes for analysis."""
    changes = analyze_openapi_contract(
        service_name="user-service",
        file_path="specs/openapi.yaml",
        base_spec_path=Path("services/user-service/specs/base/openapi.yaml"),
        head_spec_path=Path("services/user-service/specs/head/openapi.yaml"),
    )
    return {"changes": changes}


def analyze_findings(state: AnalysisState) -> AnalysisState:
    """Analyze downstream impact findings."""
    changes = state["changes"]
    findings = []

    for change in changes:
        candidates = find_candidate_consumers(change)
        for candidate in candidates:
            if candidate.service_name == "shared-docs":
                continue
            service_root = Path("services") / candidate.service_name
            evidence = scan_service_for_change(service_root, candidate.service_name, change)
            findings.append(analyze_impact(change, candidate.service_name, evidence))

    return {"findings": findings}


def build_report(state: AnalysisState) -> AnalysisState:
    """Build and persist the analysis report."""
    report, report_path = build_and_save_report(
        "user-service",
        state["changes"],
        state["findings"],
    )
    return {"report": report, "report_path": report_path.as_posix()}


def create_workflow():
    """Create the LangGraph workflow."""
    graph = StateGraph(AnalysisState)
    graph.add_node("load_changes", load_changes)
    graph.add_node("analyze_findings", analyze_findings)
    graph.add_node("build_report", build_report)
    graph.set_entry_point("load_changes")
    graph.add_edge("load_changes", "analyze_findings")
    graph.add_edge("analyze_findings", "build_report")
    graph.add_edge("build_report", END)
    return graph.compile()


def run_langgraph_analysis() -> AnalysisState:
    """Run the LangGraph analysis workflow."""
    workflow = create_workflow()
    return workflow.invoke({})
