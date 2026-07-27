import os
from tavily import TavilyClient


def tavily_search(query):

    print(
        "TAVILY QUERY:",
        query
    )


    api_key = os.getenv(
        "TAVILY_API_KEY"
    )


    if not api_key:

        print(
            "TAVILY API KEY MISSING"
        )

        return []


    client = TavilyClient(
        api_key=api_key
    )


    response = client.search(
        query=query,
        max_results=5
    )


    return response.get(
        "results",
        []
    )
