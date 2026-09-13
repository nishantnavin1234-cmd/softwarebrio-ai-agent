import os
import json

from dotenv import load_dotenv
from groq import Groq

from scraper.schema import CompanyIntelligence


load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def extract_company_intelligence(context: str) -> CompanyIntelligence:
    schema = CompanyIntelligence.model_json_schema()

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a company research assistant. "
                    "Extract company intelligence only from the provided website content. "
                    "Do not invent information. "
                    "If information is not available, use an empty list or null where appropriate. "
                    "The company overview should be concise and approximately two sentences."
                ),
            },
            {
                "role": "user",
                "content": context,
            },
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "company_intelligence",
                "schema": schema,
            },
        },
        temperature=0,
    )

    data = json.loads(response.choices[0].message.content)

    return CompanyIntelligence.model_validate(data)