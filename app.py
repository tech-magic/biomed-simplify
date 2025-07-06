import streamlit as st
from streamlit.components.v1 import html as st_html # Alias to avoid conflict

from ui.dashboard_utils import fetch_introduction, fetch_search_manual, fetch_search_instructions

from utils.pubmed_fetcher import fetch_pubmed_publications, get_corrected_query
from utils.summarization_utils import build_article
from utils.mindmap_generator import render_mindmap

from agentic_ai.main_workflow import trigger_agentic_ai_workflow

# Initialize a session state
if 'mindmap_content' not in st.session_state:
    st.session_state.mindmap_content = ""

st.set_page_config(
    page_title="BioMedSimplify",  # Tab title
    page_icon="🔬",                  # Tab icon (favicon)
    layout="wide",                  # Optional: "centered" or "wide"
)

st.markdown(
    """
    <h1 style='text-align: center;'>
        🔬 BioMedSimplify
    </h1>
    """,
    unsafe_allow_html=True
)

with st.expander("🛠️ Help Center: Intro & Tips", expanded=True):
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(fetch_introduction(), unsafe_allow_html=True)
    with col2:
        st.markdown(fetch_search_instructions())
        with st.expander("📘 *Expand for more search options and examples!*"):
            st.markdown(fetch_search_manual())

st.markdown("---")

col_search_1, col_search_2, col_search_3 = st.columns([2, 1, 1])
with col_search_1:
    query = st.text_input(
        "🔍 What health topic, drug, or condition do you want to understand better?",
        placeholder="e.g., BRCA1, diabetes, metformin, COVID, CRISPR",
        help="ℹ️ e.g., BRCA1, diabetes, metformin, COVID, CRISPR"
    )
with col_search_3:
    num_pubs = st.slider(
        "📚 Latest publication count:",
        min_value=5,
        max_value=25,
        step=5,
        value=10,
        help="ℹ️ How many recent publications should we fetch? More publications may take longer to summarize and visualize."
    )

if query:
    corrected_query = get_corrected_query(query)
    with st.spinner(f"Searching latest BioMedical insights for: {corrected_query}"):
        publications = fetch_pubmed_publications(corrected_query, max_results=num_pubs)
        trigger_agentic_ai_workflow(corrected_query, num_pubs)
        with st.spinner(f"Generating Summary"):
            title, contents = build_article(publications)

            citation_list = "\n".join(
                [f"{i+1}. {pub['citation']}" for i, pub in enumerate(publications)]
            )

            markdown_content = f"""
# Latest findings for **{corrected_query}**

## {title}

{contents}

#### References
{citation_list}
            """

            print(markdown_content)

            st.markdown(markdown_content, unsafe_allow_html=True)

            with st.spinner(f"Generating Mindmap"):
                latest_mindmap = render_mindmap(contents)
                print(latest_mindmap)
                st.session_state.mindmap_content = latest_mindmap
                st_html(st.session_state.mindmap_content, height=800)

