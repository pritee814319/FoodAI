
import requests
from bs4 import BeautifulSoup
import json


def recipe_parser_agent(url):

    headers = {

        "User-Agent":
        "Mozilla/5.0"

    }


    response = requests.get(
        url,
        headers=headers,
        timeout=15
    )


    if response.status_code != 200:

        return {

            "error": "Unable to open recipe page"

        }


    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )


    recipes = soup.find_all(
        "script",
        type="application/ld+json"
    )


    for script in recipes:


        try:

            data = json.loads(
                script.string
            )


            # Some websites return a list

            if isinstance(data, list):

                items = data

            else:

                items = [data]



            for item in items:


                if item.get(
                    "@type"
                ) == "Recipe":


                    return {

                        "Recipe":
                            item.get(
                                "name"
                            ),

                        "Ingredients":
                            item.get(
                                "recipeIngredient",
                                []
                            ),

                        "Instructions":
                            extract_instructions(
                                item.get(
                                    "recipeInstructions",
                                    []
                                )
                            ),

                        "Servings":
                            item.get(
                                "recipeYield"
                            ),

                        "Source":
                            url

                    }


        except Exception:

            continue



    return {

        "error":
        "Recipe information not found"

    }





def extract_instructions(data):


    instructions = []


    if isinstance(
        data,
        list
    ):


        for step in data:


            if isinstance(
                step,
                dict
            ):

                text = step.get(
                    "text"
                )

                if text:

                    instructions.append(
                        text
                    )


            else:

                instructions.append(
                    step
                )


    elif isinstance(
        data,
        str
    ):

        instructions.append(
            data
        )


    return instructions
