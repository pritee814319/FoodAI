from agents.recipe_search import recipe_search_agent
from agents.recipe_parser_agent import recipe_parser_agent
from agents.ingredient_agent import ingredient_agent


def divide_nutrition(total, people):
    """
    Divide nutrition by number of servings.
    """

    if people <= 0:
        people = 1

    result = {}

    for key, value in total.items():
        try:
            result[key] = round(value / people, 2)
        except Exception:
            result[key] = 0

    return result


def empty_result(food_name, people):

    return {
        "query": food_name,
        "servings": people,
        "recipes": [],
        "nutrition": {
            "Total Recipe Nutrition": {
                "Calories (kcal)": 0,
                "Protein (g)": 0,
                "Carbohydrates (g)": 0,
                "Fat (g)": 0,
                "Fiber (g)": 0,
                "Sugar (g)": 0,
                "Sodium (mg)": 0
            },
            "Nutrition Per Person": {
                "Calories (kcal)": 0,
                "Protein (g)": 0,
                "Carbohydrates (g)": 0,
                "Fat (g)": 0,
                "Fiber (g)": 0,
                "Sugar (g)": 0,
                "Sodium (mg)": 0
            }
        }
    }


def manager_agent(food_name, people):

    print("=" * 60)
    print("FOODAI MANAGER")
    print("Food :", food_name)
    print("People :", people)
    print("=" * 60)

    try:

        search_result = recipe_search_agent(food_name)

    except Exception as e:

        print("Recipe Search Error:", e)

        return empty_result(food_name, people)

    recipes = search_result.get("recipes", [])

    print("Recipes Found:", len(recipes))

    if not recipes:

        return empty_result(food_name, people)

    ##########################################################
    # ONLY USE THE BEST RECIPE
    ##########################################################

    recipe = recipes[0]

    url = recipe.get("URL", "")

    print("Using Recipe:", url)

    ##########################################################
    # PARSE RECIPE
    ##########################################################

    try:

        parsed = recipe_parser_agent(url)
print("========== PARSER RESULT ==========")
print(parsed)
print("===================================")
    except Exception as e:

        print("Recipe Parser Error:", e)

        return empty_result(food_name, people)

    ingredients = parsed.get("Ingredients", [])

    instructions = parsed.get("Instructions", [])

    print("Ingredients:", len(ingredients))
    print("Instructions:", len(instructions))

    ##########################################################
    # NUTRITION
    ##########################################################

    nutrition = ingredient_agent(ingredients)

    total = nutrition.get("Total Nutrition", {})

    per_person = divide_nutrition(
        total,
        people
    )

    ##########################################################
    # FINAL RECIPE
    ##########################################################

    final_recipe = {
        "Recipe": recipe.get("Recipe", food_name.title()),
        "URL": url,
        "Ingredients": ingredients,
        "Instructions": instructions
    }

    ##########################################################
    # RETURN
    ##########################################################

    return {

        "query": food_name,

        "servings": people,

        "recipes": [
            final_recipe
        ],

        "nutrition": {

            "Total Recipe Nutrition": total,

            "Nutrition Per Person": per_person

        }

    }
