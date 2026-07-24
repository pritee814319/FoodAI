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



        # remove error results

        if recipe.get(
            "error"
        ):

            continue



        if recipe.get(
            "Recipe"
        ) == "error":

            continue



        try:


            parsed = recipe_parser_agent(
                recipe
            )


            if not parsed.get(
                "Recipe"
            ):

                parsed["Recipe"] = recipe.get(
                    "Recipe",
                    "Unknown Recipe"
                )



            parsed_recipes.append(
                parsed
            )


        except Exception as e:


            print(
                "PARSER ERROR:",
                e
            )


            parsed_recipes.append(
                recipe
            )



    if not parsed_recipes:


        return {

            "error":
            "Recipe parsing failed"

        }



    # -----------------------------
    # Take first recipe nutrition
    # -----------------------------

    first_recipe = parsed_recipes[0]



    ingredients = first_recipe.get(
        "Ingredients",
        []
    )


    print(
        "RAW INGREDIENTS:"
    )


    print(
        ingredients
    )



    # -----------------------------
    # Clean ingredients
    # -----------------------------

    clean_list = []



    for item in ingredients:


        if isinstance(
            item,
            str
        ):


            cleaned = clean_ingredient(
                item
            )



            if cleaned:


                clean_list.append(
                    cleaned
                )



    print(
        "FINAL USDA INGREDIENTS:"
    )


    print(
        clean_list
    )



    # -----------------------------
    # Nutrition
    # -----------------------------

    nutrition = ingredient_agent(
        clean_list
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


        "nutrition":
        {


            "Total Recipe Nutrition":
            total_nutrition,


            "Nutrition Per Person":
            per_person

        }

    }
