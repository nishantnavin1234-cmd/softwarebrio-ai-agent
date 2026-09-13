from scraper.browser import fetch_page
from scraper.content import clean_text, filter_relevant_links, make_absolute_urls
from scraper.llm import extract_company_intelligence
import sys


def process_domain(domain: str):
    url = f"https://{domain}"

    text, links = fetch_page(url)
    if not text.strip():
        print(f"No content retrieved from {url}")
        return None

    cleaned_text = clean_text(text)

    relevant_links = filter_relevant_links(links, domain)

    absolute_links = make_absolute_urls(relevant_links, url)

    print("Cleaned characters:", len(cleaned_text))
    print("Relevant pages:")

    crawled_pages = {}

    for link in absolute_links:
        print("\nCrawling:", link)

        page_text, _ = fetch_page(link)
        cleaned_page_text = clean_text(page_text)

        crawled_pages[link] = cleaned_page_text[:4000]

        print("Characters:", len(cleaned_page_text))

    combined_context = "\n\n".join(
        f"PAGE: {page_url}\n{text}"
        for page_url, text in crawled_pages.items()
    )

    print("\nFirst page preview:")
    print(list(crawled_pages.values())[0][:500])

    print("\nCombined context characters:", len(combined_context))

    print("\nExtracting company intelligence...")

    result = extract_company_intelligence(combined_context)

    result_data = result.model_dump()

    print("\nCompany Intelligence:")
    print(result.model_dump_json(indent=2))

    return result_data

domains = sys.argv[1:]

if not domains:
    print("Please provide at least one company domain.")
    print("Example: python main.py postman.com supabase.com vapi.ai")
    sys.exit(1)

results = {}

for domain in domains:
    print("\n" + "=" * 60)
    print(f"PROCESSING: {domain}")
    print("=" * 60)

    try:
        results[domain] = process_domain(domain)

    except Exception as e:
        print(f"Failed to process {domain}: {e}")
        results[domain] = None

import json

with open("output.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("\nSaved results to output.json")