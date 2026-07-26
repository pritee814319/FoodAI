import re

from api.usda_client import search_usda_food


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
    "published",
    "updated",
    "author",
    "subscribe",
    "cook",
    "serve",
    "instruction",
    "method",
    "step"
]


def clean_ingredients(items):

    cleaned = []

    seen = set()


    for item in items:

        if not isinstance(item, str):
            continue


        text = item.strip()


        if len(text) < 3:
            continue


        lower = text.lower()


        # remove sentences
        if len(text.split()) > 12:
            continue


        if any(word in lower for word in BAD_WORDS):
            continue


        # must contain measurement
        measurement = re.search(
            r"\b\d+(\.\d+)?\s?(cup|tbsp|tsp|g|kg|gram|ml|oz|lb|tablespoon|teaspoon)\b",
            lower
        )


        if not measurement:
            continue


        if text.lower() in seen:
            continue


        seen.add(text.lower())

        cleaned.append(text)



    return cleaned





def extract_nutrition(data):


    nutrition = {

        "Calories (kcal)":0,
        "Protein (g)":0,
        "Carbohydrates (g)":0,
        "Fat (g)":0,
        "Fiber (g)":0,
        "Sugar (g)":0,
        "Sodium (mg)":0

    }


    if not data:
        return nutrition



    usda = data.get(
        "nutrition",
        {}
    )



    for name,value in usda.items():

        key=name.lower()


        if "energy" in key:
            nutrition["Calories (kcal)"] = value


        elif "protein" in key:
            nutrition["Protein (g)"] = value


        elif "carbohydrate" in key:
            nutrition["Carbohydrates (g)"] = value


        elif "lipid" in key or "fat" in key:
            nutrition["Fat (g)"] = value


        elif "fiber" in key:
            nutrition["Fiber (g)"] = value


        elif "sodium" in key:
            nutrition["Sodium (mg)"] = value


        elif "sugar" in key:
            nutrition["Sugar (g)"] = value



    return nutrition





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
                "USDA SEARCH:",
                ingredient
            )

if len(ingredient.split()) > 8:
    continue
    
            result = search_usda_food(
                ingredient
            )


            nutrition = extract_nutrition(
                result
            )


            for key in total:

                total[key]+=nutrition[key]


            used.append(
                ingredient
            )


        except Exception as e:

            print(
                "Nutrition error:",
                ingredient,
                e
            )



    for key in total:

        total[key]=round(
            total[key],
            2
        )



    return {

        "Ingredients Used":used,

        "Total Nutrition":total

    }
