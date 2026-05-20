# Projet multi-agents medical avec LangGraph

Ce projet realise une version simple et claire du cahier des charges `Cahier_des_charges_Projet_MultiAgents_Medical.pdf`.

## Decoupage du cahier des charges

1. **Contexte**: simuler une orientation clinique preliminaire.
2. **Ethique**: ne pas produire de diagnostic definitif.
3. **Agents**: Supervisor, Diagnostic Agent, Physician Review, Report Agent.
4. **Workflow**: 5 questions patient, recommandation intermediaire, validation medecin, rapport final.
5. **Backend**: Python, LangGraph, FastAPI.
6. **MCP**: outil minimal de recommandation intermediaire.
7. **Frontend**: interface Streamlit.
8. **Tests**: trois scenarios dans `examples/test_cases.md`.
9. **Livrables**: code, README, rapport technique et demonstration.

## Structure

```text
backend/
  app/
    api.py
    graph.py
    state.py
    nodes/
    tools/
mcp_server/
  server.py
frontend/
  streamlit_app.py
docs/
  decoupage_cahier_des_charges.md
  rapport_technique.md
examples/
  test_cases.md
langgraph.json
```

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r backend/requirements.txt
python -m pip install -r frontend/requirements.txt
```

## Lancer l'API

```bash
uvicorn backend.app.api:app --reload --port 8000
```

Documentation API:

```text
http://localhost:8000/docs
```

## Lancer le frontend

Dans un deuxieme terminal:

```bash
streamlit run frontend/streamlit_app.py
```

## Lancer le serveur MCP

Optionnel pour la demonstration:

```bash
python mcp_server/server.py
```

## Tester avec curl

Demarrer une consultation:

```bash
curl -X POST http://localhost:8000/consultation/start ^
  -H "Content-Type: application/json" ^
  -d "{\"initial_case\":\"Patient avec toux et fatigue depuis deux jours\"}"
```

Repondre aux questions:

```bash
curl -X POST http://localhost:8000/consultation/{thread_id}/resume ^
  -H "Content-Type: application/json" ^
  -d "{\"answer\":\"Depuis deux jours\"}"
```

Apres les 5 reponses, ajouter l'avis medecin:

```bash
curl -X POST http://localhost:8000/consultation/{thread_id}/resume ^
  -H "Content-Type: application/json" ^
  -d "{\"physician_treatment\":\"Repos, hydratation, paracetamol si besoin, consultation si aggravation.\"}"
```

Lire le rapport:

```bash
curl http://localhost:8000/consultation/{thread_id}/report
```

## LangGraph Studio

Le fichier `langgraph.json` expose le graphe:

```text
medical_graph -> backend/app/graph.py:medical_graph
```

## Mention obligatoire

Le rapport final contient:

```text
Ce systeme ne remplace pas une consultation medicale.
```
>>>>>>> 9512377 (Initial commit)
