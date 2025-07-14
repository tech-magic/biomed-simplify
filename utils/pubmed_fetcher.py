from Bio import Entrez, Medline

from config.email_config import ENTREZ_EMAIL

def get_corrected_query(query, email=ENTREZ_EMAIL):
    Entrez.email = email
    try:
        with Entrez.espell(term=query) as handle:
            record = Entrez.read(handle)

        original = record.get("Query", "[No Query Returned]")
        corrected = record.get("CorrectedQuery")

        print("Original Query:", original)

        if corrected and isinstance(corrected, str) and corrected.lower() != 'no correction suggested':
            print("Corrected Query:", corrected)
            return corrected

        
        return query

    except Exception as e:
        print("❌ Error:", e)
        return query
    
def build_citation(record, i):
    authors = record.get('AU', [])
    if len(authors) > 3:
        authors_text = f"{authors[0]} et al."
    else:
        authors_text = ', '.join(authors)
    title = record.get('TI', 'No Title')
    journal = record.get('JT', 'No Journal')
    year = record.get('DP', 'n.d.').split(" ")[0]
    return f"[{i}]. {authors_text}, {title}, {journal}, {year}."

from typing import List, Dict
from Bio import Entrez, Medline

ENTREZ_EMAIL = "your.email@example.com"   # set once and reuse


def _search_pubmed_ids(query: str, email: str, retstart: int, retmax: int) -> List[str]:
    """Return ≤ retmax PubMed IDs starting at offset `retstart`."""
    Entrez.email = email
    with Entrez.esearch(
        db="pubmed",
        term=query,
        sort="pub date",
        retstart=retstart,
        retmax=retmax,
    ) as handle:
        result = Entrez.read(handle)
    return result["IdList"]


def _fetch_medline_records(id_list: List[str]) -> List[Dict]:
    """Fetch MEDLINE records for the given PubMed IDs."""
    if not id_list:
        return []
    with Entrez.efetch(
        db="pubmed",
        id=",".join(id_list),
        rettype="medline",
        retmode="text",
    ) as handle:
        return list(Medline.parse(handle))


def fetch_pubmed_publications(
    query: str,
    email: str = ENTREZ_EMAIL,
    max_results: int = 10,
) -> List[Dict]:
    """
    Get up to `max_results` PubMed records **that have abstracts**.
    Each paging request also asks for `max_results` IDs, so the
    batch‑size == max_results invariant is always satisfied.
    """
    gathered: List[Dict] = []
    retstart = 0  # offset for the next esearch call

    while len(gathered) < max_results:
        # Request the next "page" – same size as max_results
        id_list = _search_pubmed_ids(query, email, retstart, max_results)
        if not id_list:  # no more results
            break

        for record in _fetch_medline_records(id_list):
            abstract = record.get("AB", "").strip()
            if not abstract:
                continue  # skip papers without abstracts

            gathered.append(
                {
                    "id": str(len(gathered) + 1),
                    "pmid": record.get("PMID", "Unknown"),
                    "citation": build_citation(record, str(len(gathered) + 1)),
                    "abstract": abstract,
                }
            )
            if len(gathered) >= max_results:
                break

        retstart += max_results  # move offset by one full "page"

    return gathered  # may be < max_results if PubMed runs out

