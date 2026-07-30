# agents/ingredient_agent.py

import re


INGREDIENT_MAP = {


    # Rice / Poha
    "poha": "Rice flakes, dry",

    "rice flakes": "Rice flakes, dry",

    "flattened rice": "Rice flakes, dry",



    # Spices
    "turmeric": "Turmeric, ground",

    "salt": "Salt, table",

    "sugar": "Sugar, granulated",



    # Oil
    "oil": "Vegetable oil",

    "vegetable oil": "Vegetable oil",

    "avocado oil": "Avocado oil",



    # Seeds
    "mustard seeds": "Mustard seed",



    # Nuts
    "peanuts": "Peanuts, raw",



    # Vegetables
    "onion": "Onions, raw",

    "red onion": "Onions, raw",

    "potato": "Potatoes, raw",

    "peas": "Peas, green, raw",

    "green peas": "Peas, green, raw",



    # Herbs
    "cilantro": "Coriander leaves, raw",

    "coriander": "Coriander leaves, raw",

    "curry leaves": "Curry leaves",



    # Citrus
    "lemon": "Lemon juice, raw"

}





def normalize_ingredient(name):


    name = name.lower().strip()


    for key,value in INGREDIENT_MAP.items():

        if key in name:

            return value



    return name





def clean_ingredients(quantity_output):


    cleaned=[]


    for item in quantity_output:


        name = item.get(
            "name",
            ""
        )


        grams = item.get(
            "grams",
            0
        )


        cleaned.append({

            "original":
            item.get(
                "original",
                ""
            ),


            "name":
            name,


            "usda_name":
            normalize_ingredient(name),


            "grams":
            grams

        })


    return cleaned




# wrapper used by manager_agent
def ingredient_agent(quantity_output):

    return clean_ingredients(quantity_output)
