# SERP Analysis Tool with Google Custom Search API

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

A Python-based Search Engine Results Page (SERP) analysis tool that leverages the Google Custom Search JSON API to fetch and analyze web content for specialized research domains. Developed as a course project in my third year.

## Core Technologies:
  - Python (3.8 +)
  - Google Custom Search JSON API
  - Matplotlib (for visualisation)
  - Concurrent execution via `ThreadPoolExecutor`

## Key Features

- **Multi-mode Search Capability**:
  - General web search
  - Crime reporting papers analysis
  - Deep learning journal papers analysis

- **Structured Data Extraction**:
  - Identifies 100+ crime-reporting features (incident details, victim info, evidence, etc.)
  - Detects academic paper sub-headings in deep learning publications

- **Visual Analytics**:
  - Automated bar chart generation for feature frequency analysis
  - Threaded processing for concurrent data extraction/visualization

## Usage

1. **Configure API**:
   - Replace placeholder credentials in `utils.py`:
     
     ```python
     API_KEY = "your_google_api_key"
     SEARCH_ENGINE_ID = "your_search_engine_id"
     ```

2. **Run the program**:
   ```bash
   python main.py
   ```

3. **Select analysis mode:**
   - General search
   - Crime reporting analysis
   - Deep learning paper analysis
  
## Usage Examples

**Crime-Reporting Mode:**

```bash
Copy
> Select mode: 2
> Query: "homicide investigation techniques 2023"

Analyzing 10 results...
- Extracted 23 incident_details features
- Found 8 weapon/evidence references
- Generated visualization: crime_features.png
```
