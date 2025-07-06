import json

from crewai import Task

DESCRIPTION="""
Use the `publication_fetcher_tool` to retrieve a list of PubMed publications for the provided inputs.

Tool: `publication_fetcher_tool`  
Tool Input: A JSON-formatted string like:
{
    "input_query": "{input_query}",
    "latest_publication_count": {latest_publication_count}
}
"""

EXPECTED_OUPUT="""
A valid JSON array. Each item should be a dictionary representing a single PubMed publication.
"""

def validate_pubmed_json_output(output_str: str) -> bool:
    try:
        data = json.loads(output_str)
        if isinstance(data, list):
            for item in data:
                if not isinstance(item, dict):
                    return False
            return True
        return False
    except json.JSONDecodeError:
        return False

def get_publication_fetcher_task(publication_fetcher_agent):
    return Task(
        name="publication_fetcher_task",
        agent=publication_fetcher_agent,
        description=DESCRIPTION,
        expected_output=EXPECTED_OUPUT,
        output_format="JSON",
        max_retries=10,
        output_validation=validate_pubmed_json_output
    )