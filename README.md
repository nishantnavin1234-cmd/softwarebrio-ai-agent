# SoftwareBrio AI Lead Enrichment Agent

A Python-based AI lead enrichment pipeline that crawls public company websites, discovers relevant pages, extracts useful content, and uses an LLM to generate structured company intelligence.

## Objective

The agent accepts one or more company domains and processes each company independently.

For every domain, it:

1. Retrieves the company homepage using Playwright.
2. Discovers relevant internal pages such as About, Company, Team, Contact, Careers, and Pricing pages.
3. Uses a custom multi-step browsing agent to prioritize and crawl useful pages.
4. Cleans the extracted webpage text before sending it to the LLM.
5. Combines the most relevant content into a bounded context.
6. Uses Groq and an OpenAI GPT-OSS model to extract structured company intelligence.
7. Validates the LLM response using Pydantic.
8. Optionally enriches team members with public LinkedIn profile URLs using Tavily search.
9. Records token usage and estimated LLM API cost.
10. Saves the final results to `output.json`.

## Extracted Intelligence

The pipeline extracts:

- Company overview
- Target audience / Ideal Customer Profile (ICP)
- Public generic contact emails
- Key leadership / team members
- Team member roles
- LinkedIn URLs when discoverable
- Confidence score from 0 to 1
- LLM token usage
- Estimated API cost

## Architecture

```text
Company domains
      |
      v
   main.py
      |
      v
Homepage retrieval
      |
      v
Internal link discovery
      |
      v
Custom multi-step browsing agent
      |
      v
Relevant page crawling
      |
      v
Text cleaning
      |
      v
Context preparation
      |
      v
LLM structured extraction
      |
      v
Pydantic validation
      |
      v
LinkedIn enrichment
      |
      v
Usage + cost tracking
      |
      v
   output.json