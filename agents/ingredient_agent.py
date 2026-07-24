import re
from api.usda_client import get_food_nutrition



BAD_WORDS = [

    "recipe",
    "about",
    "photo",
    "guide",
    "share",
    "comment",
    "review",
    "faq",
    "table",
    "contents",
    "more",
    "breakfast recipes",
    "tips",
    "variation",
    "instruction",
    "method",
    "how to make",
    "published",
    "updated"

]



def clean_ingredients(items):


    cleaned = []

    seen = set()



    for item in items:


        if not isinstance(
            item,
            str
        ):

            continue



        text = item.strip()



        if len(text) < 3:

            continue



        lower = text.lower()



        # remove unwanted webpage text

        if any(
            word in lower
            for word in BAD_WORDS
        ):

            continue



        # remove urls

        if "http" in lower:

            continue



        # remove social/share numbers

        if re.search(
            r"\d+k\s*shares",
            lower
        ):

            continue



        # remove duplicates

        if text.lower() in seen:

            continue



        seen.add(
            text.lower()
        )


        cleaned.append(
            text
        )



    return cleaned





def ingredient_agent(ingredients):


    print(
        "RAW INGREDIENT COUNT:",
        len(ingredients)
    )



    ingredients = clean_ingredients(
        ingredients
    )



    print(
        "CLEAN INGREDIENT COUNT:",
        len(ingredients)
    )



    print(
        "CLEAN INGREDIENTS:"
    )


    for item in ingredients:

        print(
            item
        )



    total = {


        "Calories (kcal)":0,

        "Protein (g)":0,

        "Carbohydrates (g)":0,

        "Fat (g)":0,

        "Fiber (g)":0,

        "Sugar (g)":0,

        "Sodium (mg)":0

    }




    for ingredient in ingredients:


        try:


            nutrition = get_food_nutrition(
                ingredient
            )



            if nutrition:


                total["Calories (kcal)"] += nutrition.get(
                    "Calories (kcal)",
                    0
                )


                total["Protein (g)"] += nutrition.get(
                    "Protein (g)",
                    0
                )


                total["Carbohydrates (g)"] += nutrition.get(
                    "Carbohydrates (g)",
                    0
                )


                total["Fat (g)"] += nutrition.get(
                    "Fat (g)",
                    0
                )


                total["Fiber (g)"] += nutrition.get(
                    "Fiber (g)",
                    0
                )


                total["Sugar (g)"] += nutrition.get(
                    "Sugar (g)",
                    0
                )


                total["Sodium (mg)"] += nutrition.get(
                    "Sodium (mg)",
                    0
                )



        except Exception as e:


            print(
                "Nutrition error:",
                ingredient,
                e
            )




    # round values

    for key in total:


        total[key] = round(
            total[key],
            2
        )



    return {


        "Ingredients Used":

        ingredients,


        "Total Nutrition":

        total

    }
