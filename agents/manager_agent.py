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


    print(
        "START MANAGER:",
        food
    )


    print(
        "PEOPLE:",
        people
    )



    # -----------------------------
    # Search recipes
    # -----------------------------

    search_result = recipe_search_agent(
        food
    )


    recipes = search_result.get(
        "recipes",
        []
    )



    if not recipes:


        return {

            "error":
            "No recipes found"

        }



    parsed_recipes = []



    # -----------------------------
    # Parse recipes
    # -----------------------------

    for recipe in recipes:


        if not isinstance(
            recipe,
            dict
        ):

            continue



        try:


            parsed = recipe_parser_agent(
                recipe
            )



            if parsed.get(
                "Recipe"
            ):


                parsed_recipes.append(
                    parsed
                )



        except Exception as e:


            print(
                "PARSER ERROR:",
                e
            )



    if not parsed_recipes:


        return {

            "error":
            "Recipe details could not be extracted"

        }



    # -----------------------------
    # First recipe for nutrition
    # -----------------------------

    first_recipe = parsed_recipes[0]



    raw_ingredients = first_recipe.get(
        "Ingredients",
        []
    )



    print(
        "RAW INGREDIENTS:",
        raw_ingredients
    )



    # Clean ingredients for USDA

    ingredients = []


    for item in raw_ingredients:


        cleaned = clean_ingredient(
            item
        )


        if cleaned:

            ingredients.append(
                cleaned
            )



    print(
        "CLEAN INGREDIENTS:",
        ingredients
    )



    # -----------------------------
    # Nutrition
    # -----------------------------

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


        "query":
        food,


        "servings":
        people,


        "recipes":
        parsed_recipes,


        "nutrition": {


            "Total Recipe Nutrition":
            total_nutrition,


            "Nutrition Per Person":
            per_person

        }

    }
