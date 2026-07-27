import re


#################################################
# UNIT CONVERSION TABLE
#################################################

UNIT_TO_GRAMS = {

    "cup": {

        "rice flakes": 75,
        "peanuts": 146,
        "vegetable oil": 218,
        "coconut": 80

    },


    "cups": {

        "rice flakes": 100,
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

    "sugar": "sugar",


    "green peas": "peas",

    "peas": "peas",


    "coriander": "cilantro",

    "cilantro": "cilantro",


    "curry leaves": "curry leaves",


    "lemon": "lemon"

}



#################################################
# FRACTION CONVERSION
#################################################

def convert_fraction(value):


    value = value.strip()


    fractions = {

        "½":0.5,
        "¼":0.25,
        "¾":0.75,
        "⅓":0.33,
        "⅔":0.66

    }


    result = 0


    for symbol, number in fractions.items():

        if symbol in value:

            result += number

            value = value.replace(
                symbol,
                ""
            )


    try:

        result += float(value)

    except:

        pass


    if result == 0:

        result = 1


    return result



#################################################
# PARSE INGREDIENT
#################################################

def parse_ingredient(text):


    if not isinstance(text,str):

        return None


    original = text.lower()



    ################################
    # FIND FOOD
    ################################

    food = None


    for key in FOOD_MAP:


        if key in original:

            food = FOOD_MAP[key]

            break



    if not food:

        return None




    ################################
    # PRIORITY 1
    # USE PROVIDED GRAMS
    ################################

    gram_match = re.search(

        r"(\d+\.?\d*)\s*(grams|gram|g)",

        original

    )


    if gram_match:


        grams = float(
            gram_match.group(1)
        )


        return {

            "original": text,

            "name": food,

            "grams": round(
                grams,
                2
            )

        }



    ################################
    # QUANTITY
    ################################

    quantity_match = re.search(

        r"(\d+\.?\d*\s*[½¼¾⅓⅔]?)",

        original

    )


    if quantity_match:


        quantity = convert_fraction(

            quantity_match.group(1)

        )


    else:


        quantity = 1




    ################################
    # UNIT
    ################################

    unit = "piece"



    units = [

        "tablespoons",

        "tablespoon",

        "tbsp",

        "teaspoons",

        "teaspoon",

        "tsp",

        "cups",

        "cup"

    ]


    for u in units:


        if u in original:

            unit = u

            break




    ################################
    # CONVERT TO GRAMS
    ################################

    if unit in UNIT_TO_GRAMS:


        grams = (

            quantity *

            UNIT_TO_GRAMS[unit].get(

                food,

                10

            )

        )


    else:


        piece_weights = {

            "potato":150,

            "onion":110,

            "lemon":50,

            "curry leaves":5,

            "cilantro":5,

            "peas":100

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


    print(
        "========== QUANTITY AGENT =========="
    )


    print(
        "INPUT:",
        ingredients
    )



    output = []



    for item in ingredients:


        result = parse_ingredient(

            item

        )


        if result:

            output.append(

                result

            )



    print(

        "OUTPUT:",

        output

    )


    return output
