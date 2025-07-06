from crewai import Crew, Process

from agentic_ai.llm.llm_utils import get_crew_llm

from agentic_ai.agents.publication_fetcher_agent import get_publication_fetcher_agent
from agentic_ai.agents.plain_english_explainer_agent import get_plain_english_explainer_agent
from agentic_ai.agents.recursive_summarizer_agent import get_recursive_summarizer_agent

from agentic_ai.tasks.publication_fetcher_task import get_publication_fetcher_task
from agentic_ai.tasks.plain_english_explainer_task import get_plain_english_explainer_task
from agentic_ai.tasks.recursive_summarizer_task import get_recursive_summarizer_task

def trigger_agentic_ai_workflow(input_query, latest_publication_count):

    publication_fetcher_agent = get_publication_fetcher_agent()
    publication_fetcher_task = get_publication_fetcher_task(publication_fetcher_agent)

    plain_english_explainer_agent = get_plain_english_explainer_agent()
    plain_english_explainer_task = get_plain_english_explainer_task(plain_english_explainer_agent)

    recursive_summarizer_agent = get_recursive_summarizer_agent()
    recursive_summarizer_task = get_recursive_summarizer_task(recursive_summarizer_agent)

    # Create a crew to execute the task
    crew = Crew(
        agents=[publication_fetcher_agent, plain_english_explainer_agent, recursive_summarizer_agent],
        tasks=[publication_fetcher_task, plain_english_explainer_task, recursive_summarizer_task],
        process=Process.sequential,
        verbose=True,
        manager_llm=get_crew_llm()
    )

    # Run the crew and get the analysis
    result = crew.kickoff(inputs={
            "input_query": input_query,
            "latest_publication_count": latest_publication_count
        }
    )

    print("Printing Result")
    print("\r\n====================\r\n")
    print(result)
    print("\r\n====================\r\n")
    print(str(result))