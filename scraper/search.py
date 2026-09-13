import os

from dotenv import load_dotenv
from tavily import TavilyClient


load_dotenv()

client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


def search_linkedin(name: str, company: str) -> str | None:
    query = f"{name} {company} LinkedIn"

    response = client.search(
        query=query,
        max_results=5
    )

    for result in response.get("results", []):
        url = result.get("url", "")

        if "linkedin.com/in/" in url.lower():
            return url

    return None