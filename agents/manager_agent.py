from agents.food_image_agent import food_image_agent
from agents.recipe_search import recipe_search_agent
from agents.recipe_parser_agent import recipe_parser_agent
from agents.ingredient_quantity_agent import ingredient_quantity_agent
from agents.ingredient_agent import ingredient_agent
from agents.recipe_rank_agent import recipe_rank_agent



#################################################
# DIVIDE NUTRITION PER PERSON
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


    print(
        "========== MANAGER START =========="
    )

    print(
        "FOOD:",
        food_name
    )



    ###################################
    # SEARCH RECIPES
    ###################################

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



    ###################################
    # PARSE RECIPES
    ###################################

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
                "PARSER ERROR:",
                e
            )



    print(
        "VALID RECIPES:",
        len(parsed_recipes)
    )



    ###################################
    # NO RECIPES
    ###################################

    if not parsed_recipes:


        return {

            "query": food_name,

            "recipes": [],

            "nutrition": {

                "Total Recipe Nutrition": {},

                "Nutrition Per Person": {}

            }

        }





    ###################################
    # RANK RECIPES
    ###################################

    ranking = recipe_rank_agent(
        parsed_recipes
    )


    print(
        "RANKING:",
        ranking
    )



    best_recipe_name = ranking.get(
        "Best Recipe"
    )



    selected_recipe = parsed_recipes[0]



    for recipe in parsed_recipes:

        if recipe.get("Recipe") == best_recipe_name:

            selected_recipe = recipe

            break





    ###################################
    # INGREDIENT EXTRACTION
    ###################################

    raw_ingredients = selected_recipe.get(
        "Ingredients",
        []
    )


    print(
        "RAW INGREDIENTS:",
        raw_ingredients
    )




    ###################################
    # QUANTITY AGENT
    ###################################

    quantity_output = ingredient_quantity_agent(
        raw_ingredients
    )


    print(
        "QUANTITY OUTPUT:",
        quantity_output
    )




    ###################################
    # USDA NUTRITION
    ###################################

    nutrition_result = ingredient_agent(
        quantity_output
    )


    total = nutrition_result.get(
        "Total Nutrition",
        {}
    )


    print(
        "FINAL TOTAL:",
        total
    )





    ###################################
    # FINAL RESPONSE
    ###################################

    return {

    "query": food_name,

    "servings": people,


    "food_image":

        image_result,


    "recommended_recipe":

        ranking.get(
            "Best Recipe"
        ),


    "recipe_ranking":

        ranking.get(
            "Ranked Recipes"
        ),


    "recipes":

        parsed_recipes,


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
