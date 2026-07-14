import os
import csv

from agent.analyzer import load_document
from agent.rule_engine import (
    extract_auth_methods,
    extract_api_surface,
    extract_self_serve,
    extract_buildability,
    extract_mcp
)


def generate_research(csv_input, csv_output):

    with open(csv_input, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        rows = list(reader)

    output = []

    for row in rows:

        app = row["app_name"]
        category = row["category"]

        text = load_document(app)

        if text is None:
            continue

        output.append({

            "app_name": app,

            "category": category,

            "one_line_description": "",

            "auth_methods": ", ".join(
                extract_auth_methods(text)
            ),

            "self_serve_vs_gated":
                extract_self_serve(text),

            "api_surface":
                ", ".join(
                    extract_api_surface(text)
                ),

            "buildability_verdict":
                extract_buildability(text),

            "main_blocker": "",

            "evidence_url": ""

        })

    with open(csv_output,
              "w",
              newline="",
              encoding="utf-8") as f:

        writer = csv.DictWriter(
            f,
            fieldnames=output[0].keys()
        )

        writer.writeheader()

        writer.writerows(output)

    print(f"Saved {len(output)} rows.")