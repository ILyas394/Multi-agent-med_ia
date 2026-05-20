from langgraph.graph import END, START, StateGraph

from backend.app.nodes.diagnostic_agent import diagnostic_agent_node
from backend.app.nodes.physician_review import physician_review_node
from backend.app.nodes.report_agent import report_agent_node
from backend.app.nodes.supervisor import supervisor_node
from backend.app.state import MedicalState


def route_from_supervisor(state: MedicalState) -> str:
    return state.get("next", "diagnostic_agent")


def route_after_diagnostic(state: MedicalState) -> str:
    if state.get("waiting_for") == "patient":
        return "WAIT"
    return "supervisor"


def route_after_physician_review(state: MedicalState) -> str:
    if state.get("waiting_for") == "physician":
        return "WAIT"
    return "supervisor"


def build_graph():
    graph = StateGraph(MedicalState)

    graph.add_node("supervisor", supervisor_node)
    graph.add_node("diagnostic_agent", diagnostic_agent_node)
    graph.add_node("physician_review", physician_review_node)
    graph.add_node("report_agent", report_agent_node)

    graph.add_edge(START, "supervisor")
    graph.add_conditional_edges(
        "supervisor",
        route_from_supervisor,
        {
            "diagnostic_agent": "diagnostic_agent",
            "physician_review": "physician_review",
            "report_agent": "report_agent",
            "FINISH": END,
        },
    )
    graph.add_conditional_edges(
        "diagnostic_agent",
        route_after_diagnostic,
        {"WAIT": END, "supervisor": "supervisor"},
    )
    graph.add_conditional_edges(
        "physician_review",
        route_after_physician_review,
        {"WAIT": END, "supervisor": "supervisor"},
    )
    graph.add_edge("report_agent", "supervisor")

    return graph.compile()


medical_graph = build_graph()
