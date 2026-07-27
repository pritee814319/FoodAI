import requests
from bs4 import BeautifulSoup
import json
import re



def extract_json_objects(data):

    """
    Find all recipe objects from JSON-LD
    """

    results = []


    if isinstance(data, dict):

        if "@graph" in data:

            results.extend(
                extract_json_objects(
                    data["@graph"]
                )
            )


        else:

            results.append(data)



    elif isinstance(data, list):

        for item in data:

            results.extend(
                extract_json_objects(item)
            )


    return results




def clean_ingredient(item):


    if not isinstance(item,str):

        return None


    text=item.strip()



    if len(text)<3:

        return None



    bad=[

        "optional",
        "to taste",
        "for garnish",
        "recipe",
        "photo",
        "note"

    ]



    lower=text.lower()



    if any(
        x in lower
        for x in bad
    ):

        return None



    # remove numbers

    text=re.sub(
        r"^\d+[\d\/\.\s¼½¾]*",
        "",
        text
    )



    # remove measurements

    text=re.sub(

        r"\b(cups?|tbsp|tablespoons?|tsp|teaspoons?|grams?|ml)\b",

        "",

        text,

        flags=re.I

    )



    text=text.strip(
        " ,-"
    )



    return text





def clean_instruction(step):


    if isinstance(step,dict):

        step=step.get(
            "text",
            ""
        )


    if not isinstance(step,str):

        return None



    step=step.strip()



    if len(step)<10:

        return None



    return step





def recipe_parser_agent(url):


    print(
        "PARSING URL:",
        url
    )


    try:


        response=requests.get(

            url,

            headers={
                "User-Agent":
                "Mozilla/5.0"
            },

            timeout=15

        )



        soup=BeautifulSoup(

            response.text,

            "html.parser"

        )



        ingredients=[]

        instructions=[]



        scripts=soup.find_all(

            "script",

            type="application/ld+json"

        )



        print(
            "JSON SCRIPTS:",
            len(scripts)
        )



        for script in scripts:


            try:

                data=json.loads(
                    script.string
                )


            except:

                continue



            objects=extract_json_objects(
                data
            )



            for obj in objects:


                recipe_type=str(
                    obj.get(
                        "@type",
                        ""
                    )
                )



                if "Recipe" not in recipe_type:

                    continue



                print(
                    "FOUND RECIPE JSON"
                )



                raw_ing=obj.get(

                    "recipeIngredient",

                    []

                )



                for ing in raw_ing:


                    clean=clean_ingredient(
                        ing
                    )


                    if clean:

                        ingredients.append(
                            clean
                        )



                raw_steps=obj.get(

                    "recipeInstructions",

                    []

                )



                for step in raw_steps:


                    clean=clean_instruction(
                        step
                    )


                    if clean:

                        instructions.append(
                            clean
                        )




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
            "INGREDIENT COUNT:",
            len(ingredients)
        )


        print(
            "STEP COUNT:",
            len(instructions)
        )



        return {


            "Ingredients":

                ingredients[:30],


            "Instructions":

                instructions[:20],


            "URL":

                url

        }



    except Exception as e:


        print(
            "PARSER ERROR:",
            e
        )


        return {

            "Ingredients":[],

            "Instructions":[],

            "URL":url

        }
