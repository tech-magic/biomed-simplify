from crewai import Task

from agentic_ai.llm.llm_utils import get_crew_llm

DESCRIPTION="""

You are a title-generating assistant.

Use the JSON object from {recursive_summarizer_task.output}, which contains a summary field.
The value of this field is the text summary for which you must generate a title.
Generate a concise, informative, and relevant topic title that best represents the content of the summary.

Return only the title, without quotation marks.

"""

EXPECTED_OUTPUT="""

Return only the title, without quotation marks.

"""

def get_title_generator_task(title_generator_agent):
    return Task(
        name="title_generator_task",
        agent=title_generator_agent,
        description=DESCRIPTION,
        expected_output=EXPECTED_OUTPUT,
        max_retries=10
    )
