from app.agents.langgraph_workflow import run_langgraph_analysis


def test_run_langgraph_analysis_returns_expected_state() -> None:
    """Verify the LangGraph workflow returns report state."""
    state = run_langgraph_analysis()

    assert state["changes"]
    assert state["findings"]
    assert state["report"].service_name == "user-service"
    assert state["report_path"].endswith(".md")
