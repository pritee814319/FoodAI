import requests
from bs4 import BeautifulSoup


def recipe_parser_agent(url):

    try:

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


        # Remove unwanted page sections

        for tag in soup(
            [
                "script",
                "style",
                "nav",
                "footer",
                "header",
                "aside"
            ]
        ):
            tag.decompose()



        text = soup.get_text("\n")


        lines = [
            line.strip()
            for line in text.split("\n")
            if line.strip()
        ]



        ingredients = []
        instructions = []



        # Words to ignore

        ignore = [

            "share",
            "facebook",
            "instagram",
            "twitter",
            "subscribe",
            "newsletter",
            "comments",
            "author",
            "jump to recipe",
            "print recipe",
            "save recipe",
            "privacy",
            "cookie",
            "advertisement",
            "cooking tips",
            "cooking basics",
            "related recipes",
            "more recipes",
            "you may also like"

        ]



        for line in lines:


            lower = line.lower()



            if any(
                word in lower
                for word in ignore
            ):
                continue



            # Ignore headings

            if len(line) < 5:
                continue



            if len(line) > 180:
                continue



            # Ingredient detection

            ingredient_words = [

                "cup",
                "cups",
                "tbsp",
                "tablespoon",
                "tablespoons",
                "tsp",
                "teaspoon",
                "teaspoons",
                "gram",
                "grams",
                "kg",
                "ml",
                "clove",
                "piece",
                "pieces",
                "inch",
                "½",
                "¼",
                "¾"

            ]



            if any(
                word in lower
                for word in ingredient_words
            ):

                ingredients.append(line)

                continue




            # Instruction detection

            action_words = [

                "add ",
                "mix ",
                "cook ",
                "heat ",
                "stir ",
                "fry ",
                "saute",
                "sauté",
                "boil ",
                "wash ",
                "rinse ",
                "drain ",
                "serve ",
                "cover ",
                "remove ",
                "place "

            ]



            if lower.startswith(
                tuple(action_words)
            ):

                instructions.append(line)



        return {


            "Ingredients":
            list(dict.fromkeys(ingredients))[:30],


            "Instructions":
            list(dict.fromkeys(instructions))[:25]

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
