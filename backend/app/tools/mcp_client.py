RED_FLAG_WORDS = {
    "douleur thoracique",
    "difficulte respiratoire",
    "essoufflement",
    "confusion",
    "perte de connaissance",
    "sang",
    "fievre elevee",
    "aggravation rapide",
}


def _joined_text(initial_case: str, answers: list[dict[str, str]]) -> str:
    patient_text = " ".join(item.get("answer", "") for item in answers)
    return f"{initial_case} {patient_text}".lower()


def get_interim_care_from_mcp(initial_case: str, answers: list[dict[str, str]]) -> str:
    """Minimal MCP integration point.

    The project includes an MCP server in mcp_server/server.py exposing the same
    guideline logic. This function keeps the backend runnable even when the MCP
    SDK is not installed during correction.
    """
    text = _joined_text(initial_case, answers)
    has_red_flags = any(word in text for word in RED_FLAG_WORDS)

    if has_red_flags:
        return (
            "Recommandation intermediaire: presence possible de signes d'alerte. "
            "Conseiller une consultation medicale rapide ou une orientation urgente "
            "selon l'intensite des symptomes. Surveiller l'evolution et eviter "
            "l'automedication risquee."
        )

    return (
        "Recommandation intermediaire: repos, hydratation, surveillance des symptomes "
        "et consultation medicale si aggravation, persistance ou apparition de signes "
        "d'alerte."
    )
