from scraper.browser import fetch_page
from scraper.content import clean_text
from scraper.llm import extract_company_intelligence
from scraper.search import search_linkedin
from scraper.agent import agent_loop

import sys
import json
from urllib.parse import urljoin, urlparse


def is_same_domain(url: str, domain: str) -> bool:
    """
    Return True when the URL belongs to the requested domain
    or one of its legitimate subdomains.
    """

    hostname = urlparse(url).hostname

    if not hostname:
        return False

    hostname = hostname.lower().rstrip(".")
    domain = domain.lower().strip().rstrip(".")

    return (
        hostname == domain
        or hostname.endswith("." + domain)
    )


def process_domain(domain: str):
    url = f"https://{domain}"

    # --------------------------------------------------
    # Step 1: Fetch homepage
    # --------------------------------------------------

    text, links = fetch_page(url)

    if not text.strip():
        print(f"No content retrieved from {url}")
        return None

    cleaned_text = clean_text(text)

    print("Cleaned characters:", len(cleaned_text))

    # --------------------------------------------------
    # Step 2: Prepare links for the agent
    # --------------------------------------------------

    print("\nStarting agentic page discovery...")

    absolute_links = []

    for text_value, href in links:

        if not href:
            continue

        absolute_url = urljoin(url, href)

        if is_same_domain(
            absolute_url,
            domain
        ):
            absolute_links.append(
                (text_value, absolute_url)
            )

    # --------------------------------------------------
    # Step 3: Agentic browsing
    # --------------------------------------------------

    crawled_pages = agent_loop(
        initial_links=absolute_links,
        fetch_function=fetch_page,
        clean_function=clean_text,
        base_url=url,
        max_pages=5
    )

    # --------------------------------------------------
    # Step 4: Add homepage context
    # --------------------------------------------------

    crawled_pages = {
        url: cleaned_text[:4000],
        **crawled_pages
    }

    print("\nPages selected by agent:")

    for page_url in crawled_pages:
        print(page_url)

    # --------------------------------------------------
    # Step 5: Combine context
    # --------------------------------------------------

    combined_context = "\n\n".join(
        f"PAGE: {page_url}\n{text}"
        for page_url, text in crawled_pages.items()
    )

    print(
        "\nCombined context characters:",
        len(combined_context)
    )

    # --------------------------------------------------
    # Step 6: LLM extraction
    # --------------------------------------------------

    print("\nExtracting company intelligence...")

    result, usage_data = extract_company_intelligence(
        combined_context
    )

    # --------------------------------------------------
    # Step 7: Cost tracking
    # --------------------------------------------------

    print("\nLLM Usage:")

    print(
        f"Input tokens: "
        f"{usage_data['input_tokens']}"
    )

    print(
        f"Output tokens: "
        f"{usage_data['output_tokens']}"
    )

    print(
        f"Total tokens: "
        f"{usage_data['total_tokens']}"
    )

    print(
        f"Estimated cost: "
        f"${usage_data['estimated_cost_usd']:.6f}"
    )

    # --------------------------------------------------
    # Step 8: External LinkedIn enrichment
    # --------------------------------------------------

    print("\nChecking LinkedIn profiles...")

    for member in result.team_members:

        if member.linkedin_url:

            print(
                f"LinkedIn already found for "
                f"{member.name}: "
                f"{member.linkedin_url}"
            )

            continue

        try:

            linkedin_url = search_linkedin(
                member.name,
                domain
            )

            if linkedin_url:

                member.linkedin_url = linkedin_url

                print(
                    f"Found LinkedIn for "
                    f"{member.name}: "
                    f"{linkedin_url}"
                )

            else:

                print(
                    f"No LinkedIn found for "
                    f"{member.name}"
                )

        except Exception as e:

            print(
                f"LinkedIn search failed for "
                f"{member.name}: {e}"
            )

    # --------------------------------------------------
    # Step 9: Build final result
    # --------------------------------------------------

    result_data = result.model_dump()

    result_data["usage"] = usage_data

    print("\nCompany Intelligence:")

    print(
        json.dumps(
            result_data,
            indent=2,
            ensure_ascii=False
        )
    )

    return result_data


# --------------------------------------------------
# CLI input
# --------------------------------------------------

domains = sys.argv[1:]

if not domains:

    print("Please provide at least one company domain.")

    print(
        "Example: "
        "python main.py postman.com supabase.com vapi.ai"
    )

    sys.exit(1)


# --------------------------------------------------
# Process all domains
# --------------------------------------------------

results = {}

for domain in domains:

    print("\n" + "=" * 60)
    print(f"PROCESSING: {domain}")
    print("=" * 60)

    try:

        results[domain] = process_domain(domain)

    except Exception as e:

        print(
            f"Failed to process {domain}: {e}"
        )

        results[domain] = None


# --------------------------------------------------
# Save final output
# --------------------------------------------------

with open(
    "output.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        results,
        f,
        indent=2,
        ensure_ascii=False
    )


print("\nSaved results to output.json")