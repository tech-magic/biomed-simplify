import json

from typing import Any
from crewai.tools import tool

from agentic_ai.utils.pubmed_fetcher import fetch_pubmed_publications

@tool("publication_fetcher_tool")
def publication_fetcher_tool(tool_input: str) -> Any:
    """
    Returns a JSON array of latest PubMed publications.

    Args:
        tool_input (str): A JSON string with:
            - "input_query" (str)
            - "latest_publication_count" (int)
    """
    try:
        data = json.loads(tool_input)
        input_query = data.get("input_query", "")
        max_results = int(data.get("latest_publication_count", 10))
        return fetch_pubmed_publications(input_query, max_results)
    except Exception as e:
        return {"error": f"Failed to fetch publications: {str(e)}"}