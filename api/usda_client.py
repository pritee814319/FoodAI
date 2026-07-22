import os
import requests


USDA_API_KEY = os.getenv("USDA_API_KEY")


def search_usda_food(food):

    url = "https://api.nal.usda.gov/fdc/v1/foods/search"


    params = {

        "api_key": USDA_API_KEY,

        "query": food,

        "pageSize": 1

    }


    response = requests.get(
        url,
        params=params
    )


    print(
        "USDA STATUS:",
        response.status_code
    )


    if response.status_code != 200:

        return {

            "error": "USDA API error",

            "status": response.status_code,

            "details": response.text

        }


    data = response.json()


    foods = data.get(
        "foods",
        []
    )


    if not foods:

        return {

            "error": "Food not found"

        }


    food_data = foods[0]


    nutrients = food_data.get(
        "foodNutrients",
        []
    )


    nutrition = {}


    for item in nutrients:


        nutrient_name = item.get(
            "nutrientName"
        )


        value = item.get(
            "value",
            0
        )


        if nutrient_name:

            nutrition[nutrient_name] = value



    return {

        "food": food_data.get(
            "description",
            food
        ),

        "nutrition": nutrition,

        "source": "USDA FoodData Central"

    }
