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



        # ==================================
        # Read Schema.org Recipe Data
        # ==================================


        scripts = soup.find_all(
            "script",
            type="application/ld+json"
        )



        for script in scripts:


            try:


                if not script.string:

                    continue



                data = json.loads(
                    script.string
                )



                if isinstance(
                    data,
                    list
                ):

                    items = data


                else:

                    items = [
                        data
                    ]



                for item in items:



                    recipe_type = str(
                        item.get(
                            "@type",
                            ""
                        )
                    )



                    if "Recipe" not in recipe_type:

                        continue



                    # --------------------------
                    # Ingredients
                    # --------------------------


                    ing = item.get(
                        "recipeIngredient",
                        []
                    )


                    if isinstance(
                        ing,
                        list
                    ):

                        ingredients.extend(
                            ing
                        )



                    # --------------------------
                    # Instructions
                    # --------------------------


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



            except Exception as e:


                print(
                    "JSON PARSE ERROR:",
                    e
                )




        # ==================================
        # HTML fallback
        # ==================================


        if not ingredients:



            tags = soup.find_all(
                [
                    "li",
                    "p"
                ]
            )



            for tag in tags:



                text = tag.get_text(
                    " ",
                    strip=True
                )



                lower = text.lower()



                if any(
                    word in lower
                    for word in [

                        "cup",
                        "tbsp",
                        "tsp",
                        "poha",
                        "onion",
                        "rice",
                        "oil",
                        "peanut"

                    ]
                ):



                    if len(text) < 150:


                        ingredients.append(
                            text
                        )





        # ==================================
        # Clean duplicates
        # ==================================


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



        print(
            "INGREDIENTS FOUND:",
            len(ingredients)
        )


        print(
            "INSTRUCTIONS FOUND:",
            len(instructions)
        )



        recipe["Ingredients"] = ingredients[:30]


        recipe["Instructions"] = "\n\n".join(
            instructions[:20]
        )



        return recipe



    except Exception as e:


        print(
            "PARSER ERROR:",
            e
        )


        return recipe
