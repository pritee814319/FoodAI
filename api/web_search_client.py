from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()


def search_web_recipes(food):


    client = TavilyClient(
        api_key=os.getenv(
            "TAVILY_API_KEY"
        )
    )


    response = client.search(

        query=f"{food} recipe ingredients instructions",

        max_results=5

    )


    results = []


    for item in response["results"]:


        results.append({

            "title":
                item["title"],

            "url":
                item["url"],

            "content":
                item.get(
                    "content",
                    ""
                )

        })


    return results
