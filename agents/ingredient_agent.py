import os
import requests
import re


USDA_KEY = os.getenv("USDA_API_KEY")

USDA_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"



def clean_name(text):

    text = text.lower()

    text = re.sub(
        r"[^a-z\s]",
        "",
        text
    )

    remove = [
        "chopped",
        "finely",
        "diced",
        "fresh",
        "medium",
        "small",
        "large",
        "optional",
        "to taste"
    ]

    for word in remove:
        text = text.replace(
            word,
            ""
        )

    return text.strip()



def extract_quantity(text):

    """
    Convert recipe quantity into approximate grams
    """

    text = text.lower()


    # cups

    cup = re.search(
        r"(\d+\.?\d*)\s*(cup|cups)",
        text
    )

    if cup:

        return float(cup.group(1)) * 120



    # tablespoons

    tbsp = re.search(
        r"(\d+\.?\d*)\s*(tbsp|tablespoon)",
        text
    )

    if tbsp:

        return float(
            tbsp.group(1)
        ) * 15



    # teaspoons

    tsp = re.search(
        r"(\d+\.?\d*)\s*(tsp|teaspoon)",
        text
    )

    if tsp:

        return float(
            tsp.group(1)
        ) * 5



    # grams

    gram = re.search(
        r"(\d+)\s*g",
        text
    )

    if gram:

        return float(
            gram.group(1)
        )



    # default assumption

    return 100





def search_usda(food):


    try:

        response = requests.get(

            USDA_URL,

            params={

                "api_key": USDA_KEY,

                "query": food,

                "pageSize": 1

            },

            timeout=10

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
            "USDA ERROR",
            e
        )


    return None





def nutrients_from_food(food, grams):


    result = {

        "Calories (kcal)":0,

        "Protein (g)":0,

        "Carbohydrates (g)":0,

        "Fat (g)":0,

        "Fiber (g)":0,

        "Sugar (g)":0,

        "Sodium (mg)":0

    }


    if not food:

        return result



    factor = grams / 100



    for n in food.get(
        "foodNutrients",
        []
    ):


        name = n.get(
            "nutrientName",
            ""
        )


        value = n.get(
            "value",
            0
        )



        value = value * factor



        if name == "Energy":

            result["Calories (kcal)"] = round(value,2)


        elif name == "Protein":

            result["Protein (g)"] = round(value,2)


        elif name == "Carbohydrate, by difference":

            result["Carbohydrates (g)"] = round(value,2)


        elif name == "Total lipid (fat)":

            result["Fat (g)"] = round(value,2)


        elif name == "Fiber, total dietary":

            result["Fiber (g)"] = round(value,2)


        elif name == "Sugars, total including NLEA":

            result["Sugar (g)"] = round(value,2)


        elif name == "Sodium, Na":

            result["Sodium (mg)"] = round(value,2)



    return result





def ingredient_agent(ingredients):


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


        if not isinstance(item,str):

            continue



        name = clean_name(item)


        if not name:

            continue



        grams = extract_quantity(item)



        print(
            "INGREDIENT:",
            name,
            grams,
            "g"
        )



        food = search_usda(
            name
        )



        nutrition = nutrients_from_food(
            food,
            grams
        )



        for key in total:

            total[key] += nutrition[key]



    return {

        "Total Nutrition":

        {
            k:round(v,2)

            for k,v in total.items()

        }

    }
