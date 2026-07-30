import requests
import streamlit as st
import os


USDA_URL = (
    "https://api.nal.usda.gov/fdc/v1/foods/search"
)



def get_usda_key():

    try:
        return st.secrets["USDA_API_KEY"]

    except:

        return os.getenv(
            "USDA_API_KEY"
        )



def search_usda(food):


    key = get_usda_key()


    if not key:
        print("NO USDA KEY")
        return None



    params = {

        "api_key": key,

        "query": food,

        "pageSize": 10

    }



    try:

        response = requests.get(
            USDA_URL,
            params=params,
            timeout=10
        )


        data = response.json()


        foods = data.get(
            "foods",
            []
        )


        if not foods:
            return None



        # prefer real nutrition databases

        preferred = [

            f for f in foods

            if f.get("dataType")
            in
            [
                "Foundation",
                "SR Legacy"
            ]

        ]



        if preferred:

            return preferred[0]



        return foods[0]



    except Exception as e:

        print(
            "USDA ERROR:",
            e
        )

        return None





def extract_nutrients(food):


    nutrients = {}


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



        nutrients[name] = value



    return nutrients





def normalize_name(name):


    mapping = {


        "rice flakes":
        "rice flakes",


        "poha":
        "rice flakes",


        "flattened rice":
        "rice flakes",


        "vegetable oil":
        "oil, vegetable",


        "oil":
        "oil, vegetable",


        "potato":
        "potatoes raw",


        "peas":
        "green peas raw",


        "onion":
        "onions raw",


        "peanuts":
        "peanuts raw"


    }


    return mapping.get(
        name.lower(),
        name
    )





def calculate_item(food, grams):


    nutrients = extract_nutrients(
        food
    )


    calories = (
        nutrients.get(
            "Energy",
            nutrients.get(
                "Energy (Atwater General Factors)",
                0
            )
        )
    )


    protein = nutrients.get(
        "Protein",
        0
    )


    carbs = nutrients.get(
        "Carbohydrate, by difference",
        nutrients.get(
            "Carbohydrates",
            0
        )
    )


    fat = nutrients.get(
        "Total lipid (fat)",
        0
    )


    fiber = nutrients.get(
        "Fiber, total dietary",
        0
    )


    sodium = nutrients.get(
        "Sodium, Na",
        0
    )



    factor = grams / 100



    return {


        "Calories (kcal)":
        round(
            calories * factor,
            2
        ),


        "Protein (g)":
        round(
            protein * factor,
            2
        ),


        "Carbohydrates (g)":
        round(
            carbs * factor,
            2
        ),


        "Fat (g)":
        round(
            fat * factor,
            2
        ),


        "Fiber (g)":
        round(
            fiber * factor,
            2
        ),


        "Sodium (mg)":
        round(
            sodium * factor,
            2
        )

    }






def ingredient_agent(
        ingredients
):


    print(
        "========== INGREDIENT AGENT =========="
    )


    total = {


        "Calories (kcal)":0,

        "Protein (g)":0,

        "Carbohydrates (g)":0,

        "Fat (g)":0,

        "Fiber (g)":0,

        "Sodium (mg)":0

    }



    details=[]



    for item in ingredients:


        name = normalize_name(
            item["name"]
        )


        grams = item["grams"]



        print(
            "SEARCH:",
            name,
            grams
        )



        food = search_usda(
            name
        )



        if not food:

            print(
                "NOT FOUND:",
                name
            )

            continue



        item_nutrition = calculate_item(
            food,
            grams
        )



        details.append({

            "Ingredient":
            name,

            "grams":
            grams,

            "nutrition":
            item_nutrition

        })



        for k,v in item_nutrition.items():

            total[k]+=v





    for k in total:

        total[k]=round(
            total[k],
            2
        )



    return {


        "Ingredients":

        details,


        "Total Nutrition":

        total

    }
