import csv
import json
from collections import Counter


def analyze_patterns(csv_file, output_json):

    auth_counter = Counter()
    api_counter = Counter()
    selfserve_counter = Counter()
    build_counter = Counter()

    with open(csv_file, newline="", encoding="utf-8") as f:

        reader = csv.DictReader(f)

        for row in reader:

            # Authentication
            for auth in row["auth_methods"].split(","):
                auth = auth.strip()
                if auth:
                    auth_counter[auth] += 1

            # API Surface
            for api in row["api_surface"].split(","):
                api = api.strip()
                if api:
                    api_counter[api] += 1

            # Self Serve
            value = row["self_serve_vs_gated"].strip()
            if value:
                selfserve_counter[value] += 1

            # Buildability
            value = row["buildability_verdict"].strip()
            if value:
                build_counter[value] += 1

    patterns = {
        "Authentication Methods": dict(auth_counter),
        "API Types": dict(api_counter),
        "Self Serve vs Gated": dict(selfserve_counter),
        "Buildability": dict(build_counter)
    }

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(patterns, f, indent=4)

    print("Pattern analysis completed.")