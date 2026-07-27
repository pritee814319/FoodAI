import requests
from bs4 import BeautifulSoup
import json


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


        ingredients = []
        instructions = []


        # -------------------------
        # Extract JSON-LD recipe
        # -------------------------

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


                if isinstance(data, list):

                    items = data

                else:

                    items = [data]



                for item in items:


                    if not isinstance(item, dict):
                        continue


                    recipe_type = str(
                        item.get("@type", "")
                    )


                    if "Recipe" not in recipe_type:
                        continue



                    ingredients = item.get(
                        "recipeIngredient",
                        []
                    )


                    raw_steps = item.get(
                        "recipeInstructions",
                        []
                    )



                    for step in raw_steps:


                        if isinstance(step, dict):

                            text = step.get(
                                "text",
                                ""
                            )

                            if text:
                                instructions.append(text)


                        elif isinstance(step, str):

                            instructions.append(step)



            except Exception as e:

                print(
                    "JSON-LD error:",
                    e
                )



        # -------------------------
        # Clean ingredients
        # -------------------------

        clean_ingredients = []


        for item in ingredients:


            if not isinstance(item, str):
                continue


            item = item.strip()


            if len(item) < 3:
                continue


            clean_ingredients.append(item)



        ingredients = list(
            dict.fromkeys(clean_ingredients)
        )



        # -------------------------
        # Clean instructions
        # -------------------------

        clean_instructions = []


        for step in instructions:


            if not isinstance(step, str):
                continue


            step = step.strip()


            if len(step) < 5:
                continue


            clean_instructions.append(step)



        instructions = list(
            dict.fromkeys(clean_instructions)
        )



        # -------------------------
        # Validation
        # -------------------------

        if len(ingredients) < 5:

            return {

                "Ingredients": [],

                "Instructions": [],

                "URL": url

            }



        if len(instructions) < 3:

            return {

                "Ingredients": [],

                "Instructions": [],

                "URL": url

            }



        return {

            "Ingredients": ingredients[:30],

            "Instructions": instructions[:30],

            "URL": url

        }



    except Exception as e:


        print(
            "Parser error:",
            e
        )


        return {

            "Ingredients": [],

            "Instructions": [],

            "URL": url

        }
