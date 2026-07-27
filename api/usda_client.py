import os
import requests


USDA_API_KEY = os.getenv("USDA_API_KEY")


BASE_URL = (
    "https://api.nal.usda.gov/fdc/v1/foods/search"
)



def search_usda_food(food):


    print("============================")
    print("USDA LOOKUP:", food)
    print("============================")


    if not USDA_API_KEY:

        print("ERROR: USDA KEY MISSING")

        return None



    params = {

        "api_key": USDA_API_KEY,

        "query": food,

        "pageSize": 1

    }



    try:


        response = requests.get(
            BASE_URL,
            params=params,
            timeout=10
        )


        print(
            "USDA STATUS:",
            response.status_code
        )


        data = response.json()



        print(
            "USDA RESPONSE KEYS:",
            data.keys()
        )



        foods = data.get(
            "foods",
            []
        )



        if not foods:

            print(
                "NO USDA FOOD FOUND:",
                food
            )

            return None



        food_item = foods[0]



        print(
            "USDA FOUND:",
            food_item.get("description")
        )



        nutrients = {}



        for nutrient in food_item.get(
            "foodNutrients",
            []
        ):


            name = nutrient.get(
                "nutrientName",
                ""
            )


            value = nutrient.get(
                "value",
                0
            )


            nutrients[name] = value



        print(
            "NUTRIENTS:",
            nutrients
        )



        return {


            "name":
                food_item.get(
                    "description"
                ),


            "nutrition":
                nutrients

        }



    except Exception as e:


        print(
            "USDA ERROR:",
            e
        )


        return None
