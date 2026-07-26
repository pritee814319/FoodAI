from api.usda_client import search_usda_food


BAD_WORDS = [
    "recipe",
    "about",
    "photo",
    "guide",
    "share",
    "comment",
    "review",
    "author",
    "subscribe",
    "published",
    "updated",
    "instagram",
    "facebook"
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

        if any(word in lower for word in BAD_WORDS):
            continue

        if "http" in lower:
            continue

        if text.lower() in seen:
            continue

        seen.add(text.lower())

        cleaned.append(text)


    return cleaned



def extract_nutrition(usda_result):

    nutrition = {

        "Calories (kcal)": 0,
        "Protein (g)": 0,
        "Carbohydrates (g)": 0,
        "Fat (g)": 0,
        "Fiber (g)": 0,
        "Sugar (g)": 0,
        "Sodium (mg)": 0

    }


    if not usda_result:
        return nutrition


    data = usda_result.get(
        "nutrition",
        {}
    )


    for key, value in data.items():

        name = key.lower()


        if "energy" in name:
            nutrition["Calories (kcal)"] = value

        elif "protein" in name:
            nutrition["Protein (g)"] = value

        elif "carbohydrate" in name:
            nutrition["Carbohydrates (g)"] = value

        elif "total lipid" in name:
            nutrition["Fat (g)"] = value

        elif "fiber" in name:
            nutrition["Fiber (g)"] = value

        elif "sugar" in name:
            nutrition["Sugar (g)"] = value

        elif "sodium" in name:
            nutrition["Sodium (mg)"] = value


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

        "Calories (kcal)": 0,
        "Protein (g)": 0,
        "Carbohydrates (g)": 0,
        "Fat (g)": 0,
        "Fiber (g)": 0,
        "Sugar (g)": 0,
        "Sodium (mg)": 0

    }



    for ingredient in ingredients:

if len(ingredient.split()) > 12:
    continue
        try:

            print(
                "USDA SEARCH:",
                ingredient
            )


            result = search_usda_food(
                ingredient
            )


            nutrition = extract_nutrition(
                result
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

        "Ingredients Used": ingredients,

        "Total Nutrition": total

    }
