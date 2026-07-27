import re


#################################################
# UNIT CONVERSION TABLE
#################################################

UNIT_TO_GRAMS = {

    "cup": {
        "rice flakes": 100,
        "poha": 100,
        "peanuts": 146,
        "vegetable oil": 218,
        "coconut": 80
    },

    "cups": {
        "rice flakes": 100,
        "poha": 100,
        "peanuts": 146,
        "vegetable oil": 218,
        "coconut": 80
    },


    "tablespoon": {

        "vegetable oil": 14,
        "peanuts": 9,
        "sugar": 12,
        "coconut": 5

    },


    "tablespoons": {

        "vegetable oil": 14,
        "peanuts": 9,
        "sugar": 12,
        "coconut": 5

    },


    "tbsp": {

        "vegetable oil": 14,
        "peanuts": 9,
        "sugar": 12,
        "coconut": 5

    },


    "teaspoon": {

        "salt": 6,
        "sugar": 4,
        "mustard seeds": 2,
        "cumin": 2,
        "turmeric": 2

    },


    "teaspoons": {

        "salt": 6,
        "sugar": 4,
        "mustard seeds": 2,
        "cumin": 2,
        "turmeric": 2

    },


    "tsp": {

        "salt": 6,
        "sugar": 4,
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

    "flattened rice": "rice flakes",

    "beaten rice": "rice flakes",

    "rice flakes": "rice flakes",


    "peanut": "peanuts",

    "peanuts": "peanuts",


    "oil": "vegetable oil",

    "vegetable oil": "vegetable oil",


    "mustard": "mustard seeds",

    "mustard seeds": "mustard seeds",


    "cumin": "cumin",

    "jeera": "cumin",

    "cumin seeds": "cumin",


    "potato": "potato",

    "onion": "onion",


    "turmeric": "turmeric",

    "salt": "salt",

    "sugar": "sugar"

}




#################################################
# FRACTION CONVERSION
#################################################

def convert_fraction(value):


    fractions = {

        "½":0.5,
        "¼":0.25,
        "¾":0.75,
        "⅓":0.33,
        "⅔":0.66

    }


    number = 0


    for symbol,amount in fractions.items():

        if symbol in value:

            number += amount

            value=value.replace(symbol,"")



    try:

        number += float(value)

    except:

        pass



    if number == 0:

        number = 1



    return number




#################################################
# PARSE INGREDIENT
#################################################

def parse_ingredient(text):


    if not isinstance(text,str):

        return None



    original=text.lower()



    food=None



    for key in FOOD_MAP:


        if key in original:

            food=FOOD_MAP[key]

            break



    if not food:

        return None




    # quantity

    match=re.search(
        r"(\d+\.?\d*\s*[½¼¾⅓⅔]?)",
        original
    )


    if match:

        quantity=convert_fraction(
            match.group(1)
        )

    else:

        quantity=1





    unit="piece"



    for u in [

        "cups",
        "cup",
        "tablespoons",
        "tablespoon",
        "tbsp",
        "teaspoons",
        "teaspoon",
        "tsp"

    ]:


        if u in original:

            unit=u

            break





    grams=0



    if unit in UNIT_TO_GRAMS:


        grams = (
            quantity *
            UNIT_TO_GRAMS[unit].get(
                food,
                10
            )
        )



    else:


        piece_weights={

            "potato":150,

            "onion":110,

            "lemon":50

        }


        grams = (

            piece_weights.get(
                food,
                5
            )

            *

            quantity

        )




    return {

        "original":text,

        "name":food,

        "grams":round(
            grams,
            2
        )

    }




#################################################
# MAIN AGENT
#################################################

def ingredient_quantity_agent(ingredients):


    print(
        "========== QUANTITY AGENT =========="
    )


    print(
        "INPUT:",
        ingredients
    )


    output=[]



    for item in ingredients:


        result=parse_ingredient(item)


        if result:

            output.append(result)



    print(
        "OUTPUT:",
        output
    )


    return output
