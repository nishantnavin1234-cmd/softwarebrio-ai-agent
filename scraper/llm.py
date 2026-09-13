import os
import json

from dotenv import load_dotenv
from groq import Groq

from scraper.schema import CompanyIntelligence


load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def extract_company_intelligence(
    context: str
) -> tuple[CompanyIntelligence, dict]:

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
                    "The company overview should be concise and approximately two sentences. "
                    "The confidence_score must reflect both reliability and completeness "
                    "of the extracted information. "
                    "Use 0.9-1.0 when nearly all requested fields are populated with strong evidence. "
                    "Use 0.7-0.89 when most fields are populated but some information is missing. "
                    "Use 0.5-0.69 when several requested fields are missing or weakly supported. "
                    "Use 0.3-0.49 when only a small amount of useful information was found. "
                    "Use 0.0-0.29 when very little or no reliable information was found. "
                    "If contact emails, team members, or target audience information are not available "
                    "in the provided content, leave those fields empty and reduce the confidence score "
                    "accordingly. "
                    "Never invent information to make the output more complete."
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

    data = json.loads(
        response.choices[0].message.content
    )

    result = CompanyIntelligence.model_validate(data)

    # ---------------------------------------------
    # Token usage
    # ---------------------------------------------

    usage = response.usage

    usage_data = {
        "input_tokens": usage.prompt_tokens if usage else 0,
        "output_tokens": usage.completion_tokens if usage else 0,
        "total_tokens": usage.total_tokens if usage else 0,
    }

    # ---------------------------------------------
    # Estimated cost
    # ---------------------------------------------

    # Approximate pricing for the selected model.
    # Kept separate so it can be updated if pricing changes.
    input_cost_per_million = 0.075
    output_cost_per_million = 0.30

    estimated_cost = (
        usage_data["input_tokens"]
        / 1_000_000
        * input_cost_per_million
        +
        usage_data["output_tokens"]
        / 1_000_000
        * output_cost_per_million
    )

    usage_data["estimated_cost_usd"] = round(
        estimated_cost,
        6
    )

    return result, usage_data