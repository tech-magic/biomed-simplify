from crewai import Agent

def get_title_generator_agent():
    return Agent(
        name="title_generator_agent",
        role="Title Generator",
        goal="Generate concise and informative titles for scientific summaries.",
        backstory="A headline writer trained to produce crisp and catchy article titles.",
        allow_delegation=False,
        memory=False
    )
