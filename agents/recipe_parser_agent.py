import requests
from bs4 import BeautifulSoup
import json


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
            timeout=20
        )


        print(
            "STATUS:",
            response.status_code
        )


        if response.status_code != 200:

            return recipe



        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )


        ingredients = []

        instructions = []



        # -------------------------
        # Method 1 Schema.org
        # -------------------------

        scripts = soup.find_all(
            "script",
            type="application/ld+json"
        )


        for script in scripts:


            try:

                data = json.loads(
                    script.string
                )


                if isinstance(data, list):

                    items = data

                else:

                    items = [data]



                for item in items:


                    if "Recipe" in str(
                        item.get("@type","")
                    ):


                        ingredients.extend(
                            item.get(
                                "recipeIngredient",
                                []
                            )
                        )


                      steps = item.get(
    "recipeInstructions",
    []
)


if isinstance(steps, list):


    for step in steps:


        if isinstance(
            step,
            dict
        ):


            text = step.get(
                "text",
                ""
            )


            if text:

                instructions.append(
                    text
                )


        elif isinstance(
            step,
            str
        ):


            instructions.append(
                step
            )


elif isinstance(
    steps,
    str
):


    instructions.append(
        steps
    )


                        if isinstance(
                            steps,
                            list
                        ):

                            for s in steps:

                                if isinstance(
                                    s,
                                    dict
                                ):

                                    instructions.append(
                                        s.get(
                                            "text",
                                            ""
                                        )
                                    )

                                else:

                                    instructions.append(
                                        s
                                    )


            except:

                pass



        # -------------------------
        # Method 2 HTML fallback
        # -------------------------

        if not ingredients:


            possible = soup.find_all(
                [
                    "li",
                    "p"
                ]
            )


            for tag in possible:


                text = tag.get_text(
                    " ",
                    strip=True
                )


                words = text.lower()


                if any(
                    x in words
                    for x in [
                        "cup",
                        "tbsp",
                        "tsp",
                        "poha",
                        "rice",
                        "onion",
                        "oil"
                    ]
                ):

                    if len(text) < 150:

                        ingredients.append(
                            text
                        )



        # remove duplicates

        ingredients = list(
            dict.fromkeys(
                ingredients
            )
        )


        recipe["Ingredients"] = ingredients[:30]


        recipe["Instructions"] = "\n".join(
            instructions
        )


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
