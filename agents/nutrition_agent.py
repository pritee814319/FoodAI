from api.usda_client import search_usda_food


def nutrition_agent(food):

    try:

        result = search_usda_food(food)


        # USDA error handling
        if "error" in result:

            return {

                "food": food,

                "nutrition": {},

                "message": result["error"]

            }


        return {

            "food": result.get(
                "food",
                food
            ),

            "nutrition": result.get(
                "nutrition",
                {}
            ),

            "source": result.get(
                "source",
                "USDA FoodData Central"
            )

        }


    except Exception as e:

        return {

            "food": food,

            "nutrition": {},

            "error": str(e)

        }
