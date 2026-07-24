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



        # -----------------------------
        # Schema.org JSON Recipe Data
        # -----------------------------

        scripts = soup.find_all(
            "script",
            type="application/ld+json"
        )



        for script in scripts:


            try:


                data = json.loads(
                    script.string
                )



                if isinstance(
                    data,
                    list
                ):

                    items = data

                else:

                    items = [data]



                for item in items:



                    if "Recipe" in str(
                        item.get("@type")
                    ):



                        ingredients = item.get(
                            "recipeIngredient",
                            []
                        )



                        steps = item.get(
                            "recipeInstructions",
                            []
                        )



                        servings = item.get(
                            "recipeYield",
                            ""
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



            except Exception:


                pass



        # -----------------------------
        # Clean Ingredients
        # -----------------------------

        clean = []



        for item in ingredients:


            if not isinstance(
                item,
                str
            ):

                continue



            item = item.strip()



            # remove very long descriptions

            if len(item) <= 120:


                clean.append(
                    item
                )



        recipe["Ingredients"] = clean[:40]



        recipe["Instructions"] = "\n".join(
            instructions
        )



        recipe["Servings"] = servings



        print(
            "INGREDIENTS FOUND:",
            len(clean)
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
