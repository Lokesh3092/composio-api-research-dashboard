import pandas as pd

from agent.search_agent import search_documentation
from agent.downloader import download_documentation


def main():

    apps = pd.read_csv("apps_input.csv")

    print(f"Found {len(apps)} apps\n")

    for index, row in apps.iterrows():

        app_name = row["app_name"]

        print("=" * 60)
        print(f"Processing: {app_name}")

        search_results = search_documentation(app_name)

        if not search_results["results"]:
            print("No documentation found.")
            continue

        docs_url = search_results["results"][0]["url"]

        print("Documentation:", docs_url)

        download_documentation(
            docs_url,
            app_name
        )

        print("Done\n")


if __name__ == "__main__":
    main()