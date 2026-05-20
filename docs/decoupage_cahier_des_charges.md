# Decoupage du cahier des charges

## 1. Contexte et objectif

Le projet simule une orientation clinique preliminaire avec un workflow multi-agents. Il ne fournit pas de diagnostic definitif et reste un exercice academique.

## 2. Cadre ethique

- Ne pas presenter le systeme comme un dispositif medical.
- Ne jamais produire un diagnostic definitif.
- Utiliser des termes prudents: synthese clinique, orientation preliminaire, recommandation intermediaire.
- Ajouter dans le rapport: `Ce systeme ne remplace pas une consultation medicale.`

## 3. Agents obligatoires

- `Supervisor`: choisit la prochaine etape du workflow.
- `Diagnostic Agent`: pose 5 questions et prepare la synthese.
- `Physician Review`: etape humaine pour l'avis du medecin.
- `Report Agent`: genere le rapport final.

## 4. Workflow

```text
START
  -> Supervisor
  -> DiagnosticAgent
  -> ask_patient x5
  -> recommend_interim_care
  -> PhysicianReview
  -> ReportAgent
  -> END
```

## 5. Backend

Le backend utilise Python, FastAPI et LangGraph. Le graphe est defini dans `backend/app/graph.py`.

## 6. MCP

Le dossier `mcp_server/` contient un serveur MCP minimal avec un outil `recommend_interim_care`. Le backend contient aussi un client/fallback dans `backend/app/tools/mcp_client.py` pour garder le projet simple a executer.

## 7. API

- `POST /sessions/start`
- `POST /consultation/start`
- `POST /consultation/resume`
- `POST /consultation/{thread_id}/resume`
- `GET /consultation/{thread_id}`
- `GET /consultation/{thread_id}/report`

## 8. Frontend

Le frontend Streamlit permet:

- de saisir le cas initial;
- de repondre aux 5 questions;
- de saisir l'avis du medecin;
- d'afficher le rapport final.

## 9. Tests attendus

- Syndrome respiratoire simple.
- Cas avec signes d'alerte.
- Cas benin.

Chaque test doit verifier les 5 questions, la recommandation intermediaire, la revue medecin et le rapport final.
