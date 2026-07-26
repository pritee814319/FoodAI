import requests
from bs4 import BeautifulSoup



REMOVE_WORDS = [

    "share",
    "facebook",
    "instagram",
    "twitter",
    "comments",
    "advertisement",
    "newsletter",
    "related recipes",
    "more recipes",
    "jump to recipe",
    "author",
    "subscribe",
    "privacy",
    "cookie",
    "cooking basics",
    "tips",
    "variation"

]



INGREDIENT_MARKERS = [

    "cup",
    "cups",
    "tbsp",
    "tablespoon",
    "tsp",
    "teaspoon",
    "gram",
    "kg",
    "ml",
    "oz",
    "lb",
    "½",
    "¼",
    "¾"

]



def recipe_parser_agent(url):

    try:

        headers = {
            "User-Agent":
            "Mozilla/5.0"
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


        text = soup.get_text(
            "\n"
        )


        lines = [

            x.strip()

            for x in text.split("\n")

            if x.strip()

        ]



        ingredients = []

        instructions = []



        for line in lines:


            lower = line.lower()



            if any(
                word in lower
                for word in REMOVE_WORDS
            ):

                continue



            if len(line) > 120:

                continue



            # Ingredients

            if any(
                marker in lower
                for marker in INGREDIENT_MARKERS
            ):

                ingredients.append(line)



            # Instructions

            elif (

                lower.startswith("add")
                or lower.startswith("mix")
                or lower.startswith("cook")
                or lower.startswith("heat")
                or lower.startswith("serve")
                or lower.startswith("stir")
                or lower.startswith("saute")
                or lower.startswith("fry")

            ):

                instructions.append(line)



        return {

            "Ingredients":

            list(dict.fromkeys(ingredients))[:30],


            "Instructions":

            list(dict.fromkeys(instructions))[:20]

        }



    except Exception as e:


        print(
            "Parser error:",
            e
        )


        return {

            "Ingredients": [],

            "Instructions": []

        }
