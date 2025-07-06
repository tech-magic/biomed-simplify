import os
import json
from typing import Any, Tuple

from crewai import Crew, Task, Process
from agentic_ai.llm.llm_utils import get_crew_llm
from agentic_ai.agents.summary_validation_agent import get_summary_validation_agent

DESCRIPTION = """

Use the input JSON object {combined_summary_results}, to validate the **summary** field against the **source_ids** and **references** fields.

Invoke the `summary_validation_tool` as below to validate the **summary**.

Tool: `summary_validation_tool`  
Tool Input: {combined_summary_results} as a JSON string

Respond with a JSON object (representing summary validation results) with the following fields:

```json
{
    "valid": bool,
    "errors": List[]  # List of all validation issues
}
```

"""

CONTEXT_VALIDATION_DESCRIPTION="""

Use the input JSON object {combined_summary_results}, to validate the **summary** field against the **source_ids** and **references** fields.

Inspect for any language that explicitly mentions the existence of 2 documents, such as:
- "Here is a summary of Document A and Document B."
- "Both documents discuss..."

IF there is any indication in the language that the summary was based on 2 documents THEN
    - Mark the `valid` flag in **summary validation results** as false (i.e., invalidate the summary so it has to be redone)
    - Add all problematic phrases to the `errors` list.
ELSE
    - Mark the `valid` flag in **summary validation results** as true
END IF

Respond with a JSON object (representing **summary validation results**) with the following fields:

```json
{
    "valid": bool,
    "errors": List[]  # List of all validation issues
}
```

"""

EXPECTED_OUTPUT="""

A JSON object with the following fields:

```json
{
    "valid": bool,
    "errors": List[]  # List of all validation issues
}
```

"""

def validate_summary_validation_output(output_str: str) -> Tuple[bool, Any]:
    try:
        data = json.loads(output_str)
        if isinstance(data, dict):
            is_valid = data.get("valid")
            errors = data.get("errors")

            if not isinstance(is_valid, bool):
                return (False, "'valid' field is not found in the JSON object returned as task output")
            
            if not isinstance(errors, list):
                return (False, "'errors' field is not found in the JSON object returned as task output")

            return (True, "Validation passed")

        return (False, "The generated summary validation is not a properly formatted JSON Object")
    except json.JSONDecodeError:
        return (False, "The generated summary validation is not a properly formatted JSON Object")

def get_summary_validation_task(summary_validation_agent):
    return Task(
        name="summary_validation_task",
        agent=summary_validation_agent,
        description=DESCRIPTION,
        expected_output=EXPECTED_OUTPUT,
        output_format="JSON",
        max_retries=10,
        output_validation=validate_summary_validation_output
    )

def get_summary_context_validation_task(summary_validation_agent):
    return Task(
        name="summary_context_validation_task",
        agent=summary_validation_agent,
        description=CONTEXT_VALIDATION_DESCRIPTION,
        expected_output=EXPECTED_OUTPUT,
        output_format="JSON",
        max_retries=10,
        output_validation=validate_summary_validation_output
    )
    
def validate_combined_summary(output_str: str) -> Tuple[bool, Any]:
    try:
        data = json.loads(output_str)
        if isinstance(data, dict):
            summary_validation_agent = get_summary_validation_agent()
            summary_validation_task = get_summary_validation_task(summary_validation_agent)

            summary_validation_crew = Crew(
                agents=[summary_validation_agent],
                tasks=[summary_validation_task],
                process=Process.sequential,
                manager_llm=get_crew_llm()
            )

            result = summary_validation_crew.kickoff(inputs={
                    "combined_summary_results": data
                }
            )

            try:
                data = json.loads(result.output)
                if isinstance(data, dict):
                    is_valid = data.get("valid")
                    errors = data.get("errors")

                    if not isinstance(is_valid, bool):
                        return (False, "'valid' field is not found in the JSON object returned as task output")
                    
                    if not isinstance(errors, list):
                        return (False, "'errors' field is not found in the JSON object returned as task output")
                    
                    if is_valid:

                        summary_context_validation_task = get_summary_context_validation_task(summary_validation_agent)

                        summary_context_validation_crew = Crew(
                            agents=[summary_validation_agent],
                            tasks=[summary_context_validation_task],
                            process=Process.sequential,
                            manager_llm=get_crew_llm()
                        )

                        context_validation_result = summary_context_validation_crew.kickoff(inputs={
                                "combined_summary_results": data
                            }
                        )

                        return (True, "Validation passed")
                    else:
                        return (False, os.linesep.join(errors))

                return (False, "The generated summary validation is not a properly formatted JSON Object")
            except json.JSONDecodeError:
                return (False, "The generated summary validation is not a properly formatted JSON Object")

        return (False, "The generated summary is not a properly formatted JSON Object")
    except json.JSONDecodeError:
        return (False, "The generated summary is not a properly formatted JSON Object")
    

