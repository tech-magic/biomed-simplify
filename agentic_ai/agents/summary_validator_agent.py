from crewai import Agent

def get_summary_validator_agent():
    return Agent(
        role="Summary Quality Validator",
        goal="Determine whether a merged summary is valid, without any mechanical or meta explanation, and that all source IDs are integrated.",
        backstory="An expert editor checking if a summary is clean, natural, and integrates all source citations without referencing the summary process.",
        allow_delegation=False,
        memory=False
    )
