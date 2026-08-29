# PRISMA 2020 Flow Diagram - Master Synthesis (ScamShield RBL)

```mermaid
flowchart TD
    subgraph Identification
        A["Records identified from academic databases<br/>(ArXiv, OpenAlex, Semantic Scholar, CrossRef, Google Scholar)<br/><b>Total raw records: N = 1727</b>"]
        B["Records removed before screening:<br/>Duplicate records across team: <b>N = 176</b>"]
        A --> B
        C["Unique records for title/abstract screening<br/><b>N = 1551</b>"]
        B --> C
    end

    subgraph Screening
        D["Records excluded during Title/Abstract screening<br/>(Out of domain, non-scam, theoretical only)<br/><b>N = 1509</b>"]
        C --> D
        E["Reports sought for retrieval & full-text assessment<br/><b>N = 44 candidate reports</b>"]
        C --> E
    end

    subgraph Eligibility
        F["Reports excluded due to cross-member duplication:<br/><b>N = 2 duplicate papers</b>"]
        E --> F
        G["Assessed for eligibility under PICO + IC/EC criteria<br/><b>N = 42 full reports</b>"]
        E --> G
    end

    subgraph Included
        H["Final Master Included Studies in Systematic Review<br/>& 7-Column Evidence Extraction Matrix<br/><b>N = 42 Unique Papers</b>"]
        G --> H
    end
```

### PRISMA Flow Synthesis Statistics:
1. **Total Records Identified (Identification Phase):** `1727` records across 5 researchers.
2. **Unique Records Screened (Screening Phase):** `1551` records after global deduplication.
3. **Cross-Member Candidate Papers Assessed:** `44` candidate papers.
4. **Final Unique Studies Included in Master Matrix:** `42` peer-reviewed empirical studies.
