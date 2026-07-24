import requests
from bs4 import BeautifulSoup
import re



def recipe_parser_agent(recipe):

    print(
        "PARSING RECIPE:",
        recipe.get("Recipe")
    )


    url = recipe.get(
        "URL",
        ""
    )


    if not url:

        return recipe



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


        if response.status_code != 200:

            print(
                "PAGE ERROR:",
                response.status_code
            )

            return recipe



        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )



        # --------------------------------
        # Extract page text
        # --------------------------------

        text = soup.get_text(
            " ",
            strip=True
        )



        # --------------------------------
        # Ingredients
        # --------------------------------

        ingredients = []


        ingredient_keywords = [

            "ingredients",
            "ingredient"

        ]


        for tag in soup.find_all(
            ["li","p"]
        ):


            content = tag.get_text(
                " ",
                strip=True
            )


            if len(content) > 3:

                if any(
                    word in content.lower()
                    for word in [
                        "cup",
                        "tbsp",
                        "tsp",
                        "kg",
                        "gram",
                        "g ",
                        "ml",
                        "onion",
                        "tomato",
                        "salt"
                    ]
                ):

                    ingredients.append(
                        content
                    )



        # remove duplicates

        ingredients = list(
            dict.fromkeys(
                ingredients
            )
        )



        # --------------------------------
        # Instructions
        # --------------------------------

        instructions = []


        for tag in soup.find_all(
            ["li","p"]
        ):


            content = tag.get_text(
                " ",
                strip=True
            )


            if len(content) > 30:

                if any(
                    word in content.lower()
                    for word in [
                        "cook",
                        "add",
                        "mix",
                        "heat",
                        "boil",
                        "bake",
                        "serve"
                    ]
                ):

                    instructions.append(
                        content
                    )



        # --------------------------------
        # Servings
        # --------------------------------

        servings = ""


        match = re.search(
            r"(serves|servings|yield)\s*:?\s*(\d+)",
            text,
            re.I
        )


        if match:

            servings = match.group(2)



        recipe["Ingredients"] = ingredients[:20]

        recipe["Instructions"] = "\n".join(
            instructions[:10]
        )

        recipe["Servings"] = servings



        print(
            "INGREDIENTS FOUND:",
            len(ingredients)
        )


        print(
            "INSTRUCTIONS FOUND:",
            len(instructions)
        )


        return recipe



    except Exception as e:


        print(
            "PARSER ERROR:",
            e
        )


        return recipe
