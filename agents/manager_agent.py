from agents.recipe_search import recipe_search_agent
from agents.recipe_parser_agent import recipe_parser_agent
from agents.ingredient_quantity_agent import ingredient_quantity_agent
from agents.ingredient_agent import ingredient_agent



#################################################
# DIVIDE NUTRITION BY PEOPLE
#################################################

def divide_nutrition(total, people):

    if people <= 0:
        people = 1

    return {
        key: round(value / people, 2)
        for key, value in total.items()
    }



#################################################
# MANAGER AGENT
#################################################

def manager_agent(food_name, people):


    print("========== MANAGER START ==========")
    print("FOOD:", food_name)
    print("PEOPLE:", people)



    #################################################
    # SEARCH RECIPES
    #################################################

    search_result = recipe_search_agent(
        food_name
    )


    recipes = search_result.get(
        "recipes",
        []
    )


    print(
        "RECIPES FOUND:",
        len(recipes)
    )



    parsed_recipes = []



    #################################################
    # PARSE RECIPES
    #################################################

    for recipe in recipes:


        url = recipe.get(
            "URL",
            ""
        )


        print(
            "PARSING:",
            url
        )



        try:


            parsed = recipe_parser_agent(
                url
            )


            ingredients = parsed.get(
                "Ingredients",
                []
            )


            print(
                "RAW INGREDIENT COUNT:",
                len(ingredients)
            )



            if len(ingredients) > 0:


                parsed["Recipe"] = recipe.get(
                    "Recipe",
                    food_name
                )


                parsed_recipes.append(
                    parsed
                )



        except Exception as e:


            print(
                "PARSER ERROR:",
                e
            )



    print(
        "VALID RECIPES:",
        len(parsed_recipes)
    )



    #################################################
    # NO RECIPE FOUND
    #################################################

    if not parsed_recipes:


        return {


            "query": food_name,


            "recipes": [],


            "nutrition": {

                "Total Recipe Nutrition": {},

                "Nutrition Per Person": {}

            }

        }



    #################################################
    # TAKE BEST RECIPE
    #################################################

    selected_recipe = parsed_recipes[0]


    raw_ingredients = selected_recipe.get(
        "Ingredients",
        []
    )


    print(
        "========== RAW INGREDIENTS =========="
    )


    for item in raw_ingredients:

        print(item)




    #################################################
    # CONVERT INGREDIENTS TO GRAMS
    #################################################

    quantity_ingredients = ingredient_quantity_agent(
        raw_ingredients
    )



    print(
        "========== QUANTITY OUTPUT =========="
    )


    print(
        quantity_ingredients
    )



    #################################################
    # USDA NUTRITION
    #################################################

    nutrition_result = ingredient_agent(
        quantity_ingredients
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



    #################################################
    # FINAL RESPONSE
    #################################################

    return {


        "query": food_name,


        "servings": people,


        "recipes": parsed_recipes[:3],



        "nutrition": {


            "Total Recipe Nutrition":

                total,



            "Nutrition Per Person":

                divide_nutrition(
                    total,
                    people
                )

        }

    }
