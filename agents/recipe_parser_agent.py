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
            timeout=15
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

        servings = ""



        # -----------------------------------
        # Look for Schema Recipe JSON
        # -----------------------------------

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


                    if item.get(
                        "@type"
                    ) == "Recipe" or "Recipe" in str(item.get("@type")):


                        ingredients = item.get(
                            "recipeIngredient",
                            []
                        )


                        steps = item.get(
                            "recipeInstructions",
                            []
                        )


                        if isinstance(
                            steps,
                            list
                        ):

                            for step in steps:

                                if isinstance(
                                    step,
                                    dict
                                ):

                                    instructions.append(
                                        step.get(
                                            "text",
                                            ""
                                        )
                                    )

                                else:

                                    instructions.append(
                                        step
                                    )

                        else:

                            instructions.append(
                                steps
                            )



                        servings = item.get(
                            "recipeYield",
                            ""
                        )


            except Exception:

                pass



        # -----------------------------------
        # Fallback text extraction
        # -----------------------------------

        if not ingredients:


            for li in soup.find_all(
                "li"
            ):

                text = li.get_text(
                    " ",
                    strip=True
                )


                if any(
                    x in text.lower()
                    for x in [
                        "cup",
                        "tbsp",
                        "tsp",
                        "onion",
                        "salt",
                        "oil"
                    ]
                ):

                    ingredients.append(
                        text
                    )



        recipe["Ingredients"] = ingredients


        recipe["Instructions"] = "\n".join(
            instructions
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
