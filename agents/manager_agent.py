from agents.recipe_agent import recipe_agent
from agents.nutrition_agent import nutrition_agent


def manager_agent(food, grams=100):

    result = {
        "query": food,
        "recipe": None,
        "nutrition": None
    }

    # Get recipes
    recipes = recipe_agent(food)

    result["recipe"] = recipes

    # Get nutrition
    nutrition = nutrition_agent(food, grams)

    result["nutrition"] = nutrition

    return result