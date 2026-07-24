from agents.recipe_search import recipe_search_agent
from agents.recipe_parser_agent import recipe_parser_agent
from agents.ingredient_agent import ingredient_agent



def divide_nutrition(total, people):


    per_person = {}


    for key, value in total.items():


        try:

            per_person[key] = round(
                value / people,
                2
            )


        except Exception:


            per_person[key] = value



    return per_person





def manager_agent(food, people):


    print(
        "START MANAGER:",
        food
    )


    print(
        "PEOPLE:",
        people
    )



    # ==========================
    # Recipe Search
    # ==========================


    search_result = recipe_search_agent(
        food
    )



    if not search_result:


        return {

            "error":
            "No recipes found"

        }



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



    # ==========================
    # Parse recipes
    # ==========================


    for recipe in recipes[:5]:


        try:


            parsed = recipe_parser_agent(
                recipe
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





    # ==========================
    # Pick first recipe with ingredients
    # ==========================


    selected_recipe = None



    for recipe in parsed_recipes:


        ingredients = recipe.get(

            "Ingredients",

            []

        )


        if ingredients:


            selected_recipe = recipe

            break





    if not selected_recipe:


        return {


            "query": food,


            "servings": people,


            "recipes": parsed_recipes,


            "nutrition": {

                "Total Recipe Nutrition": {},

                "Nutrition Per Person": {}

            }

        }





    print(

        "SELECTED RECIPE:",

        selected_recipe.get(
            "Recipe"
        )

    )





    ingredients = selected_recipe.get(

        "Ingredients",

        []

    )



    print(

        "INGREDIENTS SENT TO USDA:",

        ingredients

    )





    # ==========================
    # Nutrition
    # ==========================


    nutrition_result = ingredient_agent(

        ingredients

    )



    total_nutrition = nutrition_result.get(

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
