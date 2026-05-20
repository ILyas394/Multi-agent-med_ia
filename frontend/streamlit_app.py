import requests
import streamlit as st

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Orientation clinique", layout="centered")
st.title("Orientation clinique multi-agents")

if "thread_id" not in st.session_state:
    st.session_state.thread_id = None
if "state" not in st.session_state:
    st.session_state.state = None


def refresh_state():
    response = requests.get(f"{API_URL}/consultation/{st.session_state.thread_id}", timeout=10)
    response.raise_for_status()
    st.session_state.state = response.json()["state"]


with st.sidebar:
    st.header("Nouvelle consultation")
    initial_case = st.text_area("Cas initial patient", height=120)
    if st.button("Demarrer", type="primary"):
        response = requests.post(
            f"{API_URL}/consultation/start",
            json={"initial_case": initial_case},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        st.session_state.thread_id = data["thread_id"]
        st.session_state.state = data["state"]

state = st.session_state.state

if not state:
    st.info("Saisissez un cas initial dans la barre laterale pour commencer.")
    st.stop()

st.caption(f"Consultation: {st.session_state.thread_id}")

if state["waiting_for"] == "patient":
    st.subheader(f"Question {state['question_count'] + 1}/5")
    st.write(state["current_question"])
    answer = st.text_area("Reponse du patient")
    if st.button("Envoyer la reponse"):
        response = requests.post(
            f"{API_URL}/consultation/{st.session_state.thread_id}/resume",
            json={"answer": answer},
            timeout=10,
        )
        response.raise_for_status()
        st.session_state.state = response.json()["state"]
        st.rerun()

elif state["waiting_for"] == "physician":
    st.subheader("Revue du medecin traitant")
    st.text_area("Synthese clinique", value=state["diagnostic_summary"], height=220, disabled=True)
    st.text_area("Recommandation intermediaire", value=state["interim_care"], height=120, disabled=True)
    treatment = st.text_area("Traitement ou conduite a tenir")
    if st.button("Valider la revue medecin", type="primary"):
        response = requests.post(
            f"{API_URL}/consultation/{st.session_state.thread_id}/resume",
            json={"physician_treatment": treatment},
            timeout=10,
        )
        response.raise_for_status()
        st.session_state.state = response.json()["state"]
        st.rerun()

else:
    st.subheader("Rapport final")
    st.text_area("Rapport", value=state["final_report"], height=420)
