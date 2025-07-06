import os
import json

from typing import List, Dict, Any

from crewai import Task, Crew, Process

from agentic_ai.llm.llm_utils import get_crew_llm
from agentic_ai.tasks.summary_validation_task import validate_combined_summary

COMBINED_SUMMARY_PROMPT= """

You are an intelligent assistant specializing in research paper summarization.

## Instructions

- Below are two summaries, one from **Document A** and another from **Document B**.
- Your task is to write a single, coherent summary that integrates the key insights from both documents.
- Cite **every** `source_id` from the **Sources List** **at least once**, placing each citation appropriately **within or between** summary sentences using this format: `[source_id]`.
- Use the **References** section to understand the context of each `source_id`, so you can cite them in the most relevant parts of the summary.
- **Do not merge or alter** `source_id`s — each citation must preserve its original `source_id`.

### Output Format

Return your output as a JSON object with the following fields:

```json
{
  "summary": "The complete combined summary as plain text, with all source_ids cited using the format: [source_id].",
  "source_ids": [1, 2, 3],
  "references": [
    "1. [citation information for source_id 1]",
    "2. [citation information for source_id 2]",
    "3. [citation information for source_id 3]"
  ]
}
```

## Validation Rules
- Each `source_id` in the **Sources List** must appear **at least once** in the summary.
- Avoid any language that explicitly mentions the existence of two documents.
    - Do not write: "Here is a summary of Document A and Document B."
    - Do not write: "Both documents discuss..."

---

### Sources List:
{source_ids}

---

### **Document A**:

## summary:
{summary_a}

---

### **Document B**:

## summary:
{summary_b}

---

### **References**

{references}

"""

SUMMARY_OUTPUT="""

A JSON object with the following fields:

```json
{
  "summary": "The complete combined summary as plain text, with all source_ids cited using the format: [source_id].",
  "source_ids": [1, 2, 3],
  "references": [
    "1. [citation information for source_id 1]",
    "2. [citation information for source_id 2]",
    "3. [citation information for source_id 3]"
  ]
}
```

"""

DESCRIPTION="""

Use the JSON array provided by {plain_english_explainer_task.output}, which contains a list of publications.

Your task is to **recursively synthesize all summaries** from each publication into a single, well-structured **final summary**, ensuring **equal contribution** from every publication.

The **final summary** must include **in-text citations** referencing the `id` of each publication:
- Every `id` must be included **at least once** within the body of the summary (i.e., integrated within the sentences—not as footnotes or appendices).
- Citation format: [id].

Use the **citation information associated with each publication’s** `source_id` to determine the **most contextually appropriate** placement for each citation within the summary.

Maintain clarity, logical flow, and a balanced representation of all sources throughout the final summary.

"""

class RecursiveSummarizerTask(Task):
    def __init__(self, recursive_summarizer_agent):
        super().__init__(
            name="recursive_summarizer_task",
            agent=recursive_summarizer_agent,
            description=DESCRIPTION,
            expected_output=SUMMARY_OUTPUT
        )

    def generate_combined_summary(self, a: Dict, b: Dict) -> Dict:

        source_ids = a["source_ids"] + b["source_ids"]
        formatted_source_ids = ", ".join(source_ids)
        references = os.linesep.join(a["references"] + b["references"])
        summary_a=a["summary"]
        summary_b=b["summary"]

        combined_summary_task = Task(
            agent=self.agent,
            description=COMBINED_SUMMARY_PROMPT,
            expected_output=SUMMARY_OUTPUT,
            output_format="JSON",
            verbose=True,
            max_retries=10,
            output_validation=validate_combined_summary
        )

        combined_summary_crew = Crew(
            agents=[self.agent],
            tasks=[combined_summary_task],
            process=Process.sequential,
            manager_llm=get_crew_llm()
        )

        result = combined_summary_crew.kickoff(inputs={
                "source_ids": formatted_source_ids,
                "summary_a": summary_a,
                "summary_b": summary_b,
                "references": references
            }
        )

        return result.output

    def execute(self, inputs: Dict[str, Any] = None, context: Dict[str, Any] = None) -> List[Dict]:

        if not context or "plain_english_explainer_task.output" not in context:
            raise ValueError("Missing plain_english_summary_results in context.")

        try:
            publications = json.loads(context["plain_english_explainer_task.output"])
        except Exception as e:
            raise ValueError(f"Invalid publication_results JSON: {e}")
        
        docs = [{"summary":s["abstract"], "source_ids": [s["id"]], "references": [s["citation"]]} for s in publications]
        while len(docs) > 1:
            new_docs = []
            for i in range(0, len(docs), 2):
                if i + 1 < len(docs):
                    merged = self.generate_combined_summary(docs[i], docs[i + 1])
                    new_docs.append(merged)
                else:
                    new_docs.append(docs[i])
            docs = new_docs
        return docs[0]
    
def get_recursive_summarizer_task(recursive_summarizer_agent):
    return RecursiveSummarizerTask(recursive_summarizer_agent)
