import base64
import requests

from crewai import Task

DESCRIPTION="""

You are an expert in generating **Mermaid.js mindmaps** for a given input **summary**.

---

### Instructions:
1. Use the JSON object returned from {recursive_summarizer_task.output}, which contains a **summary** field.
2. The **value** of this **summary** field (described in Instruction #1) is the **summary** for which you must generate a mindmap supported by Mermaid.js
3. Extract key ideas and hierarchical sub-ideas from the provided **summary**.
4. Represent the identified ideas and sub-ideas in **valid Mermaid.js mindmap syntax** adhering with all **syntax rules** described in the **Mermaid.js Mindmap Syntax Guidelines** section.
5. Return only the **validated Mermaid.js Mindmap**.
6. Ensure that:  
    - The **main idea** appears at the center.  
    - **sub-ideas** branch out logically from the root **main idea**, forming a well-structured hierarchy.  
    - The output is **valid Mermaid.js mindmap code**, ready for direct rendering with Mermaid.js. 

---

### Mermaid.js Mindmap Syntax Guidelines:

Following are the **syntax rules** for creating a **valid mermaid.js mindmap**:

1. Start the chart with `mindmap` on its own line. Never include spaces before or after the `mindmap` keyword.
2. Don't use single backticks or triple backticks (` ``` `) anywhere in the diagram syntax.
3. The first node has to be the "root" node in the second line, indented with one tab to the right from the first line, followed by two brackets like:
root((Main Idea))
4. Ideas then  are grouped under each other, where each sub-idea needs right indented with one additional tabs under it's corresponding parent Idea.
5. Except for the starting and ending brackets in the root node, Ideas and sub-ideas should NOT include any hyphens, dashes nor any types of brackets (like curly brackets, brackets, or square brackets).
6. Don't use special characters for Ideas or sub-ideas — for example, write `bioinfo.edu` instead of `bioinfo[.]edu`.
7. Use dashes to add explanations, not extra brackets.
    - Example: write `(Cell signaling - MAPK - pathway)` instead of `(Cell signaling (MAPK) pathway)`.
8. Show gene names (like `TP53`) or protein IDs (like `P01308`) directly, without extra brackets.
9. Don't put a period at the end of a line if it comes right before a closing parenthesis.
10. Do not use emojis or icons.
11. Make sure that there are NO extra spaces at the end of lines.
12. Limit the nodes, the sub-nodes and downwards between 1-10 words.

---

### Mermaid.js Mindmap Example:

Below is a **valid Mermaid.js mindmap** generated about `Gene Expression Analysis` that aheres with **syntax rules** described in the above **Mermaid.js Mindmap Syntax Guidelines** section:

mindmap
  root((Gene Expression Analysis))
    Data Sources
      RNA Sequencing
      Microarrays
      Public Repositories
    Preprocessing
      Quality Control
      Normalization
      Filtering
    Analysis Methods
      Differential Expression
      Clustering
      Dimensionality Reduction
    Applications
      Disease Classification
      Biomarker Discovery
      Drug Response Prediction
    Tools
      DESeq2
      edgeR
      Seurat

---

### Final Validation:

1. If the mindmap lacks structure or clarity, refine the hierarchy to ensure logical flow and balanced branching.
2. Validate the **generated Mermaid.js Mindmap** based on **syntax rules** provided in **Mermaid.js Mindmap Syntax Guidelines** section.
3. If the **generated Mermaid.js Mindmap** needs to be updated based on rule #1 or rule #2 in this section:
    - **Re-generate** a **new Mermaid.js Mindmap** by **re-iterating** back to the **Instructions** section.
4. Output only **valid Mermaid.js Mindmap**:
    - NO extra text
    - NO backticks nor `mermaid` keyword, within the FIRST and LAST lines.

"""

EXPECTED_OUTPUT="""

1. A **valid Mermaid.js mindmap** adhering with the below **Validation Rules**.
2. NO extra text 
3. NO backticks nor `mermaid` keyword, within the FIRST and LAST lines.

---

### Validation Rules:

1. Don't use hyphens, dashes or nested brackets in the text of nodes.
2. Include no more than 5 main branches — these represent the core topics. Add smaller branches for supporting details.
3. Use single parentheses `()` to shape the nodes.
4. Do not use emojis or icons.
5. Make sure there are no extra spaces at the end of lines. Don't use special characters or brackets in the chart labels.
6. Start the chart with `mindmap` on its own line. Don't include spaces before or after the `mindmap` keyword. Don't use triple backticks (` ``` `) to wrap the diagram.
7. Do not include `style root` lines or any comment lines (like ones starting with `#`). The second line should start with `root(...)`.
8. Avoid or escape special characters — for example, write `bioinfo.edu` instead of `bioinfo[.]edu`.
9. Use dashes to add explanations, not extra brackets.
    - Example: write `(Cell signaling - MAPK - pathway)` instead of `(Cell signaling (MAPK) pathway)`.
10. Show gene names (like `TP53`) or protein IDs (like `P01308`) directly, without extra brackets.
11. Don't put a period at the end of a line if it comes right before a closing parenthesis.

"""

def passes_static_validations(mindmap_code) -> tuple[bool, str]:

    # Static validation
    lines = mindmap_code.strip().splitlines()

    # Ensure code starts with 'mindmap'
    if not lines or lines[0].strip() != "mindmap":
        return False, "Missing 'mindmap' as the first line"

    # Ensure a root node exists
    if not any("root((" in line for line in lines):
        return False, "Missing root node with syntax like 'root((Main Topic))'"

    # Ensure no forbidden characters
    if any("```" in line or "[" in line or "]" in line for line in lines):
        return False, "Contains invalid syntax (e.g., triple backticks or square brackets)"

    # Ensure no line has trailing or non-tab leading spaces
    for i, line in enumerate(lines):
        stripped = line.lstrip('\t')  # Remove leading tabs
        if stripped != stripped.strip():
            return False, f"Line {i+1} has invalid leading/trailing spaces (only tabs allowed for indentation)"

    return True, "Valid mindmap syntax"

def validate_mindmap_output(mindmap_code: str) -> tuple[bool, str]:
    """
    Validates a Mermaid.js mindmap diagram by attempting to render it via mermaid.ink.
    If the external service is down, it falls back to basic syntax validation rules.
    """

    static_validation_results = passes_static_validations(mindmap_code)
    if not static_validation_results[0]:
        return static_validation_results

    try:
        # Encode the Mermaid code to base64url format
        b64_code = base64.urlsafe_b64encode(mindmap_code.encode('utf-8')).decode('utf-8')
        url = f"https://mermaid.ink/img/{b64_code}"
        resp = requests.get(url, timeout=10)

        if resp.status_code == 200 and resp.headers.get("Content-Type", "").startswith("image/"):
            return True, "Valid Mermaid.js mindmap"
        else:
            return False, f"Mermaid.ink rejected the mindmap. Status: {resp.status_code}"

    except Exception as e:
        return True, "Validated with fallback rules (mermaid.ink unreachable)"

def get_mindmap_generator_task(mindmap_generator_agent):
    return Task(
        name="mindmap_generator_task",
        agent=mindmap_generator_agent,
        description=DESCRIPTION,
        expected_output=EXPECTED_OUTPUT,
        output_format="text",
        max_retries=10,
        output_validation=validate_mindmap_output
    )

