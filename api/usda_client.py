import os
import requests


def search_usda_food(food):

    key = os.getenv("USDA_API_KEY")

    print("USDA KEY EXISTS:", bool(key))
    print("SEARCHING USDA:", food)


    url = "https://api.nal.usda.gov/fdc/v1/foods/search"


    params = {
        "api_key": key,
        "query": food,
        "pageSize": 1
    }


    response = requests.get(
        url,
        params=params,
        timeout=10
    )


    print("STATUS:", response.status_code)

    print(
        "RAW RESPONSE:",
        response.text[:500]
    )


    if response.status_code != 200:
        return None



    data = response.json()


    foods = data.get(
        "foods",
        []
    )


    if not foods:
        print("NO FOOD FOUND")
        return None



    item = foods[0]


    print(
        "FOUND:",
        item.get("description")
    )


    nutrients = {}


    for n in item.get(
        "foodNutrients",
        []
    ):

        nutrients[
            n.get("nutrientName")
        ] = n.get(
            "value"
        )


    print(
        "NUTRIENTS:",
        nutrients
    )


    return {

        "nutrition": nutrients

    }
