from api.usda_client import search_usda_food
import re


BAD_WORDS = [

    "recipe",
    "step",
    "add",
    "cook",
    "heat",
    "mix",
    "serve",
    "garnish",
    "stir",
    "saute",
    "sauté",
    "instructions",
    "method",
    "time",
    "minutes",
    "optional",
    "note",
    "tip",
    "photo",
    "guide",
    "author",
    "subscribe",
    "comments"

]


def clean_ingredients(items):

    cleaned = []
    seen = set()


    for item in items:

        if not isinstance(item, str):
            continue


        text = item.strip()


        if len(text) < 5:
            continue


        lower = text.lower()


        # remove instructions
        if any(
            lower.startswith(word)
            for word in BAD_WORDS
        ):
            continue


        # remove sentences
        if len(text.split()) > 12:
            continue


        # remove pure measurements
        if re.match(
            r"^[0-9\s¼½¾/.-]+$",
            text
        ):
            continue


        # remove useless words
        if lower in [
            "cup",
            "cups",
            "tbsp",
            "tablespoon",
            "tablespoons",
            "tsp",
            "teaspoon",
            "teaspoons",
            "gram",
            "grams"
        ]:
            continue


        # remove duplicate
        if lower in seen:
            continue


        seen.add(lower)

        cleaned.append(text)



    return cleaned[:20]





def extract_nutrition(result):


    nutrition = {

        "Calories (kcal)":0,
        "Protein (g)":0,
        "Carbohydrates (g)":0,
        "Fat (g)":0,
        "Fiber (g)":0,
        "Sugar (g)":0,
        "Sodium (mg)":0

    }


    if not result:
        return nutrition


    data = result.get(
        "nutrition",
        {}
    )


    for key,value in data.items():

        k = key.lower()


        if "energy" in k:
            nutrition["Calories (kcal)"] = value


        elif "protein" in k:
            nutrition["Protein (g)"] = value


        elif "carbohydrate" in k:
            nutrition["Carbohydrates (g)"] = value


        elif "total lipid" in k:
            nutrition["Fat (g)"] = value


        elif "fiber" in k:
            nutrition["Fiber (g)"] = value


        elif "sodium" in k:
            nutrition["Sodium (mg)"] = value


    return nutrition





def ingredient_agent(ingredients):


    print(
        "RAW INGREDIENTS:",
        len(ingredients)
    )


    ingredients = clean_ingredients(
        ingredients
    )


    print(
        "CLEAN INGREDIENTS:",
        ingredients
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



    used=[]


    for ingredient in ingredients:


        try:

            print(
                "USDA:",
                ingredient
            )


            result = search_usda_food(
                ingredient
            )


            nutrition = extract_nutrition(
                result
            )


            # ignore failed USDA matches
            if nutrition["Calories (kcal)"] == 0:
                continue


            used.append(
                ingredient
            )


            for key in total:

                total[key] += nutrition[key]



        except Exception as e:

            print(
                "Nutrition error:",
                ingredient,
                e
            )



    for key in total:

        total[key] = round(
            total[key],
            2
        )



    return {

        "Ingredients Used": used,

        "Total Nutrition": total

    }
