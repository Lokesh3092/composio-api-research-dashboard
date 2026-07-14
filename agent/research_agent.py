import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

from pathlib import Path

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)
print(os.getenv("OPENROUTER_API_KEY"))

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


def extract_page_text(url):

    response = requests.get(
        url,
        timeout=15,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove unwanted HTML elements
    for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
        tag.decompose()

    text = soup.get_text(separator="\n")

    # Clean empty lines
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]

    return "\n".join(lines)

def extract_information(document_text):

    prompt = f"""
You are an API Research Assistant.

Read the documentation below and return ONLY valid JSON.

Return exactly this format:

{{
  "one_line_description": "",
  "auth_methods": [],
  "self_serve_vs_gated": "",
  "api_surface": "",
  "buildability_verdict": "",
  "main_blocker": ""
}}

Documentation:

{document_text[:12000]}
"""

    response = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3-0324:free",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    result = response.choices[0].message.content

    return result


if __name__ == "__main__":

    text = extract_page_text(
        "https://docs.slack.dev/authentication"
    )

    result = extract_information(text)

    print(result)