from agents.recipe_search import recipe_search_agent
from agents.recipe_parser_agent import recipe_parser_agent
from agents.ingredient_agent import ingredient_agent


def divide_nutrition(total, people):

    if not total:
        return {}

    return {
        k: round(v / people, 2)
        for k, v in total.items()
    }



def manager_agent(food_name, people):

    print(
        "MANAGER START:",
        food_name
    )


    # -----------------------------------
    # Search recipes
    # -----------------------------------

    search_result = recipe_search_agent(
        food_name
    )


    recipes = search_result.get(
        "recipes",
        []
    )


    final_recipes = []


    # -----------------------------------
    # Parse recipes
    # -----------------------------------

    for recipe in recipes:

        parsed = recipe_parser_agent(
            recipe
        )


        if parsed.get("Ingredients"):

            final_recipes.append(
                parsed
            )


    if not final_recipes:

        return {

            "recipes": [],

            "nutrition": {

                "Total Recipe Nutrition": {},

                "Nutrition Per Person": {}

            }

        }



    # -----------------------------------
    # Calculate nutrition
    # using first complete recipe
    # -----------------------------------

    first_recipe = final_recipes[0]


    nutrition = ingredient_agent(
        first_recipe["Ingredients"]
    )


    total = nutrition.get(
        "Total Nutrition",
        {}
    )


    return {


        "query": food_name,


        "servings": people,


        "recipes": final_recipes,


        "nutrition": {


            "Total Recipe Nutrition":

            total,


            "Nutrition Per Person":

            divide_nutrition(
                total,
                people
            )

        }

    }
