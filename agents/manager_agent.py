from agents.recipe_search import recipe_search_agent
from agents.recipe_parser_agent import recipe_parser_agent
from agents.ingredient_quantity_agent import ingredient_quantity_agent
from agents.ingredient_agent import ingredient_agent



#################################################
# DIVIDE NUTRITION PER PERSON
#################################################

def divide_nutrition(total, people):

    if people <= 0:
        people = 1


    return {

        key: round(
            value / people,
            2
        )

        for key, value in total.items()

    }





#################################################
# MANAGER AGENT
#################################################

def manager_agent(food_name, people):


    print(
        "========== MANAGER START =========="
    )

    print(
        "FOOD:",
        food_name
    )



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



    parsed_recipes=[]



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



            if ingredients:


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
    # NO RECIPES FOUND
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
    # INGREDIENT PROCESSING
    #################################################

    raw_ingredients = parsed_recipes[0].get(
        "Ingredients",
        []
    )


    print(
        "========== RAW INGREDIENTS =========="
    )


    for item in raw_ingredients:

        print(item)



    #################################################
    # QUANTITY AGENT
    #################################################

    quantity_result = ingredient_quantity_agent(
        raw_ingredients
    )



    print(
        "========== QUANTITY RESULT =========="
    )


    print(
        quantity_result
    )





    #################################################
    # USDA NUTRITION
    #################################################

    nutrition_result = ingredient_agent(
        quantity_result
    )



    print(
        "========== USDA RESULT =========="
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
