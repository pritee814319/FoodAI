import requests
from bs4 import BeautifulSoup


def recipe_parser_agent(url):

    try:

        headers = {
            "User-Agent":
            "Mozilla/5.0"
        }

        page = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        soup = BeautifulSoup(
            page.text,
            "html.parser"
        )

        text = soup.get_text("\n")

        ingredients = []
        instructions = []

        lines = [
            x.strip()
            for x in text.split("\n")
            if x.strip()
        ]

        skip_words = [

            "share",

            "facebook",

            "instagram",

            "twitter",

            "comments",

            "advertisement",

            "newsletter",

            "photo guide",

            "more recipes",

            "breakfast recipes",

            "related recipes",

            "table of contents",

            "reader interactions",

            "jump to recipe"

        ]

        for line in lines:

            lower = line.lower()

            if any(
                word in lower
                for word in skip_words
            ):
                continue

            if len(line) > 150:
                continue

            if (
                "cup" in lower
                or "tbsp" in lower
                or "tsp" in lower
                or "gram" in lower
                or "kg" in lower
                or "oz" in lower
                or "lb" in lower
                or "ml" in lower
                or "▢" in line
            ):

                ingredients.append(line)

            elif (

                lower.startswith("step")

                or lower.startswith("add")

                or lower.startswith("mix")

                or lower.startswith("cook")

                or lower.startswith("heat")

                or lower.startswith("pour")

                or lower.startswith("serve")

                or lower.startswith("garnish")

                or lower.startswith("rinse")

                or lower.startswith("saute")

                or lower.startswith("fry")

            ):

                instructions.append(line)

        ingredients = list(dict.fromkeys(ingredients))
        instructions = list(dict.fromkeys(instructions))

        return {

            "Ingredients": ingredients[:25],

            "Instructions": instructions[:20]

        }

    except Exception:

        return {

            "Ingredients": [],

            "Instructions": []

        }
