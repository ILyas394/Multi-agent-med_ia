from backend.app.state import MedicalState


def report_agent_node(state: MedicalState) -> MedicalState:
    final_report = f"""
RAPPORT FINAL D'ORIENTATION CLINIQUE

1. Cas initial
{state.get("initial_case", "").strip()}

2. Synthese clinique preliminaire
{state.get("diagnostic_summary", "").strip()}

3. Recommandation intermediaire
{state.get("interim_care", "").strip()}

4. Avis du medecin traitant
{state.get("physician_treatment", "").strip()}

5. Mention obligatoire
Ce systeme ne remplace pas une consultation medicale.
""".strip()

    return {"final_report": final_report, "waiting_for": "done", "next": "FINISH"}
