from crewai import Agent
from agentic_ai.tools.publication_fetcher_tool import publication_fetcher_tool

GOAL = """
Retrieve a list of PubMed publications for a given query and count.
Use the tool `publication_fetcher_tool` with a JSON-formatted input string.
Ensure the output is a valid JSON array. Each item should be a dictionary with publication metadata.
"""

BACKSTORY = """
You specialize in biomedical literature searches. You use tools to query PubMed based on specific input criteria.
You must always return a valid JSON array of publications.
"""

def get_publication_fetcher_agent():
    return Agent(
        role="Publication Fetcher Agent",
        goal=GOAL,
        memory=False,
        verbose=True,
        backstory=BACKSTORY,
        tools=[publication_fetcher_tool]
    )

