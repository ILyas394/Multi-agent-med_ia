from mcp.server.fastmcp import FastMCP

mcp = FastMCP("medical-care-tools")


@mcp.tool()
def recommend_interim_care(patient_text: str) -> str:
    """Return cautious interim care guidance for an academic demo."""
    text = patient_text.lower()
    red_flags = [
        "douleur thoracique",
        "difficulte respiratoire",
        "essoufflement",
        "confusion",
        "perte de connaissance",
        "sang",
        "fievre elevee",
        "aggravation rapide",
    ]
    if any(flag in text for flag in red_flags):
        return (
            "Presence possible de signes d'alerte: recommander une consultation "
            "medicale rapide ou une orientation urgente selon le contexte."
        )
    return (
        "Repos, hydratation, surveillance et consultation medicale si aggravation "
        "ou apparition de signes d'alerte."
    )


if __name__ == "__main__":
    mcp.run()
