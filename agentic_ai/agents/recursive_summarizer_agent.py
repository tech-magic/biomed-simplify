from crewai import Agent

def get_recursive_summarizer_agent():
    return Agent(
        role="Recursive Summarizer",
        goal="Merge multiple plain summaries into a cohesive combined summary.",
        backstory="An expert summarizer who can merge multiple research summaries into one.",
        allow_delegation=False
    )
