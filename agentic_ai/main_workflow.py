import json
from crewai import Crew, Process

from agentic_ai.llm.llm_utils import get_crew_llm

from agentic_ai.agents.publication_fetcher_agent import get_publication_fetcher_agent
from agentic_ai.agents.plain_english_explainer_agent import get_plain_english_explainer_agent
from agentic_ai.agents.recursive_summarizer_agent import get_recursive_summarizer_agent
from agentic_ai.agents.title_generator_agent import get_title_generator_agent
from agentic_ai.agents.mindmap_generator_agent import get_mindmap_generator_agent

from agentic_ai.tasks.publication_fetcher_task import get_publication_fetcher_task
from agentic_ai.tasks.plain_english_explainer_task import get_plain_english_explainer_task
from agentic_ai.tasks.recursive_summarizer_task import get_recursive_summarizer_task
from agentic_ai.tasks.title_generator_task import get_title_generator_task
from agentic_ai.tasks.mindmap_generator_task import get_mindmap_generator_task

def trigger_agentic_ai_workflow(input_query, latest_publication_count):

    publication_fetcher_agent = get_publication_fetcher_agent()
    publication_fetcher_task = get_publication_fetcher_task(publication_fetcher_agent)

    plain_english_explainer_agent = get_plain_english_explainer_agent()
    plain_english_explainer_task = get_plain_english_explainer_task(plain_english_explainer_agent)

    recursive_summarizer_agent = get_recursive_summarizer_agent()
    recursive_summarizer_task = get_recursive_summarizer_task(recursive_summarizer_agent)

    title_generator_agent = get_title_generator_agent()
    title_generator_task = get_title_generator_task(title_generator_agent)

    mindmap_generator_agent = get_mindmap_generator_agent()
    mindmap_generator_task = get_mindmap_generator_task(mindmap_generator_agent)

    # Create a crew to execute the task
    crew = Crew(
        agents=[
            publication_fetcher_agent, plain_english_explainer_agent, recursive_summarizer_agent,
            title_generator_agent, mindmap_generator_agent
        ],
        tasks=[
            publication_fetcher_task, plain_english_explainer_task, recursive_summarizer_task,
            title_generator_task, mindmap_generator_task
        ],
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

    results = {}

    print("Printing Results")
    for task in crew.tasks:
        print(f"--- {task.name} ---")
        print(task.output)

        if "recursive_summarizer_task" in task.name:
            try:
                data = json.loads(task.output.raw)
                results["contents"] = data.get("summary", "")
                results["references"] = data.get("references", "")
            except Exception as e:
                print("An error occurred:", e)
                results["contents"] = ""
                results["references"] = ""
        elif "title_generator_task" in task.name:
            results["title"] = task.output
        elif "mindmap_generator_task" in task.name:
            results["mindmap"] = task.output

    print("\r\n====================\r\n")
    print(result)
    print("\r\n====================\r\n")
    print(str(result))

    return results