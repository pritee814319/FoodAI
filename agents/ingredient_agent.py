# agents/ingredient_agent.py

import re


INGREDIENT_MAP = {

    "poha": "Rice, white, flakes, cooked",
    "rice flakes": "Rice, white, flakes",
    "flattened rice": "Rice, white, flakes",

    "turmeric": "Spices, turmeric, ground",

    "salt": "Salt, table",

    "sugar": "Sugar, granulated",

    "oil": "Oil, vegetable",
    "vegetable oil": "Oil, vegetable",

    "mustard seeds": "Seeds, mustard",

    "peanuts": "Peanuts, all types, raw",

    "onion": "Onions, raw",

    "red onion": "Onions, raw",

    "curry leaves": "Curry leaves, raw",

    "potato": "Potatoes, flesh and skin, raw",

    "peas": "Peas, green, raw",

    "green peas": "Peas, green, raw",

    "cilantro": "Coriander leaves, raw",

    "lemon": "Lemon, raw, without peel",

}


def normalize_ingredient(name):

    name=name.lower().strip()


    for key,value in INGREDIENT_MAP.items():

        if key in name:
            return value


    return name



def clean_ingredients(quantity_output):

    cleaned=[]


    for item in quantity_output:

        name=item["name"]

        grams=item["grams"]


        normalized=normalize_ingredient(name)


        cleaned.append({

            "original":item["original"],

            "name":name,

            "usda_name":normalized,

            "grams":grams

        })


    return cleaned
