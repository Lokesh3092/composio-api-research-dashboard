import pandas as pd


# Convert research_output.csv to JSON
research = pd.read_csv("outputs/research_output.csv")
research.to_json(
    "outputs/research_output.json",
    orient="records",
    indent=4
)

# Convert verification.csv to JSON
verification = pd.read_csv("outputs/verification.csv")
verification.to_json(
    "outputs/verification.json",
    orient="records",
    indent=4
)

print("JSON files created successfully!")