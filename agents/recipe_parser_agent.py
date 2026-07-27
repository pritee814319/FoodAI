import requests
from bs4 import BeautifulSoup
import json


def recipe_parser_agent(url):

    print("PARSER URL:", url)

    ingredients = []
    instructions = []


    try:

        headers = {
            "User-Agent": "Mozilla/5.0"
        }


        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )


        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )


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


                items=[]


                if isinstance(data,list):
                    items=data

                elif isinstance(data,dict):

                    if "@graph" in data:

                        items=data["@graph"]

                    else:

                        items=[data]



                for item in items:


                    if not isinstance(item,dict):
                        continue



                    recipe_type=str(
                        item.get("@type","")
                    )


                    if "Recipe" not in recipe_type:
                        continue



                    print("FOUND RECIPE JSON")



                    # INGREDIENTS

                    ing=item.get(
                        "recipeIngredient",
                        []
                    )


                    if ing:

                        ingredients.extend(
                            ing
                        )



                    # INSTRUCTIONS

                    steps=item.get(
                        "recipeInstructions",
                        []
                    )


                    if isinstance(steps,list):


                        for step in steps:


                            if isinstance(step,dict):

                                text=step.get(
                                    "text",
                                    ""
                                )


                                if text:
                                    instructions.append(text)


                            elif isinstance(step,str):

                                instructions.append(step)



            except Exception as e:

                print(
                    "JSON ERROR:",
                    e
                )



        # remove duplicates

        ingredients=list(
            dict.fromkeys(
                ingredients
            )
        )


        instructions=list(
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



        return {


            "Recipe": "",


            "URL": url,


            "Ingredients": ingredients[:40],


            "Instructions": instructions[:40]

        }



    except Exception as e:


        print(
            "PARSER ERROR:",
            e
        )


        return {


            "Recipe": "",


            "URL": url,


            "Ingredients": [],


            "Instructions": []

        }
