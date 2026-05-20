from backend.app.tools.mcp_client import get_interim_care_from_mcp


def recommend_interim_care(initial_case: str, answers: list[dict[str, str]]) -> str:
    """Use the MCP care tool when available, with a deterministic fallback."""
    return get_interim_care_from_mcp(initial_case, answers)
