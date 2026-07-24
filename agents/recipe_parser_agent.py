import requests
from bs4 import BeautifulSoup
import json



def clean_instruction(text):

    if not isinstance(text, str):
        return ""


    bad_words = [

        "share",
        "subscribe",
        "comments",
        "reviews",
        "about",
        "table of contents",
        "more recipes",
        "related"

    ]


    lower = text.lower()


    for word in bad_words:

        if word in lower:

            return ""


    return text.strip()





def extract_json_ld(soup):


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

                for item in data:

                    if item.get("@type") == "Recipe":

                        return item



            elif isinstance(data, dict):


                if data.get("@type") == "Recipe":

                    return data



                graph = data.get(
                    "@graph",
                    []
                )


                for item in graph:

                    if item.get("@type") == "Recipe":

                        return item



        except Exception:

            continue



    return None






def recipe_parser_agent(recipe):


    url = recipe.get(
        "URL",
        ""
    )


    if not url:


        return {


            "Recipe":
            recipe.get(
                "Recipe",
                "Unknown Recipe"
            ),


            "URL":"",


            "Image":"",


            "Ingredients":[],


            "Instructions":[]

        }





    try:


        response = requests.get(

            url,

            headers={

                "User-Agent":
                "Mozilla/5.0"

            },

            timeout=15

        )



        soup = BeautifulSoup(

            response.text,

            "html.parser"

        )



        recipe_data = extract_json_ld(
            soup
        )



        if not recipe_data:


            print(
                "No JSON recipe found:",
                url
            )


            return {


                "Recipe":
                recipe.get(
                    "Recipe",
                    "Recipe"
                ),


                "URL":
                url,


                "Image":"",


                "Ingredients":[],


                "Instructions":[]

            }




        # -------------------------
        # IMAGE
        # -------------------------


        image = recipe_data.get(
            "image",
            ""
        )


        if isinstance(image,list):

            image=image[0]



        # -------------------------
        # INGREDIENTS
        # -------------------------


        ingredients = recipe_data.get(
            "recipeIngredient",
            []
        )



        clean_ingredients=[]


        for item in ingredients:


            if isinstance(item,str):

                item=item.strip()


                if item:

                    clean_ingredients.append(
                        item
                    )



        # -------------------------
        # INSTRUCTIONS
        # -------------------------


        instructions=[]


        raw_steps = recipe_data.get(
            "recipeInstructions",
            []
        )



        for step in raw_steps:


            if isinstance(
                step,
                dict
            ):


                text = step.get(
                    "text",
                    ""
                )


            else:

                text=str(step)



            text=clean_instruction(
                text
            )


            if text:


                instructions.append(
                    text
                )



        return {


            "Recipe":

            recipe_data.get(
                "name",
                recipe.get(
                    "Recipe",
                    "Recipe"
                )
            ),



            "URL":

            url,



            "Image":

            image,



            "Ingredients":

            clean_ingredients[:30],



            "Instructions":

            instructions[:20]

        }



    except Exception as e:


        print(
            "PARSER ERROR:",
            e
        )



        return {


            "Recipe":
            recipe.get(
                "Recipe",
                "Recipe"
            ),


            "URL":
            url,


            "Image":"",


            "Ingredients":[],


            "Instructions":[]

        }
