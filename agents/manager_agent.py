from agents.recipe_agent import recipe_agent
from agents.ingredient_agent import ingredient_agent


def manager_agent(food):

    result = {

        "query": food,

        "recipes": None,

        "nutrition": None

    }


    # Find recipes
    recipes = recipe_agent(food)

    result["recipes"] = recipes


    # Analyze nutrition from first recipe
    if recipes and isinstance(recipes, list):

        first_recipe = recipes[0]


        ingredients = first_recipe.get(
            "Ingredients",
            []
        )


        nutrition = ingredient_agent(
            ingredients
        )


        result["nutrition"] = nutrition


    else:

        result["nutrition"] = {
            "error": "No recipe found"
        }


    return result
