def parse_ingredient(text):

    if not isinstance(text, str):
        return None


    original = text.lower()


    food = None


    for key in FOOD_MAP:

        if key in original:

            food = FOOD_MAP[key]
            break


    if not food:
        return None



    ################################
    # PRIORITY 1: USE PROVIDED GRAMS
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

    match = re.search(
        r"(\d+\.?\d*\s*[½¼¾⅓⅔]?)",
        original
    )


    if match:

        quantity = convert_fraction(
            match.group(1)
        )

    else:

        quantity = 1



    ################################
    # UNIT
    ################################

    unit = "piece"


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

            unit = u
            break



    ################################
    # GRAM CONVERSION
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

        "original": text,

        "name": food,

        "grams": round(
            grams,
            2
        )

    }
