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


    print(
        "MANAGER START:",
        food_name
    )



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



    final_recipes = []



    for recipe in recipes:


        url = recipe.get(
            "URL",
            ""
        )


        print(
            "PROCESSING RECIPE:",
            url
        )



        try:


            parsed = recipe_parser_agent(
                url
            )



            print(
                "========== PARSER RESULT =========="
            )


            print(
                parsed
            )


            print(
                "==================================="
            )



            if parsed.get(
                "Ingredients"
            ):


                # keep recipe name and URL

                parsed["Recipe"] = recipe.get(
                    "Recipe",
                    food_name
                )


                final_recipes.append(
                    parsed
                )



        except Exception as e:


            print(
                "Parser error:",
                e
            )



    print(
        "FINAL RECIPES:",
        len(final_recipes)
    )



    # If parser failed

    if not final_recipes:


        return {


            "query": food_name,


            "recipes": [],


            "nutrition": {


                "Total Recipe Nutrition": {},


                "Nutrition Per Person": {}

            }

        }




    # Use first recipe for nutrition

    first_recipe = final_recipes[0]



    nutrition_result = ingredient_agent(

        first_recipe.get(
            "Ingredients",
            []
        )

    )



    total = nutrition_result.get(

        "Total Nutrition",

        {}

    )



    return {


        "query": food_name,


        "servings": people,


        "recipes": final_recipes,



        "nutrition": {


            "Total Recipe Nutrition": total,



            "Nutrition Per Person":

                divide_nutrition(

                    total,

                    people

                )

        }

    }
