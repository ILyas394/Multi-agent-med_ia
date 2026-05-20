# Rapport technique court

## Architecture

Le projet est separe en quatre blocs:

- `backend/`: API FastAPI et graphe LangGraph.
- `backend/app/nodes/`: agents du workflow.
- `backend/app/tools/`: outils patient, soins et integration MCP.
- `frontend/`: interface Streamlit.
- `mcp_server/`: serveur MCP minimal.

## Choix de conception

Le projet utilise une logique deterministe au lieu d'un appel LLM externe afin de rester simple a installer et a demontrer. L'architecture reste compatible avec un modele LLM: les agents peuvent etre remplaces par des chaines LangChain plus avancees.

## Etat partage

L'etat `MedicalState` contient le cas initial, les reponses patient, le nombre de questions, la synthese clinique, la recommandation intermediaire, l'avis du medecin et le rapport final.

## Human-in-the-Loop

Le workflow s'arrete quand `waiting_for = "physician"`. L'API attend alors l'avis du medecin avant de lancer le `Report Agent`.

## Limite ethique

Le rapport final contient obligatoirement la phrase: `Ce systeme ne remplace pas une consultation medicale.`
