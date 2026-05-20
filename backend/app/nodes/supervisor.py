from backend.app.state import MedicalState


def supervisor_node(state: MedicalState) -> MedicalState:
    if state.get("final_report"):
        return {"next": "FINISH", "waiting_for": "done"}
    if state.get("physician_treatment"):
        return {"next": "report_agent"}
    if state.get("diagnostic_summary") and state.get("interim_care"):
        return {"next": "physician_review"}
    return {"next": "diagnostic_agent"}
