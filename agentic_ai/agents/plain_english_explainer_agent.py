from crewai import Agent

GOAL="""
Translate medical research into simple, jargon-free English.
"""

BACKSTORY="""
You explain complex medical research in plain English for non-specialists like patients and caregivers.
"""
    
def get_plain_english_explainer_agent():
    return Agent(
        role="Plain English Explainer Agent",
        goal=GOAL,
        backstory=BACKSTORY,
        verbose=True,
        memory=False
    )

