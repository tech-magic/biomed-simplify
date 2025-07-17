import os

from ui.utils.mermaid_mindmap_renderer import mindmap_to_html 

SUMMARY_REPORT_HEADER = """
#### Latest findings for 👉 🧭 **{input_query}** 🧭

# {report_title}

"""

SUMMARY_REPORT_BODY = """

{contents}

---

### References
{references}

---

### Mindmap

"""

def render_summary_report_header(input_query, report_title):
    return SUMMARY_REPORT_HEADER.format(
        input_query=input_query,
        report_title=report_title
    )

def render_summary_report_body(contents, references):
    return SUMMARY_REPORT_BODY.format(
        contents=contents,
        references=references
    )

def build_report(st, st_html, input_query, agentic_ai_results):

    report_title = agentic_ai_results["title"]
    report_header = render_summary_report_header(input_query, report_title)
    st.markdown(report_header, unsafe_allow_html=True)

    report_contents = agentic_ai_results["contents"]
    report_references = os.linesep.join(agentic_ai_results["references"])
    report_body = render_summary_report_body(report_contents, report_references)

    print("--- Final Report Body ---")
    print(f"{report_body}")

    st.markdown(report_body, unsafe_allow_html=True)

    mindmap_code = agentic_ai_results["mindmap"]
    mindmap_html = mindmap_to_html(mindmap_code)

    st_html(mindmap_html, height=800)




