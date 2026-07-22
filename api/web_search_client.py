import requests
from bs4 import BeautifulSoup
from urllib.parse import quote


def search_web_recipes(food):

    query = quote(
        food + " recipe ingredients instructions"
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
        timeout=10
    )


    if response.status_code != 200:

        return []


    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )


    results = []


    for link in soup.select(
        ".result__a"
    )[:5]:

        title = link.text

        href = link.get(
            "href"
        )


        results.append({

            "title": title,

            "url": href

        })


    return results
