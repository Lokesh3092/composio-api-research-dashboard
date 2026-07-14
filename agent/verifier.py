import csv
from agent.analyzer import load_document


def verify(csv_file, output_file):

    results = []

    with open(csv_file, newline="", encoding="utf-8") as f:

        reader = csv.DictReader(f)

        for row in reader:

            app = row["app_name"]

            text = load_document(app)

            confidence = 0

            notes = []

            if text:

                text = text.lower()

                # Authentication
                if row["auth_methods"]:
                    confidence += 20
                else:
                    notes.append("Authentication missing")

                # API Surface
                if row["api_surface"]:
                    confidence += 20
                else:
                    notes.append("API surface not detected in retrieved page")

                # Self Serve
                if row["self_serve_vs_gated"] != "Unknown":
                    confidence += 15
                else:
                    notes.append("Self Serve unknown")

                # Buildability
                if row["buildability_verdict"] == "Yes":
                    confidence += 20
                else:
                    notes.append("Buildability uncertain")

                # Evidence
                if len(text) > 3000:
                    confidence += 25
                else:
                    notes.append("Limited documentation retrieved")

            else:

                confidence = 0
                notes.append("Documentation missing")

            if confidence >= 80:
                status = "PASS"

            elif confidence >= 45:
                status = "REVIEW"

            else:
                status = "FAIL"

            results.append({

                "app_name": app,

                "confidence": confidence,

                "status": status,

                "notes": "; ".join(notes)

            })

    with open(output_file,
              "w",
              newline="",
              encoding="utf-8") as f:

        writer = csv.DictWriter(
            f,
            fieldnames=[
                "app_name",
                "confidence",
                "status",
                "notes"
            ]
        )

        writer.writeheader()

        writer.writerows(results)

    print("Verification Complete.")