import re

from api.usda_client import search_usda_food


# ---------------------------------------------------
# Words that indicate recipe/article text
# ---------------------------------------------------

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
    "tips",
    "variation",
    "published",
    "updated",
    "author",
    "subscribe",

    "popular",
    "traditional",
    "method",
    "process",
    "dish",
    "cook",
    "serve",
    "enjoy",
    "learn",
    "best",
    "story",
    "introduction",
    "instruction"

]


# ---------------------------------------------------
# Remove bad recipe text
# ---------------------------------------------------

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


        # Remove article text

        if any(
            word in lower
            for word in BAD_WORDS
        ):

            continue


        if "http" in lower:

            continue


        # Remove very long sentences

        if len(text.split()) > 12:

            continue


        key = text.lower()


        if key in seen:

            continue


        seen.add(key)


        cleaned.append(text)



    return cleaned



# ---------------------------------------------------
# Convert recipe ingredient into food name
# Example:
# "2 cups poha" -> "poha"
# "1 tbsp oil" -> "oil"
# ---------------------------------------------------

def normalize_ingredient(text):


    text = text.lower()


    # remove numbers

    text = re.sub(
        r"\d+[\d\/\.\s]*",
        "",
        text
    )


    units = [

        "cups",
        "cup",
        "tablespoons",
        "tablespoon",
        "tbsp",
        "teaspoons",
        "teaspoon",
        "tsp",
        "grams",
        "gram",
        "kg",
        "ml",
        "oz",
        "lb"

    ]


    for unit in units:

        text = text.replace(
            unit,
            ""
        )


    # remove symbols

    text = re.sub(
        r"[^a-z\s]",
        "",
        text
    )


    return text.strip()



# ---------------------------------------------------
# Extract USDA nutrition
# ---------------------------------------------------

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



    if "nutrition" not in usda_result:

        return nutrition



    data = usda_result["nutrition"]



    for key, value in data.items():


        key_lower = key.lower()



        if "energy" in key_lower:

            nutrition["Calories (kcal)"] = value


        elif "protein" in key_lower:

            nutrition["Protein (g)"] = value


        elif "carbohydrate" in key_lower:

            nutrition["Carbohydrates (g)"] = value


        elif "total lipid" in key_lower:

            nutrition["Fat (g)"] = value


        elif "fiber" in key_lower:

            nutrition["Fiber (g)"] = value


        elif "sugars" in key_lower:

            nutrition["Sugar (g)"] = value


        elif "sodium" in key_lower:

            nutrition["Sodium (mg)"] = value



    return nutrition



# ---------------------------------------------------
# Main Ingredient Agent
# ---------------------------------------------------

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
        "\nFINAL INGREDIENTS SENT TO USDA:"
    )


    for item in ingredients:

        print(
            "-",
            item
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



    searched = set()



    for ingredient in ingredients:


        try:


            food_name = normalize_ingredient(
                ingredient
            )


            if not food_name:

                continue



            if food_name in searched:

                continue



            searched.add(
                food_name
            )


            print(
                "USDA SEARCH:",
                food_name
            )



            result = search_usda_food(
                food_name
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


        "Ingredients Used":

        ingredients,


        "Total Nutrition":

        total

    }
