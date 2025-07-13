from crewai import Agent

def get_mindmap_generator_agent():
    return Agent(
        name="mindmap_generator_agent",
        role="Mermaid.js Mindmap Generator",
        goal="Generate structured and valid Mermaid.js mindmap code for a given input text",
        backstory="You help research students by organizing complex topics into clear, structured mindmaps using Mermaid.js. You follow strict formatting rules to ensure valid output.",
        allow_delegation=False,
        verbose=True
    )
