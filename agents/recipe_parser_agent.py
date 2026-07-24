import requests
from bs4 import BeautifulSoup



BAD_WORDS = [

    "faq",
    "reviews",
    "comments",
    "expert tips",
    "troubleshooting",
    "nutrition facts",
    "jump to recipe"

]




def clean_text(text):


    text=text.strip()


    for word in BAD_WORDS:

        if word.lower() in text.lower():

            return ""


    return text





def recipe_parser_agent(recipe):


    url = recipe.get(
        "URL",
        ""
    )



    if not url:


        return recipe



    try:


        response=requests.get(

            url,

            timeout=10,

            headers={

                "User-Agent":
                "Mozilla/5.0"

            }

        )



        soup=BeautifulSoup(

            response.text,

            "html.parser"

        )



        text=soup.get_text(
            "\n"
        )



        lines=[

            clean_text(x)

            for x in text.split("\n")

        ]



        lines=[

            x for x in lines

            if x

        ]



        ingredients=[]

        instructions=[]



        mode=None



        for line in lines:



            low=line.lower()



            if "ingredient" in low:

                mode="ingredients"

                continue



            if "instruction" in low or "direction" in low:

                mode="instructions"

                continue



            if mode=="ingredients":


                ingredients.append(line)



            elif mode=="instructions":


                instructions.append(line)





        return {


            "Recipe":

            recipe.get(
                "Recipe",
                recipe.get("title")
            ),



            "URL":

            url,



            "Ingredients":

            ingredients[:20],



            "Instructions":

            instructions[:15]

        }



    except Exception as e:


        print(
            "PARSER ERROR",
            e
        )


        return {


            "Recipe":
            recipe.get("Recipe"),


            "URL":
            url,


            "Ingredients":[],

            "Instructions":[]

        }
