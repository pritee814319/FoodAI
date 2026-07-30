from agents.food_image_agent import food_image_agent
from agents.recipe_search import recipe_search_agent
from agents.recipe_parser_agent import recipe_parser_agent
from agents.ingredient_quantity_agent import ingredient_quantity_agent
from agents.ingredient_agent import ingredient_agent
from agents.nutrition_agent import nutrition_agent
from agents.recipe_rank_agent import recipe_rank_agent



def divide_nutrition(total, people):

    if people <= 0:
        people = 1

    return {
        key: round(value / people, 2)
        for key, value in total.items()
    }



def calculate_total_nutrition(cleaned_ingredients):

    total = {

        "Calories (kcal)": 0,
        "Protein (g)": 0,
        "Carbohydrates (g)": 0,
        "Fat (g)": 0,
        "Fiber (g)": 0,
        "Sugar (g)": 0,
        "Sodium (mg)": 0

    }


    for item in cleaned_ingredients:

        try:

            result = nutrition_agent(
                item["usda_name"]
            )


            nutrition = result.get(
                "nutrition",
                {}
            )


            grams = item.get(
                "grams",
                0
            )


            # USDA values are usually per 100g
            multiplier = grams / 100


            for key in total:

                total[key] += (
                    nutrition.get(key, 0)
                    * multiplier
                )


        except Exception as e:

            print(
                "Nutrition error:",
                e
            )


    return {

        key: round(value, 2)

        for key,value in total.items()

    }




def manager_agent(food_name, people):


    print("========== MANAGER START ==========")
    print("FOOD:", food_name)



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


        try:

            parsed = recipe_parser_agent(
                url
            )


            if parsed.get("Ingredients"):


                parsed["Recipe"] = recipe.get(
                    "Recipe",
                    food_name
                )


                parsed["URL"] = url


                parsed_recipes.append(
                    parsed
                )


        except Exception as e:

            print(
                "Parser error:",
                e
            )



    print(
        "VALID RECIPES:",
        len(parsed_recipes)
    )



    if not parsed_recipes:


        return {


            "query": food_name,


            "servings": people,


            "recipes": [],


            "food_image": None,


            "nutrition": {

                "Total Recipe Nutrition": {},

                "Nutrition Per Person": {}

            }

        }



    ###################################
    # RANK RECIPE
    ###################################

    ranking = recipe_rank_agent(
        parsed_recipes
    )


    best_recipe_name = ranking.get(
        "Best Recipe"
    )



    selected_recipe = next(

        (
            r for r in parsed_recipes
            if r.get("Recipe") == best_recipe_name
        ),

        parsed_recipes[0]

    )



    ###################################
    # INGREDIENT PROCESSING
    ###################################

    raw_ingredients = selected_recipe.get(
        "Ingredients",
        []
    )


    quantity_output = ingredient_quantity_agent(
        raw_ingredients
    )


    print(
        "QUANTITY:",
        quantity_output
    )



    cleaned_ingredients = ingredient_agent(
        quantity_output
    )
print("========== INGREDIENT DEBUG ==========")

for item in cleaned_ingredients:
    print(
        item["name"],
        "|",
        item["usda_name"],
        "| grams:",
        item["grams"]
    )

print("======================================")

    print(
        "CLEAN INGREDIENTS:",
        cleaned_ingredients
    )



    ###################################
    # NUTRITION CALCULATION
    ###################################

    total = calculate_total_nutrition(
        cleaned_ingredients
    )


    per_person = divide_nutrition(
        total,
        people
    )



    ###################################
    # IMAGE
    ###################################

    image_url = None


    try:

        image_url = food_image_agent(
            food_name
        )

    except Exception as e:

        print(
            "IMAGE ERROR:",
            e
        )



    ###################################
    # FINAL OUTPUT
    ###################################

    return {


        "query": food_name,


        "servings": people,


        "food_image": image_url,


        "recipes": parsed_recipes,


        "nutrition": {


            "Total Recipe Nutrition": total,


            "Nutrition Per Person": per_person

        }

    }
