from playwright.sync_api import sync_playwright


def fetch_page(url: str) -> tuple[str, list[str]]:
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)

            try:
                page = browser.new_page()

                page.goto(
                    url,
                    wait_until="domcontentloaded",
                    timeout=30000
                )

                text = page.locator("body").inner_text()

                links = page.locator("a").evaluate_all(
                    """elements => elements.map(a => [a.innerText, a.href])
                    .filter(link => link[0] && link[1])"""
                )

                return text, links

            finally:
                browser.close()

    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return "", []