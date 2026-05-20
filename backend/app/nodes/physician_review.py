from backend.app.state import MedicalState


def physician_review_node(state: MedicalState) -> MedicalState:
    if not state.get("physician_treatment"):
        return {"waiting_for": "physician", "next": "physician_review"}
    return {"waiting_for": "done", "next": "report_agent"}
