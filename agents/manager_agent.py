from agents.recipe_search import recipe_search_agent
from agents.recipe_parser_agent import recipe_parser_agent
from agents.ingredient_agent import ingredient_agent



def divide_nutrition(total, people):

    if people <= 0:
        people = 1

    return {
        key: round(value / people, 2)
        for key, value in total.items()
    }



def manager_agent(food_name, people):

    print("========== MANAGER START ==========")
    print("FOOD:", food_name)


    # Search recipes
    search_result = recipe_search_agent(food_name)


    recipes = search_result.get(
        "recipes",
        []
    )


    print(
        "RECIPES FOUND:",
        len(recipes)
    )


    parsed_recipes = []


    for recipe in recipes:

        url = recipe.get(
            "URL",
            ""
        )


        print(
            "PARSING URL:",
            url
        )


        try:

            parsed = recipe_parser_agent(
                url
            )


            print(
                "INGREDIENT COUNT:",
                len(
                    parsed.get(
                        "Ingredients",
                        []
                    )
                )
            )


            if parsed.get("Ingredients"):


                parsed["Recipe"] = recipe.get(
                    "Recipe",
                    food_name
                )


                parsed_recipes.append(
                    parsed
                )


        except Exception as e:

            print(
                "Parser failed:",
                e
            )



    print(
        "VALID RECIPES:",
        len(parsed_recipes)
    )



    if len(parsed_recipes) == 0:

        return {

            "query": food_name,

            "recipes": [],

            "nutrition": {

                "Total Recipe Nutrition": {},

                "Nutrition Per Person": {}

            }

        }



    # Get ingredients from first recipe

    ingredients = parsed_recipes[0].get(
        "Ingredients",
        []
    )


    print(
        "========== INGREDIENTS SENT TO USDA =========="
    )


    for item in ingredients:

        print(item)


    print(
        "TOTAL INGREDIENT COUNT:",
        len(ingredients)
    )



    # Calculate nutrition

    nutrition_result = ingredient_agent(
        ingredients
    )


    print(
        "========== NUTRITION RESULT =========="
    )

    print(
        nutrition_result
    )



    total = nutrition_result.get(
        "Total Nutrition",
        {}
    )



    return {


        "query": food_name,


        "servings": people,


        "recipes": parsed_recipes,


        "nutrition": {


            "Total Recipe Nutrition": total,


            "Nutrition Per Person":

                divide_nutrition(
                    total,
                    people
                )

        }

    }
