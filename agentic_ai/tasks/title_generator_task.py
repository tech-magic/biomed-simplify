from crewai import Task
from llm.llm_utils import get_prompt_template, get_direct_answer

class TitleGeneratorTask(Task):
    def __init__(self, summary):
        self.summary = summary
        super().__init__(
            description="Generate a title from the final article summary.",
            expected_output="A single title string."
        )

    def execute(self, agent):
        prompt = get_prompt_template("prompts/main_title.prompt").format(article=self.summary)
        return get_direct_answer(prompt)
