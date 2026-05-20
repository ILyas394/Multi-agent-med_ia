from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend.app.graph import medical_graph
from backend.app.state import MedicalState

app = FastAPI(title="Medical Multi-Agent Demo")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SESSIONS: dict[str, MedicalState] = {}


class StartConsultationRequest(BaseModel):
    initial_case: str = Field(..., min_length=3)


class ResumeConsultationRequest(BaseModel):
    thread_id: str | None = None
    answer: str | None = None
    physician_treatment: str | None = None


@app.get("/")
def healthcheck():
    return {"status": "ok", "project": "medical-multi-agent"}


@app.post("/sessions/start")
def start_session():
    thread_id = str(uuid4())
    SESSIONS[thread_id] = {
        "thread_id": thread_id,
        "patient_answers": [],
        "question_count": 0,
        "waiting_for": "patient",
    }
    return {"thread_id": thread_id}


@app.post("/consultation/start")
def start_consultation(payload: StartConsultationRequest):
    thread_id = str(uuid4())
    state: MedicalState = {
        "thread_id": thread_id,
        "initial_case": payload.initial_case,
        "patient_answers": [],
        "question_count": 0,
    }
    new_state = medical_graph.invoke(state)
    SESSIONS[thread_id] = new_state
    return {"thread_id": thread_id, "state": public_state(new_state)}


@app.post("/consultation/{thread_id}/resume")
@app.post("/consultation/resume")
def resume_consultation(payload: ResumeConsultationRequest, thread_id: str | None = None):
    if thread_id is None:
        thread_id = payload.thread_id
    if thread_id is None:
        raise HTTPException(status_code=400, detail="Le thread_id est obligatoire.")
    state = get_state(thread_id)
    waiting_for = state.get("waiting_for")

    if waiting_for == "patient":
        if not payload.answer:
            raise HTTPException(status_code=400, detail="La reponse patient est obligatoire.")
        question = state.get("current_question", "")
        answers = state.get("patient_answers", [])
        answers.append({"question": question, "answer": payload.answer})
        state["patient_answers"] = answers

    elif waiting_for == "physician":
        if not payload.physician_treatment:
            raise HTTPException(status_code=400, detail="L'avis du medecin est obligatoire.")
        state["physician_treatment"] = payload.physician_treatment

    elif waiting_for == "done":
        return {"thread_id": thread_id, "state": public_state(state)}

    new_state = medical_graph.invoke(state)
    SESSIONS[thread_id] = new_state
    return {"thread_id": thread_id, "state": public_state(new_state)}


@app.get("/consultation/{thread_id}")
def get_consultation(thread_id: str):
    return {"thread_id": thread_id, "state": public_state(get_state(thread_id))}


@app.get("/consultation/{thread_id}/report")
def get_report(thread_id: str):
    state = get_state(thread_id)
    if not state.get("final_report"):
        raise HTTPException(status_code=404, detail="Le rapport final n'est pas encore disponible.")
    return {"thread_id": thread_id, "final_report": state["final_report"]}


def get_state(thread_id: str) -> MedicalState:
    try:
        return SESSIONS[thread_id]
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Consultation introuvable.") from exc


def public_state(state: MedicalState) -> dict:
    return {
        "initial_case": state.get("initial_case"),
        "waiting_for": state.get("waiting_for"),
        "question_count": state.get("question_count", 0),
        "current_question": state.get("current_question"),
        "patient_answers": state.get("patient_answers", []),
        "diagnostic_summary": state.get("diagnostic_summary"),
        "interim_care": state.get("interim_care"),
        "physician_treatment": state.get("physician_treatment"),
        "final_report": state.get("final_report"),
    }
