from agents.recipe_agent import recipe_agent
from agents.web_recipe_agent import web_recipe_agent



def recipe_search_agent(food):


    print(
        "RECIPE SEARCH:",
        food
    )


    recipes = []


    # -----------------------
    # Source 1: TheMealDB
    # -----------------------

    try:

        mealdb_results = recipe_agent(
            food
        )


        if mealdb_results:

            recipes.extend(
                mealdb_results
            )


    except Exception as e:

        print(
            "MealDB error:",
            e
        )



    # -----------------------
    # Source 2: Internet Search
    # -----------------------

    if len(recipes) < 5:


        try:

            web_results = web_recipe_agent(
                food
            )


            if web_results:

                recipes.extend(
                    web_results
                )


        except Exception as e:

            print(
                "Web search error:",
                e
            )



    # -----------------------
    # Remove duplicates
    # -----------------------

    final_recipes = []

    names = set()


    for recipe in recipes:


        if isinstance(recipe, dict):


            name = recipe.get(
                "Recipe",
                "Unknown"
            )


            if name not in names:

                names.add(name)

                final_recipes.append(
                    recipe
                )



    print(
        "TOTAL RECIPES:",
        len(final_recipes)
    )


    return {

        "query": food,

        "count": len(final_recipes),

        "recipes": final_recipes[:5]

    }
