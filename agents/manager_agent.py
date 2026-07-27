from agents.recipe_search import recipe_search_agent
from agents.recipe_parser_agent import recipe_parser_agent
from agents.ingredient_quantity_agent import ingredient_quantity_agent
from agents.ingredient_agent import ingredient_agent


def divide_nutrition(total, people):

    if people <= 0:
        people = 1

    return {
        key: round(value / people, 2)
        for key, value in total.items()#################################################
# RECIPE RANKING AGENT
#################################################

def recipe_rank_agent(recipes):


    print(
        "========== RECIPE RANK AGENT =========="
    )


    if not recipes:

        return {

            "Best Recipe": None,

            "Ranked Recipes": []

        }



    ranked=[]



    for recipe in recipes:


        score=0


        ingredients = recipe.get(
            "Ingredients",
            []
        )


        instructions = recipe.get(
            "Instructions",
            []
        )


        name = recipe.get(
            "Recipe",
            "Unknown"
        )



        #################################
        # INGREDIENT SCORE
        #################################

        ingredient_count=len(
            ingredients
        )


        if ingredient_count >= 10:

            score += 30


        elif ingredient_count >=5:

            score +=20



        #################################
        # INSTRUCTION SCORE
        #################################

        instruction_count=len(
            instructions
        )


        if instruction_count >=8:

            score +=40


        elif instruction_count >=3:

            score +=20



        #################################
        # RECIPE QUALITY
        #################################

        if "poha" in name.lower():

            score +=10


        if "traditional" in name.lower():

            score +=5



        ranked.append(

            {

            "Recipe": name,

            "Score": score,

            "Ingredients Count": ingredient_count,

            "Instruction Count": instruction_count

            }

        )



    ranked.sort(

        key=lambda x:x["Score"],

        reverse=True

    )



    return {


        "Best Recipe":

            ranked[0]["Recipe"],



        "Ranked Recipes":

            ranked

    }
    }



def manager_agent(food_name, people):


    print("========== MANAGER START ==========")
    print("FOOD:", food_name)



    ###################################
    # SEARCH RECIPES
    ###################################

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


            parsed = recipe_parser_agent(url)



            if parsed.get("Ingredients"):


                parsed["Recipe"] = recipe.get(
                    "Recipe",
                    food_name
                )


                parsed_recipes.append(
                    parsed
                )

from agents.recipe_rank_agent import recipe_rank_agent

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
    # NO RECIPE FOUND
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
    # USE FIRST RECIPE FOR NUTRITION
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



selected_recipe = next(

    recipe for recipe in parsed_recipes

    if recipe.get("Recipe") == best_recipe_name

)



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
    # USDA NUTRITION AGENT
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
    # RETURN RESULT
    ###################################

    return {


        "query": food_name,


        "servings": people,


        "recipes": parsed_recipes,


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
