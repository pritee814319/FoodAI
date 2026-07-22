from api.usda_client import search_food


def get_nutrient_value(nutrients, name):

    for nutrient in nutrients:

        if nutrient["nutrientName"] == name:
            return nutrient["value"]

    return 0



def nutrition_agent(food, grams=100):

    result = search_food(food)

    if not result:
        return {
            "error": "Food not found"
        }


    nutrients = result["foodNutrients"]


    multiplier = grams / 100


    nutrition_report = {

        "Food": result["description"],

        "Serving Size (g)": grams,


        "Calories (kcal)": round(
            get_nutrient_value(
                nutrients,
                "Energy"
            ) * multiplier,
            2
        ),


        "Protein (g)": round(
            get_nutrient_value(
                nutrients,
                "Protein"
            ) * multiplier,
            2
        ),


        "Carbohydrates (g)": round(
            get_nutrient_value(
                nutrients,
                "Carbohydrate, by difference"
            ) * multiplier,
            2
        ),


        "Fat (g)": round(
            get_nutrient_value(
                nutrients,
                "Total lipid (fat)"
            ) * multiplier,
            2
        ),


        "Fiber (g)": round(
            get_nutrient_value(
                nutrients,
                "Fiber, total dietary"
            ) * multiplier,
            2
        ),


        "Sugar (g)": round(
            get_nutrient_value(
                nutrients,
                "Total Sugars"
            ) * multiplier,
            2
        ),


        "Sodium (mg)": round(
            get_nutrient_value(
                nutrients,
                "Sodium, Na"
            ) * multiplier,
            2
        ),


        "Source": "USDA FoodData Central"
    }


    return nutrition_report
