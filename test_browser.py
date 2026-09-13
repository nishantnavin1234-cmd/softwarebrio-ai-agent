from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto("https://postman.com", wait_until="domcontentloaded")

    print("Page title:", page.title())

    browser.close()