import requests
from bs4 import BeautifulSoup
import json



def clean_text(text):

    if not text:
        return ""


    remove_words = [

        "review",
        "comment",
        "subscribe",
        "follow",
        "copyright",
        "privacy",
        "cookie",
        "jump to recipe",
        "share"

    ]


    text = text.strip()


    lower = text.lower()


    for word in remove_words:

        if word in lower:

            return ""


    return text




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
        # Schema.org Recipe Extraction
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



                if isinstance(data,list):

                    data_list=data

                else:

                    data_list=[data]



                for item in data_list:



                    if "Recipe" not in str(

                        item.get(
                            "@type",
                            ""
                        )

                    ):

                        continue




                    # Ingredients


                    ing = item.get(

                        "recipeIngredient",

                        []

                    )



                    if isinstance(

                        ing,

                        list

                    ):


                        for i in ing:


                            value = clean_text(i)


                            if value:

                                ingredients.append(
                                    value
                                )





                    # Instructions


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


                                value = step.get(

                                    "text",

                                    ""

                                )



                            else:


                                value = step




                            value = clean_text(
                                value
                            )



                            if value:

                                instructions.append(
                                    value
                                )




                    elif isinstance(

                        steps,

                        str

                    ):


                        value = clean_text(
                            steps
                        )


                        if value:

                            instructions.append(
                                value
                            )





            except Exception as e:


                print(
                    "JSON ERROR:",
                    e
                )






        # ==================================
        # Remove duplicates
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





        # ==================================
        # Safety filter
        # ==================================


        ingredients = [

            x for x in ingredients

            if len(x.split()) <= 12

        ]



        instructions = [

            x for x in instructions

            if len(x.split()) > 3

        ]






        recipe["Ingredients"] = ingredients[:20]


        recipe["Instructions"] = instructions[:15]



        print(

            "INGREDIENTS:",

            len(recipe["Ingredients"])

        )


        print(

            "INSTRUCTIONS:",

            len(recipe["Instructions"])

        )



        return recipe





    except Exception as e:


        print(

            "PARSER ERROR:",

            e

        )


        return recipe
