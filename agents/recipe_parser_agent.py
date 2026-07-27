import requests
from bs4 import BeautifulSoup
import json
import re



BAD_INGREDIENT_WORDS = [

    "optional",
    "for garnish",
    "to taste",
    "divided",
    "as needed",
    "recipe",
    "photo",
    "note",
    "tips",
    "comment",
    "subscribe"

]



BAD_STEP_WORDS = [

    "jump to",
    "print",
    "save",
    "share",
    "subscribe",
    "comment",
    "nutrition",
    "calories"

]




def clean_ingredient(text):

    """
    Clean ingredient names
    Example:
    2 cups poha -> poha
    1 medium onion chopped -> onion
    """

    if not isinstance(text, str):

        return None


    text = text.strip()



    if len(text) < 3:

        return None



    lower = text.lower()



    # remove bad content

    if any(
        word in lower
        for word in BAD_INGREDIENT_WORDS
    ):

        return None



    # remove pure numbers

    if re.match(
        r"^[0-9\s./¼½¾-]+$",
        text
    ):

        return None



    # remove measurements

    text = re.sub(
        r"\b\d+(\.\d+)?\b",
        "",
        text
    )


    text = re.sub(
        r"\b(cups?|tbsp|tablespoons?|tsp|teaspoons?|grams?|kg|ml|oz|lb)\b",
        "",
        text,
        flags=re.I
    )



    # remove brackets

    text = re.sub(
        r"\(.*?\)",
        "",
        text
    )



    # remove extra words

    remove_words = [

        "finely chopped",
        "roughly chopped",
        "chopped",
        "sliced",
        "diced",
        "minced",
        "optional"

    ]


    for word in remove_words:

        text = text.replace(
            word,
            ""
        )



    text = text.strip(
        " -,:"
    )



    if len(text) < 3:

        return None



    return text.title()





def clean_instruction(text):


    if not isinstance(text,str):

        return None



    text = text.strip()



    if len(text)<10:

        return None



    lower=text.lower()



    if any(
        word in lower
        for word in BAD_STEP_WORDS
    ):

        return None



    # remove numbering

    text = re.sub(
        r"^\d+\.",
        "",
        text
    )


    return text.strip()





def recipe_parser_agent(url):


    try:


        print(
            "PARSING:",
            url
        )


        headers = {

            "User-Agent":
            "Mozilla/5.0"

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



        ingredients=[]

        instructions=[]



        ###################################
        # JSON LD EXTRACTION
        ###################################


        scripts = soup.find_all(

            "script",

            type="application/ld+json"

        )



        for script in scripts:


            try:


                data=json.loads(
                    script.string
                )



            except:

                continue




            items=[]


            if isinstance(data,list):

                items=data


            else:

                items=[data]



            for item in items:


                if not isinstance(
                    item,
                    dict
                ):

                    continue



                recipe_type=str(
                    item.get("@type","")
                )



                if "Recipe" not in recipe_type:

                    continue



                ################################
                # INGREDIENTS
                ################################


                raw_ing=item.get(

                    "recipeIngredient",

                    []

                )



                for ing in raw_ing:


                    cleaned=clean_ingredient(
                        ing
                    )


                    if cleaned:

                        ingredients.append(
                            cleaned
                        )




                ################################
                # INSTRUCTIONS
                ################################


                raw_steps=item.get(

                    "recipeInstructions",

                    []

                )



                for step in raw_steps:



                    if isinstance(
                        step,
                        dict
                    ):

                        step=step.get(
                            "text",
                            ""
                        )



                    cleaned=clean_instruction(
                        step
                    )


                    if cleaned:

                        instructions.append(
                            cleaned
                        )





        ###################################
        # REMOVE DUPLICATES
        ###################################


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
            "FINAL INGREDIENTS:",
            ingredients
        )



        print(
            "FINAL STEPS:",
            len(instructions)
        )



        return {


            "Ingredients":

                ingredients[:25],


            "Instructions":

                instructions[:20],


            "URL":

                url

        }



    except Exception as e:


        print(
            "Parser Error:",
            e
        )


        return {


            "Ingredients":[],

            "Instructions":[],

            "URL":url

        }
