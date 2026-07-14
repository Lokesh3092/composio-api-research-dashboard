import os


def load_document(app_name):

    filename = f"data/raw_docs/{app_name.lower().replace(' ', '_')}.txt"

    if not os.path.exists(filename):
        print(f"Document not found: {filename}")
        return None

    with open(filename, "r", encoding="utf-8") as file:
        text = file.read()

    return text