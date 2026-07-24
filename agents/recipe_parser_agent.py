import requests
from bs4 import BeautifulSoup
import json
import re



def clean_text(text):

    if not text:
        return ""


    text = text.strip()


    bad_words = [

        "review",
        "comment",
        "subscribe",
        "privacy",
        "cookie",
        "copyright",
        "follow us",
        "share this",
        "leave a reply",
        "jump to recipe"

    ]


    lower = text.lower()


    for word in bad_words:

        if word in lower:

            return ""


    return text




def add_unique(items, value):


    value = clean_text(value)


    if value and value not in items:

        items.append(value)





def extract_schema_recipe(soup):


    ingredients = []

    instructions = []



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

                records = data

            else:

                records = [data]



            for item in records:



                if "Recipe" not in str(
                    item.get("@type","")
                ):

                    continue




                ing = item.get(

                    "recipeIngredient",

                    []

                )



                if isinstance(
                    ing,
                    list
                ):


                    for x in ing:

                        add_unique(
                            ingredients,
                            x
                        )




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

                            add_unique(
                                instructions,
                                step.get(
                                    "text",
                                    ""
                                )
                            )

                        else:

                            add_unique(
                                instructions,
                                step
                            )



                elif isinstance(
                    steps,
                    str
                ):


                    add_unique(
                        instructions,
                        steps
                    )



        except Exception:


            continue



    return ingredients, instructions





def extract_html_recipe(soup):


    ingredients = []

    instructions = []




    # ------------------------------
    # Find ingredient sections
    # ------------------------------


    headings = soup.find_all(

        [
            "h2",
            "h3",
            "h4"
        ]

    )



    for heading in headings:



        title = heading.get_text(

            " ",

            strip=True

        ).lower()



        if "ingredient" in title:



            parent = heading.parent



            if parent:


                for li in parent.find_all(
                    "li"
                ):


                    text = li.get_text(

                        " ",

                        strip=True

                    )


                    if len(text) < 120:


                        add_unique(

                            ingredients,

                            text

                        )





    # ------------------------------
    # Find instruction sections
    # ------------------------------


    for heading in headings:



        title = heading.get_text(

            " ",

            strip=True

        ).lower()



        if any(

            word in title

            for word in [

                "instruction",
                "method",
                "direction",
                "preparation"

            ]

        ):



            parent = heading.parent



            if parent:


                for li in parent.find_all(
                    "li"
                ):


                    text = li.get_text(

                        " ",

                        strip=True

                    )


                    if len(text) > 20:


                        add_unique(

                            instructions,

                            text

                        )




    return ingredients, instructions





def clean_ingredients(items):


    final = []



    for item in items:



        item = re.sub(

            r"\s+",

            " ",

            item

        )



        if len(item.split()) <= 15:


            if not any(

                word in item.lower()

                for word in [

                    "family",
                    "recipe",
                    "love",
                    "comment",
                    "review"

                ]

            ):


                add_unique(

                    final,

                    item

                )



    return final[:25]





def recipe_parser_agent(recipe):


    print(

        "PARSING RECIPE:",

        recipe.get(
            "Recipe"
        )

    )



    url = recipe.get(

        "URL",

        ""

    )



    if not url:

        return recipe




    try:



        response = requests.get(

            url,

            headers={

                "User-Agent":
                "Mozilla/5.0"

            },

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




        ingredients, instructions = extract_schema_recipe(
            soup
        )




        # fallback HTML

        if not ingredients:



            html_ing, html_steps = extract_html_recipe(
                soup
            )


            ingredients.extend(
                html_ing
            )


            instructions.extend(
                html_steps
            )





        ingredients = clean_ingredients(

            ingredients

        )



        instructions = [

            clean_text(x)

            for x in instructions

            if clean_text(x)

        ]



        recipe["Ingredients"] = ingredients


        recipe["Instructions"] = instructions[:20]



        print(

            "INGREDIENTS FOUND:",

            len(ingredients)

        )


        print(

            "INSTRUCTIONS FOUND:",

            len(instructions)

        )



        return recipe




    except Exception as e:


        print(

            "PARSER ERROR:",

            e

        )


        return recipe
