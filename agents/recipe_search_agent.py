
import requests

from agents.recipe_agent import recipe_agent



def search_internet_recipe(food):

    """
    Placeholder for internet recipe search.
    We will connect web search here next.
    """

    return []




def recipe_search_agent(food):


    print(
        "RECIPE SEARCH:",
        food
    )


    all_recipes = []


    # -------------------------
    # Source 1: TheMealDB
    # -------------------------

    try:

        mealdb_results = recipe_agent(food)

        if mealdb_results:

            all_recipes.extend(
                mealdb_results
            )


    except Exception as e:

        print(
            "MealDB Error:",
            e
        )



    # -------------------------
    # Source 2: Internet Search
    # -------------------------

    if len(all_recipes) < 5:


        web_results = search_internet_recipe(
            food
        )


        if web_results:

            all_recipes.extend(
                web_results
            )



    # Remove duplicates

    unique = []


    names = set()


    for recipe in all_recipes:


        name = recipe.get(
            "Recipe",
            ""
        )


        if name not in names:

            names.add(name)

            unique.append(recipe)



    return {

        "query": food,

        "count": len(unique[:5]),

        "recipes": unique[:5],

        "sources": [

            "TheMealDB",

            "Internet"

        ]

    }
