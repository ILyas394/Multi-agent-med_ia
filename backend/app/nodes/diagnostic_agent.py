from backend.app.state import MedicalState
from backend.app.tools.care_tools import recommend_interim_care
from backend.app.tools.patient_tools import ask_patient, build_patient_summary


def diagnostic_agent_node(state: MedicalState) -> MedicalState:
    answers = state.get("patient_answers", [])
    question_count = len(answers)

    if question_count < 5:
        return {
            "question_count": question_count,
            "current_question": ask_patient(question_count),
            "waiting_for": "patient",
            "next": "diagnostic_agent",
        }

    summary = build_patient_summary(state.get("initial_case", ""), answers)
    interim_care = recommend_interim_care(state.get("initial_case", ""), answers)
    return {
        "question_count": question_count,
        "current_question": "",
        "diagnostic_summary": (
            "Synthese clinique preliminaire:\n"
            f"{summary}\n"
            "Cette synthese sert uniquement a orienter la revue medicale."
        ),
        "interim_care": interim_care,
        "waiting_for": "physician",
        "next": "physician_review",
    }
