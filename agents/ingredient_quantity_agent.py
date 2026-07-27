import re


#################################################
# CONVERSION TABLE
#################################################

UNIT_TO_GRAMS = {

    "cup": {
        "rice flakes": 100,
        "poha": 100,
        "rice": 200,
        "oil": 218,
        "peanuts": 146,
        "coconut": 80
    },

    "tablespoon": {
        "oil": 14,
        "peanuts": 9,
        "sugar": 12,
        "coconut": 6
    },

    "tbsp": {
        "oil": 14,
        "peanuts": 9,
        "sugar": 12,
        "coconut": 6
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

    "oil": "oil",

    "mustard": "mustard seeds",
    "mustard seeds": "mustard seeds",

    "cumin": "cumin",
    "jeera": "cumin",

    "hing": "asafoetida",

    "turmeric": "turmeric",

    "salt": "salt",

    "sugar": "sugar",

    "coconut": "coconut",

    "lemon": "lemon",

    "curry leaves": "curry leaves",

    "coriander": "coriander",

    "cilantro": "coriander"

}



#################################################
# FRACTION HANDLER
#################################################

def convert_fraction(value):

    value=value.strip()


    fractions={

        "½":0.5,
        "¼":0.25,
        "¾":0.75,
        "⅓":0.33,
        "⅔":0.66

    }


    total=0


    for symbol,num in fractions.items():

        if symbol in value:

            total += num

            value=value.replace(
                symbol,
                ""
            )


    try:

        if value.strip():

            total += float(value)

    except:

        pass


    if total==0:

        return 1


    return total



#################################################
# PARSE INGREDIENT
#################################################

def parse_ingredient(text):


    if not isinstance(text,str):

        return None


    original=text.lower()



    # skip unknown amounts

    if "as needed" in original or "as required" in original:

        return None



    food=None


    for key in FOOD_MAP:

        if key in original:

            food=FOOD_MAP[key]

            break



    if not food:

        return None



    #################################
    # quantity
    #################################

    quantity=1



    quantity_match=re.search(

        r"(\d*\s*[½¼¾⅓⅔]|\d+)",

        original

    )


    if quantity_match:

        quantity=convert_fraction(
            quantity_match.group(1)
        )



    #################################
    # unit
    #################################

    unit="piece"



    units=[

        "cups",
        "cup",

        "tablespoons",
        "tablespoon",
        "tbsp",

        "teaspoons",
        "teaspoon",
        "tsp"

    ]


    for u in units:

        if u in original:

            unit=u

            break



    #################################
    # grams
    #################################

    grams=0



    normalized_unit=unit.rstrip("s")



    if normalized_unit in UNIT_TO_GRAMS:


        table=UNIT_TO_GRAMS[
            normalized_unit
        ]


        grams = quantity * table.get(
            food,
            10
        )



    else:


        piece_weight={

            "potato":150,

            "onion":110,

            "lemon":50,

            "curry leaves":5,

            "coriander":5,

            "asafoetida":1

        }


        grams = (

            piece_weight.get(
                food,
                10
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
