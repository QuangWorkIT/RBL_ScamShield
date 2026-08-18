#!/usr/bin/env python3
"""
OpenAlex Academic Paper Crawler for Systematic Literature Reviews (SLR)
Crawls research papers related to AI-powered scam, spam, and fraud detection for SMS and Calls.
"""

import os
import sys
import argparse
from typing import Optional, List, Dict, Any
import pandas as pd
import pyalex
from pyalex import Works

DEFAULT_QUERY = '("scam" OR "smishing" OR "vishing") AND ("SMS" OR "call") AND ("machine learning" OR "LLM" OR "AI")'
DEFAULT_START_YEAR = 2019
DEFAULT_END_YEAR = 2026
DEFAULT_OUTPUT_FILE = "01_all_records_openalex.csv"


def setup_openalex_auth(api_key: Optional[str] = None, email: Optional[str] = None) -> None:
    """Configures authentication and polite pool details for OpenAlex API."""
    # 1. API Key priority: CLI argument > Environment Variable > Interactive Prompt
    if not api_key:
        api_key = os.getenv("OPENALEX_API_KEY")

    if not api_key and sys.stdin.isatty():
        try:
            prompt_key = input("Enter OpenAlex API Key (press Enter to skip & use polite pool): ").strip()
            if prompt_key:
                api_key = prompt_key
        except (EOFError, KeyboardInterrupt):
            pass

    if api_key:
        pyalex.config.api_key = api_key
        print("[INFO] OpenAlex API Key configured.")
    else:
        print("[INFO] Running without API Key (using OpenAlex polite pool).")

    # 2. Email configuration for polite pool
    if not email:
        email = os.getenv("OPENALEX_EMAIL")
    if email:
        pyalex.config.email = email
        print(f"[INFO] OpenAlex polite pool email set to: {email}")


def extract_paper_metadata(item: Dict[str, Any]) -> Dict[str, Any]:
    """Extracts required fields (Title, Publication Year, DOI, Citation Count, Abstract) from a work item."""
    title = item.get("title") or item.get("display_name") or ""
    publication_year = item.get("publication_year")
    doi = item.get("doi") or ""
    citation_count = item.get("cited_by_count", 0)

    # Reconstruct plain text abstract from inverted index
    abstract_inv = item.get("abstract_inverted_index")
    if abstract_inv:
        try:
            abstract_text = pyalex.invert_abstract(abstract_inv)
        except Exception:
            abstract_text = ""
    else:
        abstract_text = ""

    return {
        "Title": title,
        "Publication Year": publication_year,
        "DOI (URL)": doi,
        "Citation Count": citation_count,
        "Abstract": abstract_text
    }


def crawl_papers(
    query: str,
    start_year: int,
    end_year: int,
    limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    """Queries OpenAlex for papers matching search criteria and returns metadata dictionaries."""
    year_filter = f"{start_year}-{end_year}"
    print(f"\n[SEARCH] Query: '{query}'")
    print(f"[SEARCH] Publication Year Filter: {year_filter}")

    works_query = Works().filter(publication_year=year_filter).search(query)
    total_count = works_query.count()
    print(f"[SEARCH] Total matching works found in OpenAlex: {total_count:,}")

    target_count = total_count if limit is None else min(total_count, limit)
    print(f"[FETCH] Target papers to retrieve: {target_count:,}\n")

    papers = []
    per_page = 100
    page_pager = works_query.paginate(per_page=per_page)

    fetched = 0
    page_num = 1

    for page in page_pager:
        if not page:
            break

        for item in page:
            paper_data = extract_paper_metadata(item)
            papers.append(paper_data)
            fetched += 1
            if limit and fetched >= limit:
                break

        print(f"  -> Fetched page {page_num} ({fetched}/{target_count} records)")
        page_num += 1

        if limit and fetched >= limit:
            break

    print(f"\n[COMPLETE] Successfully retrieved {len(papers):,} paper records.")
    return papers


def save_to_csv(data: List[Dict[str, Any]], output_filepath: str) -> None:
    """Exports extracted paper records to CSV format."""
    df = pd.DataFrame(data)
    df.to_csv(output_filepath, index=False, encoding="utf-8-sig")
    print(f"[EXPORT] Saved {len(df):,} records to '{output_filepath}'")


def main():
    parser = argparse.ArgumentParser(
        description="Crawl academic papers from OpenAlex for SLR on AI-powered scam/spam/fraud detection."
    )
    parser.add_argument("--api-key", help="OpenAlex API Key (or set OPENALEX_API_KEY environment variable)")
    parser.add_argument("--email", help="User email for OpenAlex polite pool (or set OPENALEX_EMAIL)")
    parser.add_argument("--query", default=DEFAULT_QUERY, help="Search query string")
    parser.add_argument("--start-year", type=int, default=DEFAULT_START_YEAR, help="Start publication year (default: 2019)")
    parser.add_argument("--end-year", type=int, default=DEFAULT_END_YEAR, help="End publication year (default: 2026)")
    parser.add_argument("--limit", type=int, help="Max records to retrieve (omit to fetch all)")
    parser.add_argument("--output", default=DEFAULT_OUTPUT_FILE, help="Output CSV filename (default: 01_all_records_openalex.csv)")

    args = parser.parse_args()

    setup_openalex_auth(api_key=args.api_key, email=args.email)
    papers = crawl_papers(
        query=args.query,
        start_year=args.start_year,
        end_year=args.end_year,
        limit=args.limit
    )

    if papers:
        save_to_csv(papers, args.output)
    else:
        print("[WARN] No papers retrieved.")


if __name__ == "__main__":
    main()
