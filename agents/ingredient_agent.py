import os
import requests
import re



USDA_KEY = os.getenv(
    "USDA_API_KEY"
)



USDA_URL = (
    "https://api.nal.usda.gov/fdc/v1/foods/search"
)





def clean_ingredient_name(text):


    if not text:

        return ""



    text = text.lower()



    # remove bullets

    text = text.replace(
        "▢",
        ""
    )



    # remove fractions and numbers

    text = re.sub(

        r"\d+[\d\/½¼¾⅓⅔⅛⅜⅝⅞]*",

        "",

        text

    )



    # remove measurements

    measurements = [

        "cup",
        "cups",
        "tbsp",
        "tablespoon",
        "tablespoons",
        "tsp",
        "teaspoon",
        "teaspoons",
        "kg",
        "g",
        "gram",
        "grams",
        "ml",
        "inch",
        "clove",
        "cloves"

    ]



    for m in measurements:


        text = text.replace(

            m,

            ""

        )



    # remove cooking words

    remove_words = [

        "finely chopped",
        "chopped",
        "diced",
        "optional",
        "fresh",
        "small",
        "medium",
        "large",
        "to taste"

    ]



    for word in remove_words:


        text = text.replace(

            word,

            ""

        )



    text = re.sub(

        r"[^a-z\s]",

        "",

        text

    )


    return text.strip()





def search_usda(food):


    if not USDA_KEY:


        print(
            "NO USDA KEY"
        )

        return None




    try:


        response = requests.get(

            USDA_URL,

            params={

                "api_key":
                USDA_KEY,

                "query":
                food,

                "pageSize":
                1

            },

            timeout=15

        )



        data = response.json()



        foods = data.get(

            "foods",

            []

        )



        if foods:


            return foods[0]



    except Exception as e:


        print(
            "USDA ERROR:",
            e
        )



    return None





def get_nutrients(food):


    nutrients = {


        "Calories (kcal)":0,

        "Protein (g)":0,

        "Carbohydrates (g)":0,

        "Fat (g)":0,

        "Fiber (g)":0,

        "Sugar (g)":0,

        "Sodium (mg)":0

    }



    if not food:


        return nutrients




    for item in food.get(

        "foodNutrients",

        []

    ):


        name = item.get(

            "nutrientName",

            ""

        )



        value = item.get(

            "value",

            0

        )



        if name == "Energy":

            nutrients[
                "Calories (kcal)"
            ] = value



        elif name == "Protein":

            nutrients[
                "Protein (g)"
            ] = value



        elif name == "Carbohydrate, by difference":

            nutrients[
                "Carbohydrates (g)"
            ] = value



        elif name == "Total lipid (fat)":

            nutrients[
                "Fat (g)"
            ] = value



        elif name == "Fiber, total dietary":

            nutrients[
                "Fiber (g)"
            ] = value



        elif name == "Sugars, total including NLEA":

            nutrients[
                "Sugar (g)"
            ] = value



        elif name == "Sodium, Na":

            nutrients[
                "Sodium (mg)"
            ] = value



    return nutrients





def ingredient_agent(ingredients):


    print(
        "INGREDIENT AGENT START"
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



    for item in ingredients:



        clean_name = clean_ingredient_name(

            item

        )



        if not clean_name:


            continue



        print(

            "USDA SEARCH:",

            clean_name

        )



        food = search_usda(

            clean_name

        )



        nutrients = get_nutrients(

            food

        )



        for key in total:


            total[key] += nutrients[key]





    return {


        "Total Nutrition":

        total

    }
