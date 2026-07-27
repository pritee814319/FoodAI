import re


#################################################
# CONVERSION TABLE
#################################################

UNIT_TO_GRAMS = {

    "cup": {
        "poha": 100,
        "rice flakes": 100,
        "rice": 200,
        "oil": 218,
        "peanuts": 146,
        "coconut": 80
    },

    "tablespoon": {
        "oil": 14,
        "peanuts": 9,
        "sugar": 12
    },

    "tbsp": {
        "oil": 14,
        "peanuts": 9,
        "sugar": 12
    },

    "teaspoon": {

        "salt": 6,

        "sugar": 4,

        "oil": 4,

        "mustard seeds": 2,

        "cumin": 2,

        "turmeric": 2

    },

    "tsp": {

        "salt": 6,

        "sugar": 4,

        "oil": 4,

        "mustard seeds": 2,

        "cumin": 2,

        "turmeric": 2

    }

}



#################################################
# FOOD NORMALIZATION
#################################################

FOOD_MAP = {

    "poha": "rice flakes",

    "beaten rice": "rice flakes",

    "flattened rice": "rice flakes",

    "peanut": "peanuts",

    "peanuts": "peanuts",

    "onion": "onion",

    "potato": "potato",

    "oil": "vegetable oil",

    "mustard": "mustard seeds",

    "cumin": "cumin",

    "jeera": "cumin",

    "hing": "asafoetida",

    "turmeric": "turmeric",

    "salt": "salt",

    "sugar": "sugar"

}



#################################################
# FRACTION HANDLER
#################################################

def convert_fraction(value):


    value=value.strip()


    fractions = {

        "½":0.5,

        "¼":0.25,

        "¾":0.75,

        "⅓":0.33,

        "⅔":0.66

    }


    for symbol,num in fractions.items():

        if symbol in value:

            value=value.replace(
                symbol,
                ""
            )

            try:

                return float(value or 0)+num

            except:

                return num



    try:

        return float(value)

    except:

        return 1





#################################################
# PARSE INGREDIENT
#################################################

def parse_ingredient(text):


    if not isinstance(text,str):

        return None



    original=text.lower()



    ################################
    # Find food name
    ################################


    food=None


    for key in FOOD_MAP:


        if key in original:

            food=FOOD_MAP[key]

            break



    if not food:

        return None



    ################################
    # Find quantity
    ################################


    quantity_match=re.search(

        r"(\d+\s*[½¼¾⅓⅔]?)",

        original

    )


    if quantity_match:

        quantity=convert_fraction(
            quantity_match.group(1)
        )

    else:

        quantity=1





    ################################
    # Find unit
    ################################


    unit="piece"


    for u in [

        "cup",

        "cups",

        "tbsp",

        "tablespoon",

        "tablespoons",

        "tsp",

        "teaspoon",

        "teaspoons"

    ]:

        if u in original:

            unit=u

            break





    ################################
    # Convert grams
    ################################


    grams=0



    if unit in UNIT_TO_GRAMS:


        table=UNIT_TO_GRAMS[unit]


        if food in table:

            grams = quantity * table[food]

        else:

            grams = quantity * 10



    else:


        # pieces

        piece_weight={

            "potato":150,

            "onion":110,

            "lemon":50,

            "curry leaves":5

        }


        grams = (

            piece_weight.get(
                food,
                50
            )
            *
            quantity

        )





    return {


        "original": text,

        "name": food,

        "grams": round(
            grams,
            2
        )

    }





#################################################
# MAIN AGENT
#################################################

def ingredient_quantity_agent(ingredients):


    result=[]


    print(
        "QUANTITY INPUT:",
        ingredients
    )



    for item in ingredients:


        parsed=parse_ingredient(
            item
        )


        if parsed:

            result.append(
                parsed
            )



    print(
        "QUANTITY OUTPUT:",
        result
    )



    return result
