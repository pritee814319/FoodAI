import requests
from bs4 import BeautifulSoup


def recipe_parser_agent(url):

    try:

        if not url:
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
            line.strip()
            for line in text.split("\n")
            if line.strip()
        ]


        ingredients = []
        instructions = []


        skip_words = [
            "share",
            "facebook",
            "instagram",
            "twitter",
            "newsletter",
            "advertisement",
            "jump to recipe",
            "related recipes",
            "comments"
        ]


        for line in lines:

            lower = line.lower()


            if any(
                word in lower
                for word in skip_words
            ):
                continue


            if len(line.split()) > 15:
                continue


            if any(
                unit in lower
                for unit in [
                    "cup",
                    "tbsp",
                    "tsp",
                    "gram",
                    "kg",
                    "ml",
                    "oz",
                    "lb"
                ]
            ):

                ingredients.append(line)



            if (
                lower.startswith("add")
                or lower.startswith("cook")
                or lower.startswith("mix")
                or lower.startswith("heat")
                or lower.startswith("serve")
                or lower.startswith("rinse")
                or lower.startswith("fry")
            ):

                instructions.append(line)



        ingredients = list(
            dict.fromkeys(
                ingredients
            )
        )


        instructions = list(
            dict.fromkeys(
                instructions
            )
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
