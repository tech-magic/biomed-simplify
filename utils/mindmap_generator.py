import uuid
from llm.llm_utils import get_answer_from_llm 

system_prompt = """
You are creating a Mermaid.js mindmap in English to help a bioscience student understand key ideas from a text. 
The goal is to clearly organize the main points and supporting details. Follow these instructions:

1. Don’t use hyphens or nested brackets in the text of nodes — use dashes or rewrite to make it clearer.
2. Include no more than 5 main branches — these represent the core topics. Add smaller branches for supporting details.
3. Use single parentheses `()` to shape the nodes.
4. Do not use emojis or icons.
5. Make sure there are no extra spaces at the end of lines. Don’t use special characters or brackets in the chart labels.
6. Start the chart with `mindmap` on its own line. Don’t use triple backticks (` ``` `) to wrap the diagram.
7. Do not include `style root` lines or any comment lines (like ones starting with `#`). The second line should start with `root(...)`.
8. Avoid or escape special characters — for example, write `bioinfo.edu` instead of `bioinfo[.]edu`.
9. Use dashes to add explanations, not extra brackets.
10. Example: write `(Cell signaling - MAPK - pathway)` instead of `(Cell signaling (MAPK) pathway)`.
11. Show gene names (like `TP53`) or protein IDs (like `P01308`) directly, without extra brackets.
12. Don’t put a period at the end of a line if it comes right before a closing parenthesis.
"""

################################################################
### mindmap
################################################################

def generate_mindmap_prompt(input_text):
    return f"""
### Task:
You are an advanced AI model specializing in structured knowledge representation.
Your goal is to create a Mermaid.js mindmap in English that captures the essential ideas, subtopics, and relationships based on a provided **Input Text**.

### Instructions:
- Extract key concepts and hierarchical relationships from the provided **Input Text**.
- Represent the identified key concepts and relationships in **Mermaid.js mindmap syntax** aligned with a structure similar to the example provided under **References**.
- Avoid any explanations or extra text.
— Return only the **Mermaid.js code**.

### Context:
Generate a mind map in **Mermaid.js syntax** based on the provided **Input Text**. The output must strictly adhere to **Mermaid.js mindmap syntax** and should effectively capture key concepts and their relationships.  
Ensure that:  
1. The **main topic** appears at the center.  
2. **Subtopics** branch out logically, forming a well-structured hierarchy.  
3. The output is **valid Mermaid.js code**, ready for direct rendering. 

### References:  
Follow the below example mindmap based on **Mermaid.js syntax** as a reference:  

mindmap
  root((Main Topic))
    Subtopic A
      Detail A1
      Detail A2
    Subtopic B
      Detail B1
      Detail B2

### Iterate & Evaluate:
If the mind map lacks structure or clarity, refine the hierarchy to ensure logical flow and balanced branching. Validate that the **Mermaid.js syntax** is correct.
**Output only **valid Mermaid.js code** — no extra text.

### Input Text:
{input_text}

"""

def mindmap_to_html(mindmap_code):
    html_code = f"""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css">
    <div class="mermaid">{mindmap_code}</div>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>mermaid.initialize({{startOnLoad:true}});</script>
    """
    return html_code

def render_mindmap(input_text):
    mindmap = get_answer_from_llm(system_prompt, generate_mindmap_prompt(input_text))
    return mindmap_to_html(mindmap)

