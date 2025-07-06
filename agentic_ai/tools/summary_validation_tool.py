import json
import re
from typing import Any, List
from crewai.tools import tool

@tool("summary_validation_tool")
def summary_validation_tool(tool_input: str) -> Any:
    """
    Validates a combined research summary JSON for structure and citation rules.

    Args:
        tool_input (str): A JSON string with:
            - "summary" (str): The combined textual summary.
            - "source_ids" (List[int]): List of source IDs that must be cited.
            - "references" (List[str]): Reference entries corresponding to each source ID.

    Returns:
        dict: {
            "valid": bool,
            "errors": List[str]  # List of all validation issues
        }
    """
    errors: List[str] = []

    try:
        data = json.loads(tool_input)

        if not isinstance(data, dict):
            return {"valid": False, "errors": ["The input is not a valid JSON object."]}

        summary = data.get("summary")
        source_ids = data.get("source_ids")
        references = data.get("references")

        # Validate 'summary'
        if not isinstance(summary, str) or not summary.strip():
            errors.append("'summary' must be a non-empty string.")

        # Validate 'source_ids'
        if not isinstance(source_ids, list):
            errors.append("'source_ids' must be a list.")
        elif not source_ids:
            errors.append("'source_ids' must not be empty.")
        elif not all(isinstance(i, int) for i in source_ids):
            errors.append("'source_ids' must only contain integers.")

        # Validate 'references'
        if not isinstance(references, list):
            errors.append("'references' must be a list.")
        elif 'source_ids' in data and isinstance(source_ids, list) and len(references) != len(source_ids):
            errors.append("'references' count must match 'source_ids' count.")
        else:
            for ref in references or []:
                if not isinstance(ref, str) or not re.match(r"^\d+\.\s", ref):
                    errors.append(f"Invalid reference format: '{ref}'")

        # Citation validations
        if isinstance(summary, str) and isinstance(source_ids, list):
            missing_ids = []
            for sid in source_ids:
                if not re.search(fr"\[{sid}\]", summary):
                    missing_ids.append(sid)
            if missing_ids:
                errors.append(f"Missing citation(s) in summary for source_ids: {missing_ids}")

            citation_matches = re.findall(r"\[(\d+)\]", summary)
            invalid_ids = [int(c) for c in citation_matches if int(c) not in source_ids]
            if invalid_ids:
                errors.append(f"Invalid citations found in summary: {invalid_ids}")

        # Disallowed phrasing
        if isinstance(summary, str):
            disallowed_phrases = [
                "document a", "document b", "both documents",
                "summary of document", "summary of both"
            ]
            lower_summary = summary.lower()
            for phrase in disallowed_phrases:
                if phrase in lower_summary:
                    errors.append(f"Disallowed phrase found in summary: '{phrase}'")

        # Final result
        if errors:
            return {"valid": False, "errors": errors}
        else:
            return {"valid": True, "errors": []}

    except json.JSONDecodeError:
        return {"valid": False, "errors": ["The input is not a properly formatted JSON string."]}
    except Exception as e:
        return {"valid": False, "errors": [f"Unexpected error: {str(e)}"]}
