import json

from typing import List, Dict, Any
from crewai import Crew, Process, Task

from agentic_ai.llm.llm_utils import get_crew_llm

SUMMARY_PROMPT_TEMPLATE = """

You are a helpful AI assistant that explains medical research to non-specialists.

TASK:
Summarize the following PubMed abstract in simple, plain English. 
Target audience includes patient advocates, caregivers, and nonprofit health workers.

Keep the explanation short, empathetic, and free from medical jargon.

ABSTRACT:
{abstract}

"""

DESCRIPTION="""

Use the JSON Array from {publication_fetcher_task.output} which contains the list of publications.
Generate plain-English summaries based on the contents of each publication.

"""

EXPECTED_OUTPUT="""

A valid JSON Array containing the list of publications.
Each publication must have its plain-English summary along with the other existing metadata (including id).

"""

class PlainEnglishExplainerTask(Task):
    def __init__(self, plain_english_explainer_agent):
        super().__init__(
            name="plain_english_explainer_task",
            agent=plain_english_explainer_agent,
            description=DESCRIPTION,
            expected_output=EXPECTED_OUTPUT,
            output_format="JSON"
        )

    def execute(self, inputs: Dict[str, Any] = None, context: Dict[str, Any] = None) -> List[Dict]:

        if not context or "publication_fetcher_task.output" not in context:
            raise ValueError("Missing publication_results in context.")

        try:
            publications = json.loads(context["publication_fetcher_task.output"])
        except Exception as e:
            raise ValueError(f"Invalid publication_results JSON: {e}")

        # Create sub-tasks for summarizing each abstract
        sub_tasks = []
        for pub in publications:
            if pub.get("id") and pub.get("abstract"):
                prompt = SUMMARY_PROMPT_TEMPLATE.format(abstract=pub["abstract"])
                sub_task = Task(
                    agent=self.agent,
                    description=prompt,
                    expected_output="Short plain-English summary",
                    output_format="text",
                    metadata={"id": pub["id"]},
                    verbose=True
                )
                sub_tasks.append(sub_task)

        sub_crew = Crew(
            agents=[self.agent],
            tasks=sub_tasks,
            process=Process.parallel,
            manager_llm=get_crew_llm()
        )

        sub_results = sub_crew.run()

        return [
            {"id": task.metadata["id"], "summary": result.strip()}
            for task, result in zip(sub_tasks, sub_results)
        ]
    
def get_plain_english_explainer_task(plain_english_explainer_agent):
    return PlainEnglishExplainerTask(plain_english_explainer_agent)