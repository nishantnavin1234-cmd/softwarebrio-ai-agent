from typing import Callable


PAGE_PRIORITIES = {
    "team": 10,
    "founder": 10,
    "founders": 10,
    "leadership": 10,
    "people": 9,
    "about": 9,
    "company": 8,
    "contact": 8,
    "pricing": 6,
    "careers": 5,
}


def score_link(text: str, url: str) -> int:
    """
    Score a link according to how useful it is likely to be
    for company intelligence extraction.
    """

    score = 0

    text_lower = (text or "").lower()
    url_lower = (url or "").lower()

    for keyword, points in PAGE_PRIORITIES.items():

        if keyword in url_lower:
            score += points

        if keyword in text_lower:
            score += points

    return score


def choose_next_pages(
    links: list[tuple[str, str]],
    crawled_urls: set[str],
    max_pages: int = 5
) -> list[str]:
    """
    Select the highest-value pages that have not been crawled yet.
    """

    candidates = []

    for text, href in links:

        if not href:
            continue

        if href in crawled_urls:
            continue

        score = score_link(
            text,
            href
        )

        if score > 0:
            candidates.append(
                (score, href)
            )

    # Highest-value pages first
    candidates.sort(
        key=lambda item: item[0],
        reverse=True
    )

    selected = []
    seen = set()

    for score, href in candidates:

        if href in seen:
            continue

        seen.add(href)
        selected.append(href)

        print(
            f"Agent priority: {score:>2} | {href}"
        )

        if len(selected) >= max_pages:
            break

    return selected


def agent_loop(
    initial_links: list[tuple[str, str]],
    fetch_function: Callable,
    clean_function: Callable,
    base_url: str,
    max_pages: int = 5
):
    """
    Custom multi-step browsing agent.

    At each iteration the agent:
    1. Reviews available links.
    2. Scores them for information value.
    3. Selects the highest-value pages.
    4. Fetches and cleans the selected pages.
    5. Incorporates newly discovered links.
    6. Repeats until the page budget is reached.
    """

    crawled_urls = set()
    gathered_pages = {}

    available_links = list(
        initial_links
    )

    while len(crawled_urls) < max_pages:

        remaining_pages = (
            max_pages - len(crawled_urls)
        )

        next_pages = choose_next_pages(
            links=available_links,
            crawled_urls=crawled_urls,
            max_pages=remaining_pages
        )

        if not next_pages:
            print(
                "Agent found no additional relevant pages."
            )
            break

        for url in next_pages:

            if url in crawled_urls:
                continue

            print(
                f"\nAgent chose: {url}"
            )

            try:

                page_text, page_links = (
                    fetch_function(url)
                )

                crawled_urls.add(url)

                if page_text.strip():

                    cleaned_text = clean_function(
                        page_text
                    )

                    gathered_pages[url] = (
                        cleaned_text[:4000]
                    )

                    print(
                        f"Agent gathered "
                        f"{len(cleaned_text)} characters"
                    )

                # Newly discovered links are fed back
                # into the next decision cycle.
                for link_text, link_url in page_links:

                    if link_url:
                        available_links.append(
                            (link_text, link_url)
                        )

            except Exception as e:

                crawled_urls.add(url)

                print(
                    f"Agent failed to fetch "
                    f"{url}: {e}"
                )

            if len(crawled_urls) >= max_pages:
                break

    return gathered_pages