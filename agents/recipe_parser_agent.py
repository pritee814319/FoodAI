import requests
from bs4 import BeautifulSoup
import re


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
        image = ""


        # -------------------------
        # Extract image
        # -------------------------

        img = soup.find(
            "meta",
            property="og:image"
        )

        if img:
            image = img.get("content","")



        # -------------------------
        # Extract Recipe JSON
        # -------------------------

        scripts = soup.find_all(
            "script",
            type="application/ld+json"
        )


        for script in scripts:


            try:

                import json

                data = json.loads(
                    script.string
                )


                if isinstance(data,list):

                    items=data

                else:

                    items=[data]


                for item in items:


                    if item.get("@type")=="Recipe":


                        ingredients = item.get(
                            "recipeIngredient",
                            []
                        )


                        steps=item.get(
                            "recipeInstructions",
                            []
                        )


                        for step in steps:


                            if isinstance(step,dict):

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


            except:

                pass



        # -------------------------
        # Clean
        # -------------------------


        ingredients=[
            x.strip()
            for x in ingredients
            if len(x.strip())>2
        ]


        instructions=[
            x.strip()
            for x in instructions
            if len(x.strip())>5
        ]



        return {


            "URL": url,

            "Image": image,

            "Ingredients": ingredients,

            "Instructions": instructions[:15]

        }



    except Exception as e:


        print(
            "Parser Error:",
            e
        )


        return {

            "URL":url,

            "Image":"",

            "Ingredients":[],

            "Instructions":[]

        }
