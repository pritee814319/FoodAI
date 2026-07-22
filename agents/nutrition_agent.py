from api.usda_client import search_food


def nutrition_agent(food):

    result = search_food(food)

    if not result:
        return {
            "error": "Food not found"
        }

    nutrients = {}

    for item in result["foodNutrients"]:
        name = item["nutrientName"]
        value = item["value"]

        nutrients[name] = value

    return {
        "food": result["description"],
        "nutrition": nutrients,
        "source": "USDA FoodData Central"
    }