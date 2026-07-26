import requests
from bs4 import BeautifulSoup
import re


def recipe_parser_agent(recipe):

    try:

        # If Tavily sends dictionary
        if isinstance(recipe, dict):
            url = recipe.get("URL", "")
        else:
            url = recipe


        if not url.startswith("http"):
            return {
                "Ingredients": [],
                "Instructions": []
            }


        headers = {
            "User-Agent": "Mozilla/5.0"
        }


        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )


        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )


        text = soup.get_text("\n")


        lines = [
            x.strip()
            for x in text.split("\n")
            if x.strip()
        ]


        ingredients = []
        instructions = []


        # words we don't want
        bad = [
            "recipe",
            "author",
            "share",
            "facebook",
            "instagram",
            "subscribe",
            "newsletter",
            "jump to",
            "comments",
            "copyright",
            "privacy",
            "advertisement"
        ]


        for line in lines:


            lower = line.lower()


            if any(
                b in lower
                for b in bad
            ):
                continue


            # ingredient detection
            if re.search(
                r"\d+\s*(cup|cups|tbsp|tablespoon|tsp|teaspoon|g|kg|ml|gram|oz|lb)",
                lower
            ):

                if len(line) < 120:
                    ingredients.append(line)



            # instruction detection

            elif any(
                lower.startswith(x)
                for x in [
                    "add",
                    "mix",
                    "cook",
                    "heat",
                    "fry",
                    "boil",
                    "rinse",
                    "marinate",
                    "serve"
                ]
            ):

                instructions.append(line)



        ingredients = list(
            dict.fromkeys(ingredients)
        )


        instructions = list(
            dict.fromkeys(instructions)
        )


        return {

            "Ingredients": ingredients[:30],

            "Instructions": instructions[:20]

        }


    except Exception as e:

        print(
            "PARSER ERROR:",
            e
        )

        return {

            "Ingredients": [],

            "Instructions": []

        }
