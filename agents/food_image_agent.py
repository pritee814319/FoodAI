import requests
from bs4 import BeautifulSoup


def food_image_agent(food):

    try:

        search_url = (
            "https://commons.wikimedia.org/w/index.php?search="
            + food.replace(" ", "+")
            + "&title=Special:MediaSearch&go=Go&type=image"
        )

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        page = requests.get(
            search_url,
            headers=headers,
            timeout=10
        )

        soup = BeautifulSoup(
            page.text,
            "html.parser"
        )

        img = soup.find("img")

        if img:

            src = img.get("src")

            if src:

                if src.startswith("//"):

                    src = "https:" + src

                return src

    except Exception:

        pass

    return None
