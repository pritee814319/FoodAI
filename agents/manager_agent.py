from agents.recipe_search import recipe_search_agent
from agents.recipe_parser_agent import recipe_parser_agent
from agents.ingredient_agent import ingredient_agent
from agents.ingredient_cleaner import clean_ingredient



def divide_nutrition(total, people):

    result = {}

    for key, value in total.items():

        try:
            result[key] = round(
                value / people,
                2
            )

        except:
            result[key] = value

    return result



def manager_agent(food, people):


    print("START MANAGER:", food)


    search_result = recipe_search_agent(
        food
    )


    recipes = search_result.get(
        "recipes",
        []
    )


    valid_recipes = []



    for recipe in recipes:


        if not isinstance(recipe, dict):

            continue


        # remove error recipes

        if recipe.get("error"):

            continue


        if recipe.get("Recipe") == "error":

            continue



        try:


            parsed = recipe_parser_agent(
                recipe
            )


            # keep original if parser fails

            if not parsed.get("Recipe"):

                parsed["Recipe"] = recipe.get(
                    "Recipe",
                    "Unknown Recipe"
                )


            valid_recipes.append(
                parsed
            )


        except Exception as e:


            print(
                "Parser failed:",
                e
            )

            valid_recipes.append(
                recipe
            )



    if not valid_recipes:


        return {

            "error":
            "No valid recipes found"

        }



    first_recipe = valid_recipes[0]



    ingredients = first_recipe.get(
        "Ingredients",
        []
    )


    print(
        "INGREDIENTS BEFORE CLEAN:",
        ingredients
    )



    cleaned = []


    for item in ingredients:


        if isinstance(item, str):

            value = clean_ingredient(
                item
            )


            if value:

                cleaned.append(
                    value
                )



    print(
        "CLEAN INGREDIENTS:",
        cleaned
    )



    nutrition = ingredient_agent(
        cleaned
    )


    total = nutrition.get(
        "Total Nutrition",
        {}
    )



    return {


        "query":
        food,


        "servings":
        people,


        "recipes":
        valid_recipes,


        "nutrition":
        {

            "Total Recipe Nutrition":
            total,


            "Nutrition Per Person":
            divide_nutrition(
                total,
                people
            )

        }

    }
