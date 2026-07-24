import requests
from bs4 import BeautifulSoup
import re



BLOCK_WORDS = [

    "faq",
    "frequently asked",
    "expert tips",
    "troubleshooting",
    "more breakfast recipes",
    "more recipes",
    "photo guide",
    "related recipes",
    "this post was first published",
    "updated & republished",
    "comments",
    "reviews",
    "share with friends",
    "print recipe",
    "jump to recipe"

]



STOP_WORDS = [

    "chilla recipe",
    "methi thepla",
    "upma recipe",
    "rava idli",
    "semiya upma",
    "akki roti"

]




def clean_line(text):

    text=text.strip()


    if len(text)<3:

        return ""



    lower=text.lower()


    for word in BLOCK_WORDS:

        if word in lower:

            return ""



    for word in STOP_WORDS:

        if word in lower:

            return ""



    return text





def extract_image(soup):


    image = soup.find(
        "meta",
        property="og:image"
    )


    if image:

        return image.get(
            "content"
        )



    return ""





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

            timeout=15,

            headers={

                "User-Agent":
                "Mozilla/5.0"

            }

        )



        soup=BeautifulSoup(

            response.text,

            "html.parser"

        )



        image_url = extract_image(
            soup
        )



        text=soup.get_text(
            "\n"
        )



        lines=[

            clean_line(x)

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



            if (

                "instruction" in low

                or

                "direction" in low

                or

                "method" in low

            ):

                mode="instructions"

                continue



            if mode=="ingredients":


                if len(ingredients)<25:

                    ingredients.append(
                        line
                    )



            elif mode=="instructions":


                if len(instructions)<20:

                    instructions.append(
                        line
                    )





        return {


            "Recipe":

            recipe.get(
                "Recipe",
                recipe.get("title")
            ),



            "URL":

            url,



            "Image":

            image_url,



            "Ingredients":

            ingredients,



            "Instructions":

            instructions

        }



    except Exception as e:


        print(
            "Parser Error:",
            e
        )


        return {

            "Recipe":
            recipe.get("Recipe"),


            "URL":
            url,


            "Image":"",


            "Ingredients":[],

            "Instructions":[]

        }
