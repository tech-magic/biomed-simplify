# 🧬 BioMedSimplify

**BioMedSimplify** is an LLM-powered agentic workflow designed to **automate and simplify biomedical literature analysis**. It extracts, rewrites, summarizes, and visualizes insights from the latest publications on a given biomedical topic—generating a researcher-friendly Markdown report complete with citations and a visual mind map.

---

## 🌟 Features

✅ Search recent biomedical publications from NCBI  
✅ Translate technical abstracts to **plain English**  
✅ Recursively summarize multiple papers into one **coherent summary**  
✅ Validate that every paper is cited at least once in the summary  
✅ Generate a **title** and a **MermaidJS mind map**  
✅ Output a polished **Markdown report**  
✅ Built with **Streamlit UI**  
✅ Works with **Ollama**, **OpenAI**, **Azure**, or any OpenAI-compatible LLM  

---

## 🧪 Agentic Workflow (CrewAI)

| Step | Agent | Task | Description |
|------|-------|------|-------------|
| 🔍 Search & Fetch | `publication_fetcher_agent` | `publication_fetcher_task` | Query NCBI via BioPython Entrez for latest publications |
| ✏️ Plain-English Rewrite | `plain_english_explainer_agent` | `plain_english_explainer_task` | Rewrites abstracts into simple language |
| 🧬 Recursive Summary | `recursive_summarizer_agent` | `recursive_summarizer_task` | Builds a coherent summary using simplified abstracts |
| ✅ Validation | `summary_validation_agent` | `summary_validation_task` | Ensures coherence and that all papers are cited |
| 🧠 Title Generator | `title_generator_agent` | `title_generator_task` | Suggests the best possible title |
| 🗺️ Mind Map Generator | `mindmap_generator_agent` | `mindmap_generator_task` | Generates a MermaidJS mind map of concepts |

---

## 📄 Output Structure

The output Markdown report includes:

1. **Generated Title**
2. **MermaidJS Mind Map**
3. **Summary with In-text Citations**
4. **References with Metadata**

---

## 🧠 Use Cases

- **Students**: Understand research in simpler terms  
- **Researchers**: Rapid literature reviews  
- **Educators**: Turn complex papers into teachable content  
- **Funding Bodies**: Summarize research proposals quickly  
- **Knowledge Systems**: Feed structured summaries into graphs/databases  

---

## 📸 UI Screenshot

> (You can insert a Streamlit screenshot or GIF demo here)

---

## 🖥️ Run Locally with Ollama

This project has been tested with **Ollama** running locally using `llama3.2:latest`.

### 🔧 Ollama Setup

1. **Install Ollama** from the [Ollama website](https://ollama.com)
2. During installation, **set Ollama to run as a service**, or launch it manually:
   ```bash
   ollama serve
    ```
3. 