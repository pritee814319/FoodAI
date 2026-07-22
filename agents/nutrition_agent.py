from api.usda_client import search_food


def get_nutrient_value(nutrients, name):

    for nutrient in nutrients:

        if nutrient["nutrientName"] == name:
            return nutrient["value"]

    return 0



def nutrition_agent(food):

    result = search_food(food)

    if not result:
        return {
            "error": "Food not found"
        }


    nutrients = result["foodNutrients"]


    nutrition_report = {

        "Food": result["description"],

        "Calories (kcal)": get_nutrient_value(
            nutrients,
            "Energy"
        ),

        "Protein (g)": get_nutrient_value(
            nutrients,
            "Protein"
        ),

        "Carbohydrates (g)": get_nutrient_value(
            nutrients,
            "Carbohydrate, by difference"
        ),

        "Fat (g)": get_nutrient_value(
            nutrients,
            "Total lipid (fat)"
        ),

        "Fiber (g)": get_nutrient_value(
            nutrients,
            "Fiber, total dietary"
        ),

        "Sugar (g)": get_nutrient_value(
            nutrients,
            "Total Sugars"
        ),

        "Sodium (mg)": get_nutrient_value(
            nutrients,
            "Sodium, Na"
        ),

        "Source": "USDA FoodData Central"
    }


    return nutrition_report
