# SoftwareBrio AI Lead Enrichment Agent

A Python-based autonomous lead enrichment pipeline that crawls company websites, extracts relevant content, and uses an LLM to produce structured company intelligence.

## Objective

The agent accepts one or more company domains, crawls their public web presence using Playwright, discovers relevant internal pages, cleans the extracted content, and uses an LLM to generate structured company intelligence.

The extracted information includes:

- Company overview
- Target audience / Ideal Customer Profile (ICP)
- Public contact emails
- Key leadership / team members
- LinkedIn URLs when discoverable
- Data confidence score

## Architecture

The project follows a modular pipeline:

```text
Company domains
      ↓
main.py
      ↓
Homepage retrieval
      ↓
Relevant internal-page discovery
      ↓
Playwright browser crawling
      ↓
Clean text extraction
      ↓
Context filtering and token limiting
      ↓
LLM structured extraction
      ↓
Pydantic validation
      ↓
output.json