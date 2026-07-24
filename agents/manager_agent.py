from agents.recipe_search import recipe_search_agent
from agents.recipe_parser_agent import recipe_parser_agent
from agents.ingredient_agent import ingredient_agent



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

    print(
        "START MANAGER:",
        food
    )


    print(
        "PEOPLE:",
        people
    )


    # Search recipes

    search_result = recipe_search_agent(
        food
    )


    recipes = search_result.get(
        "recipes",
        []
    )


    if not recipes:

        return {
            "error": "No recipes found"
        }



    # Take first recipe

    recipe = recipes[0]


    print(
        "FIRST RECIPE:",
        recipe.get("Recipe")
    )



    # Parse webpage recipe

    try:

        recipe = recipe_parser_agent(
            recipe
        )


    except Exception as e:

        print(
            "PARSER ERROR:",
            e
        )



    ingredients = recipe.get(
        "Ingredients",
        []
    )


    print(
        "INGREDIENT COUNT:",
        len(ingredients)
    )



    # Nutrition

    nutrition = ingredient_agent(
        ingredients
    )



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

            "Total Recipe Nutrition":
            total_nutrition,


            "Nutrition Per Person":
            per_person

        }

    }
