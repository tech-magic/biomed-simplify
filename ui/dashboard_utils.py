INTRODUCTION = f"""
<div style="background-color: #f9f9f9; padding: 20px; border-radius: 12px;">

#### 🧬🧪 Understand Biomedical Research in Plain English

With the **PubMed** database hosted by [NCBI](https://pubmed.ncbi.nlm.nih.gov/), you can search a vast collection of **biomedical literature**.

🚀 Try **BioMedSimplify** – our intelligent system powered by **AgenticAI** and cutting-edge **LLMs**!

It helps you effortlessly navigate the **latest publications** on any topic by:

- 📝 Generating **simplified summaries** with citations in **layman’s terms**
- 🧠 Creating **visual mindmaps**

</div>
"""

SEARCH_INSTRUCTIONS = """

### 💡 **Curious where to begin?**

Try these sample queries and watch BioMedSimplify turn complex research into clear insights and visuals:

- 🧬 `BRCA1`
- 💊 `diabetes OR metformin`
- 🦠 `COVID`

"""

SEARCH_MANUAL = """
##### 🔍 What You Can Search in PubMed

You can search by any field that PubMed indexes, such as:

1. **Keywords / Terms**  
   General keywords related to biomedical topics (e.g., *cancer*, *metformin*, *gene therapy*)

2. **Author Information**  
   Search by author's last name, optionally with initials  
   → `"Smith J"[Author]`

3. **Article Titles**  
   Words or phrases in the article title  
   → `"CRISPR gene editing"[Title]`

4. **Abstract Content**  
   Words or phrases found in abstracts  
   → `"insulin resistance"[Abstract]`

5. **Publication Types**  
   Such as review articles, clinical trials, case reports  
   → `"review"[Publication Type]`

6. **Journal Names**  
   Search articles in specific journals  
   → `"Nature Genetics"[Journal]`

7. **Publication Dates**  
   Specific dates or date ranges  
   → `"2020/01/01"[Date - Publication] : "2022/12/31"[Date - Publication]`

8. **MeSH Terms (Medical Subject Headings)**  
   Controlled vocabulary for biomedical concepts  
   → `"Diabetes Mellitus, Type 2"[MeSH Terms]`

9. **PMID (PubMed ID)**  
   Unique identifier(s) for articles  
   → `34567890[PMID]`

10. **DOI (Digital Object Identifier)**  
    Some articles include DOIs in metadata  
    → `"10.1001/jama.2020.1585"[DOI]`

11. **Grant Numbers / Funding**  
    Example: `"R01 CA123456"[Grant Number]`

12. **Affiliation**  
    Institutional or university affiliation  
    → `"Harvard University"[Affiliation]`

13. **Language**  
    Example: `"english"[Language]`

14. **Study Subjects**  
    Search by organisms (e.g., `"human"[Organism]`, `"mouse"[Organism]`)

##### 📌 Tip: Combine Fields with Boolean Operators

You can use:
- AND, OR, NOT
- Field tags like [Title], [Author], [Affiliation], [Journal], etc.
"""


def fetch_introduction():
    return INTRODUCTION

def fetch_search_instructions():
    return SEARCH_INSTRUCTIONS

def fetch_search_manual():
    return SEARCH_MANUAL