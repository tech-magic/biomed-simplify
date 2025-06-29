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
    
def ieee_citation(record):
    authors = record.get('AU', [])
    if len(authors) > 3:
        authors_text = f"{authors[0]} et al."
    else:
        authors_text = ', '.join(authors)
    title = record.get('TI', 'No Title')
    journal = record.get('JT', 'No Journal')
    year = record.get('DP', 'n.d.').split(" ")[0]
    return f"{authors_text}, {title}, {journal}, {year}."

def fetch_pubmed_publications(query, email=ENTREZ_EMAIL, max_results=10):

    Entrez.email = email
    # Search PubMed with the query, sorted by publication date descending
    search_handle = Entrez.esearch(
        db="pubmed",
        term=query,
        sort="pub date",    # Sort by most recent
        retmax=max_results
    )
    search_results = Entrez.read(search_handle)
    search_handle.close()

    # Extract the list of PubMed IDs
    id_list = search_results["IdList"]

    # Fetch citation and abstract details for the found PubMed IDs
    fetch_handle = Entrez.efetch(
        db="pubmed",
        id=",".join(id_list),
        rettype="medline",
        retmode="text"
    )
    records = list(Medline.parse(fetch_handle))
    fetch_handle.close()

    return [
        {
            "id": str(record.get("PMID", "Unknown")),
            "citation": ieee_citation(record),
            "abstract": record.get('AB', 'No abstract available.')
        }
        for record in sorted(records, key=lambda r: int(r.get("PMID", 0)))
    ]
