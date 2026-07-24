from agents.recipe_search import recipe_search_agent
from agents.ingredient_agent import ingredient_agent


def divide_nutrition(total, people):

    per_person = {}

    for key, value in total.items():

        try:
            per_person[key] = round(value / people, 2)
        except Exception:
            per_person[key] = value

    return per_person


def manager_agent(food, people):

    print("START MANAGER:", food)

    search_result = recipe_search_agent(food)

    recipes = search_result.get("recipes", [])

    if not recipes:

        return {
            "error": "No recipes found"
        }

    recipe = recipes[0]

    ingredients = recipe.get(
        "Ingredients",
        []
    )

    # Web recipes don't have ingredients yet
    if not ingredients:

        return {

            "query": food,

            "servings": people,

            "recipes": recipes,

            "nutrition": {}

        }

    nutrition = ingredient_agent(
        ingredients
    )

    total = nutrition.get(
        "Total Nutrition",
        {}
    )

    return {

        "query": food,

        "servings": people,

        "recipes": recipes,

        "nutrition": {

            "Total Recipe Nutrition": total,

            "Nutrition Per Person": divide_nutrition(
                total,
                people
            )

        }

    }
