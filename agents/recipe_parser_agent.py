import requests
from bs4 import BeautifulSoup
import re


BAD_TEXT = [

    "google",
    "facebook",
    "instagram",
    "subscribe",
    "newsletter",
    "comments",
    "review",
    "author",
    "jump to recipe",
    "table of contents",
    "privacy",
    "advertisement",
    "cookie",
    "preferred source",
    "cooking tips",
    "cooking basics",
    "more recipes"

]


def clean_line(text):

    text = text.strip()

    if len(text) < 3:
        return False

    lower = text.lower()

    for bad in BAD_TEXT:
        if bad in lower:
            return False


    # remove only numbers
    if re.match(r"^[0-9\.\-\s]+$", text):
        return False


    return True




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


        # remove unwanted html

        for tag in soup(
            [
                "script",
                "style",
                "nav",
                "footer",
                "header"
            ]
        ):
            tag.decompose()



        text = soup.get_text("\n")


        lines = [

            x.strip()

            for x in text.split("\n")

            if clean_line(x)

        ]



        ingredients = []

        instructions = []



        ingredient_words = [

            "cup",
            "cups",
            "tbsp",
            "tablespoon",
            "tsp",
            "teaspoon",
            "kg",
            "gram",
            "grams",
            "ml",
            "clove",
            "slice",
            "chopped",
            "powder"

        ]



        instruction_words = [

            "add",
            "mix",
            "cook",
            "heat",
            "fry",
            "saute",
            "boil",
            "serve",
            "stir"

        ]



        for line in lines:


            lower=line.lower()



            # ingredients

            if any(
                word in lower
                for word in ingredient_words
            ):

                if len(line) < 100:

                    ingredients.append(line)



            # instructions

            elif any(
                lower.startswith(word)
                for word in instruction_words
            ):

                if len(line) < 180:

                    instructions.append(line)




        return {

            "URL":url,

            "Ingredients":

                list(dict.fromkeys(
                    ingredients[:20]
                )),

            "Instructions":

                list(dict.fromkeys(
                    instructions[:15]
                ))

        }



    except Exception as e:


        print(
            "Parser error:",
            e
        )


        return {

            "URL":url,

            "Ingredients":[],

            "Instructions":[]

        }
