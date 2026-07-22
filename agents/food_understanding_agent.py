
import difflib


# Common food correction dictionary
# We can expand this later
FOOD_CORRECTIONS = {

    "chicken hundi": "Chicken Handi",
    "chiken handi": "Chicken Handi",
    "chiken hundi": "Chicken Handi",

    "butter chiken": "Butter Chicken",
    "buter chicken": "Butter Chicken",

    "biriyani": "Biryani",
    "biriyani rice": "Biryani",

    "piza": "Pizza",
    "pizaa": "Pizza",

    "pasta carbonara": "Pasta Carbonara",

    "tacos": "Tacos",

    "sushi": "Sushi"

}



def food_understanding_agent(food):

    original = food.strip()


    if not original:

        return {

            "original": "",
            "corrected": "",
            "confidence": 0

        }


    # normalize
    cleaned = original.lower()


    # Exact correction
    if cleaned in FOOD_CORRECTIONS:

        return {

            "original": original,

            "corrected": FOOD_CORRECTIONS[cleaned],

            "confidence": 1.0

        }



    # Try fuzzy matching
    match = difflib.get_close_matches(

        cleaned,

        FOOD_CORRECTIONS.keys(),

        n=1,

        cutoff=0.7

    )


    if match:

        return {

            "original": original,

            "corrected": FOOD_CORRECTIONS[match[0]],

            "confidence": 0.8

        }



    # If no correction needed
    return {

        "original": original,

        "corrected": original.title(),

        "confidence": 0.5

    }
