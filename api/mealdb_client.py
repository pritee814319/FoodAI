import requests


BASE_URL = "https://www.themealdb.com/api/json/v1/1/search.php"


def search_recipes(food_name):

    response = requests.get(
        BASE_URL,
        params={"s": food_name},
        timeout=15
    )

    response.raise_for_status()

    data = response.json()

    return data.get("meals")