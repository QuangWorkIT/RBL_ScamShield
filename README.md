# OpenAlex Paper Crawler for SLR

A Python command-line tool designed to query and export academic research papers from the [OpenAlex API](https://openalex.org) for Systematic Literature Reviews (SLR). 

This tool is pre-configured to search for papers on **AI-powered scam, spam, and fraud detection for SMS and Calls**, published from **2019 to 2026**.

---

## 📋 Features

- **Automated OpenAlex Queries**: Queries works using concepts: `("scam" OR "smishing" OR "vishing") AND ("SMS" OR "call") AND ("machine learning" OR "LLM" OR "AI")`.
- **Publication Year Filtering**: Restricts results to papers published between **2019** and **2026** (configurable).
- **Abstract Reconstruction**: Automatically reconstructs full text abstracts from OpenAlex's `abstract_inverted_index`.
- **API Key & Polite Pool Support**: Supports OpenAlex API keys via environment variables, CLI options, or interactive prompt, with fallback to the OpenAlex polite pool.
- **CSV Export**: Saves structured results to `01_all_records_openalex.csv` matching SLR project structures.

---

## 🛠️ Prerequisites & Installation

### Dependencies
- Python 3.8+
- `pyalex`
- `pandas`

### Installation Commands

Using standard `pip`:
```bash
pip install pyalex pandas
```

Or using `uv` package manager:
```bash
uv pip install pyalex pandas
```

---

## 🔑 Authentication (Setting the API Key)

OpenAlex allows requests without an API key (using the free polite pool), but adding an API key unlocks higher rate limits (up to 10 requests/second).

### Method 1: Environment Variable (Recommended)

**On Windows (PowerShell):**
```powershell
$env:OPENALEX_API_KEY="your_openalex_api_key_here"
```

**On Windows (Command Prompt):**
```cmd
set OPENALEX_API_KEY=your_openalex_api_key_here
```

**On Linux / macOS:**
```bash
export OPENALEX_API_KEY="your_openalex_api_key_here"
```

### Method 2: Command-Line Flag
Pass `--api-key` directly when executing the script:
```bash
python crawl_openalex.py --api-key "your_api_key_here"
```

### Method 3: Interactive Prompt
If no API key or environment variable is set, running the script will prompt you:
```
Enter OpenAlex API Key (press Enter to skip & use polite pool):
```
*Note: Pressing Enter will run the crawler in polite pool mode.*

---

## 🚀 Running the Tool

### 1. Sample Run (Test with first 25 records)
```bash
python crawl_openalex.py --limit 25
```

### 2. Full Crawl (Fetch all matching records)
```bash
python crawl_openalex.py
```

### 3. Custom Query or Date Ranges
```bash
python crawl_openalex.py --start-year 2020 --end-year 2026 --limit 100 --output custom_results.csv
```

### 4. Provide Polite Pool Email (Optional Best Practice)
```bash
python crawl_openalex.py --email "your_email@domain.com"
```

---

## 📊 Extracted Data Schema (`01_all_records_openalex.csv`)

| Column Name | Description |
| :--- | :--- |
| `Title` | Paper title or display name |
| `Publication Year` | Year the paper was published |
| `DOI (URL)` | Direct link to the paper via DOI URL |
| `Citation Count` | Number of times the paper has been cited |
| `Abstract` | Reconstructed plain-text abstract |

---

## 📂 Project Structure

```
.
├── crawl_openalex.py           # Main Python crawler script
├── README.md                   # Setup and usage guide
└── 01_all_records_openalex.csv # Generated output CSV file
```
