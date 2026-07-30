from api.usda_client import search_usda_food


def nutrition_agent(ingredient):

    try:

        # Support both formats:
        # "potato"
        # {"name":"potato","grams":100}

        if isinstance(ingredient, dict):

            food = ingredient.get(
                "usda_name",
                ingredient.get("name")
            )

            grams = ingredient.get(
                "grams",
                100
            )

        else:

            food = ingredient
            grams = 100


        result = search_usda_food(food)


        if "error" in result:

            return {

                "ingredient": food,

                "grams": grams,

                "nutrition": {},

                "message": result["error"]

            }


        nutrition = result.get(
            "nutrition",
            {}
        )


        # Convert USDA per 100g values
        factor = grams / 100


        calculated = {

            "Calories (kcal)": round(
                nutrition.get("Calories (kcal)",0) * factor,
                2
            ),

            "Protein (g)": round(
                nutrition.get("Protein (g)",0) * factor,
                2
            ),

            "Carbohydrates (g)": round(
                nutrition.get("Carbohydrates (g)",0) * factor,
                2
            ),

            "Fat (g)": round(
                nutrition.get("Fat (g)",0) * factor,
                2
            ),

            "Fiber (g)": round(
                nutrition.get("Fiber (g)",0) * factor,
                2
            ),

            "Sugar (g)": round(
                nutrition.get("Sugar (g)",0) * factor,
                2
            ),

            "Sodium (mg)": round(
                nutrition.get("Sodium (mg)",0) * factor,
                2
            )

        }


        return {

            "ingredient": food,

            "grams": grams,

            "nutrition": calculated,

            "source": "USDA FoodData Central"

        }


    except Exception as e:


        return {

            "ingredient": str(ingredient),

            "nutrition": {},

            "error": str(e)

        }
