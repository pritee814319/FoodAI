from agents.recipe_agent import recipe_agent
from agents.ingredient_agent import ingredient_agent


def divide_nutrition(total, people):

    per_person = {}

    for key, value in total.items():

        try:
            per_person[key] = round(
                value / people,
                2
            )

        except:
            per_person[key] = value

    return per_person



def manager_agent(food, people=4):

    print("START MANAGER:", food)

    result = {

        "query": food,

        "servings": people,

        "recipes": [],

        "nutrition": {}

    }


    # Get recipes
    recipes = recipe_agent(food)

    print(
        "RECIPES FOUND:",
        len(recipes) if isinstance(recipes, list) else 0
    )


    if not recipes or not isinstance(recipes, list):

        result["error"] = "No recipes found"

        return result


    # Use first recipe
    recipe = recipes[0]

    print(
        "FIRST RECIPE:",
        recipe.get("Recipe")
    )


    ingredients = recipe.get(
        "Ingredients",
        []
    )


    print(
        "INGREDIENT COUNT:",
        len(ingredients)
    )


    # Calculate nutrition
    nutrition = ingredient_agent(
        ingredients
    )


    print("NUTRITION DONE")


    total_nutrition = nutrition.get(
        "Total Nutrition",
        {}
    )


    per_person = divide_nutrition(
        total_nutrition,
        people
    )


    result["recipes"] = recipes


    result["nutrition"] = {

        "Total Recipe Nutrition": total_nutrition,

        f"Nutrition Per Person ({people} servings)": per_person

    }


    return result
