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
        # Read recipe JSON-LD
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


                    if not isinstance(item, dict):
                        continue



                    if item.get("@type") == "Recipe" or "Recipe" in str(item.get("@type")):


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

                                instructions.append(
                                    step.get(
                                        "text",
                                        ""
                                    )
                                )


                            elif isinstance(step,str):

                                instructions.append(step)



            except:

                continue



        # -------------------------
        # Clean ingredients
        # -------------------------

        clean_ing=[]


        for item in ingredients:


            if not isinstance(item,str):
                continue


            item=item.strip()


            if len(item)<3:
                continue


            clean_ing.append(item)



        ingredients = list(
            dict.fromkeys(clean_ing)
        )



        # -------------------------
        # Clean instructions
        # -------------------------

        clean_steps=[]


        for step in instructions:


            if not step:
                continue


            step=step.strip()


            if len(step)<5:
                continue


            clean_steps.append(step)



        instructions=list(
            dict.fromkeys(clean_steps)
        )



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
