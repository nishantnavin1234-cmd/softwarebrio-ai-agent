from urllib.parse import urljoin
def clean_text(text: str) -> str:
    lines = text.splitlines()
    cleaned_lines = [line.strip() for line in lines if line.strip()]
    return "\n".join(cleaned_lines)
def find_links(page):
    links = page.locator("a").all()

    return [
        (link.inner_text().strip(), link.get_attribute("href"))
        for link in links
        ]

def filter_relevant_links(links, domain):
    keywords = ["about", "team", "company", "contact", "pricing"]
    seen = set()
    relevant = []

    for text, href in links:
        if href and (href.startswith("/") or domain in href.lower()) and any(keyword in href.lower() for keyword in keywords):
            if href not in seen:
                seen.add(href)
                relevant.append(href)

    return relevant

def make_absolute_urls(urls, base_url):
    return [urljoin(base_url, url) for url in urls]