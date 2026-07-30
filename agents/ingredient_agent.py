# agents/ingredient_agent.py


INGREDIENT_MAP = {

    "poha": "Rice flakes, dry",
    "rice flakes": "Rice flakes, dry",
    "flattened rice": "Rice flakes, dry",

    "turmeric": "Turmeric, ground",

    "salt": "Salt, table",

    "sugar": "Sugar, granulated",

    "oil": "Vegetable oil",
    "vegetable oil": "Vegetable oil",

    "mustard seeds": "Mustard seed",

    "peanuts": "Peanuts, raw",

    "onion": "Onions, raw",
    "red onion": "Onions, raw",

    "curry leaves": "Curry leaves",

    "potato": "Potatoes, raw",

    "peas": "Peas, green, raw",
    "green peas": "Peas, green, raw",

    "cilantro": "Coriander leaves, raw",

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

        name=item.get("name","")

        grams=item.get("grams",0)


        cleaned.append({

            "original": item.get("original",""),

            "name": name,

            "usda_name": normalize_ingredient(name),

            "grams": grams

        })


    return cleaned




# Manager agent calls this function
def ingredient_agent(quantity_output):

    return clean_ingredients(quantity_output)
