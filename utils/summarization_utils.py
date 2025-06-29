from typing import List, Dict

from llm.llm_utils import get_prompt_template, get_direct_answer

# === Recursive summarization ===
def generate_combined_summary(a: Dict, b: Dict) -> Dict:
    prompt = get_prompt_template("prompts/combined_summary.prompt").format(
        ids_a=", ".join(a["source_ids"]),
        summary_a=a["summary"],
        ids_b=", ".join(b["source_ids"]),
        summary_b=b["summary"]
    )
    summary = get_direct_answer(prompt)
    return {
        "summary": summary,
        "source_ids": a["source_ids"] + b["source_ids"]
    }

def recursive_summarize(docs: List[Dict]) -> Dict:
    while len(docs) > 1:
        new_docs = []
        for i in range(0, len(docs), 2):
            if i + 1 < len(docs):
                merged = generate_combined_summary(docs[i], docs[i + 1])
                new_docs.append(merged)
            else:
                new_docs.append(docs[i])  # Pass lone summary up
        docs = new_docs
    return docs[0]

# === Title generator ===
def generate_title(article: str) -> str:
    prompt = get_prompt_template("prompts/main_title.prompt").format(article=article)
    return get_direct_answer(prompt)

# === Layman summary generator ===
def generate_layman_summary(summary: str) -> str:
    prompt = get_prompt_template("prompts/plain_summary.prompt").format(abstract=summary)
    return get_direct_answer(prompt)

# === Run the full pipeline ===
def build_article(publications: List[Dict]):
    # Add source_ids to each input summary
    docs = [{"summary": generate_layman_summary(s["abstract"]), "source_ids": [s["id"]]} for s in publications]
    final = recursive_summarize(docs)
    title = generate_title(final["summary"])
    return title, final["summary"]