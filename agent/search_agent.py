from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

tavily = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)

def search_documentation(app_name):

    query = f"""
    {app_name}
    official developer documentation
    API reference
    authentication
    """

    response = tavily.search(
        query=query,
        max_results=5
    )

    return response