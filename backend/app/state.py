from typing import Annotated, Literal, TypedDict

from langgraph.graph.message import add_messages


class MedicalState(TypedDict, total=False):
    messages: Annotated[list, add_messages]
    thread_id: str
    initial_case: str
    next: Literal[
        "diagnostic_agent",
        "physician_review",
        "report_agent",
        "FINISH",
    ]
    patient_answers: list[dict[str, str]]
    question_count: int
    current_question: str
    waiting_for: Literal["patient", "physician", "done"]
    interim_care: str
    diagnostic_summary: str
    physician_treatment: str
    final_report: str
