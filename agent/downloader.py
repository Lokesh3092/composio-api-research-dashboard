import os
import requests
from bs4 import BeautifulSoup


def download_documentation(url, app_name):

    response = requests.get(
        url,
        timeout=20,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
        tag.decompose()

    text = soup.get_text(separator="\n")

    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]

    clean_text = "\n".join(lines)

    os.makedirs("data/raw_docs", exist_ok=True)

    filename = f"data/raw_docs/{app_name.lower().replace(' ', '_')}.txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(clean_text)

    print(f"Saved: {filename}")

    return filename