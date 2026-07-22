from agents.recipe_agent import recipe_agent
from agents.ingredient_agent import ingredient_agent


def manager_agent(food):

    print("START MANAGER:", food)


    recipes = recipe_agent(food)

    print("RECIPES FOUND:", len(recipes) if recipes else 0)


    if recipes and isinstance(recipes, list):

        first_recipe = recipes[0]

        print("FIRST RECIPE:", first_recipe["Recipe"])


        ingredients = first_recipe.get(
            "Ingredients",
            []
        )

        print("INGREDIENT COUNT:", len(ingredients))


        nutrition = ingredient_agent(
            ingredients
        )

        print("NUTRITION DONE")


        return {
            "query": food,
            "recipes": recipes,
            "nutrition": nutrition
        }


    return {
        "error": "No recipe found"
    }
