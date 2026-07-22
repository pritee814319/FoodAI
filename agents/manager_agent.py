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



def manager_agent(food, people):

    print("START MANAGER:", food)
    print("PEOPLE:", people)


    recipes = recipe_agent(food)


    if not recipes or not isinstance(recipes, list):

        return {
            "error": "No recipes found"
        }


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


    return {

        "query": food,

        "servings": people,

        "recipes": recipes,

        "nutrition": {

            "Total Recipe Nutrition": total_nutrition,

            "Nutrition Per Person": per_person

        }

    }
