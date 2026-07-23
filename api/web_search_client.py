import requests
from bs4 import BeautifulSoup
from urllib.parse import quote



def search_web_recipes(food):


    query = quote(
        f"{food} recipe"
    )


    url = (
        "https://html.duckduckgo.com/html/?q="
        + query
    )


    headers = {

        "User-Agent":
        "Mozilla/5.0"

    }


    response = requests.get(
        url,
        headers=headers,
        timeout=15
    )


    if response.status_code != 200:

        print(
            "SEARCH STATUS:",
            response.status_code
        )

        return []



    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )


    results = []



    for result in soup.select(
        ".result"
    )[:5]:


        title = result.select_one(
            ".result__a"
        )


        snippet = result.select_one(
            ".result__snippet"
        )


        if title:


            results.append({

                "title":
                    title.get_text(),

                "url":
                    title.get(
                        "href"
                    ),

                "snippet":
                    snippet.get_text()
                    if snippet
                    else ""

            })


    return results
