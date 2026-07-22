
from agents.recipe_agent import recipe_agent


def recipe_search_agent(food):

    print("RECIPE SEARCH:", food)


    recipes = recipe_agent(food)


    if not recipes:

        return {

            "query": food,

            "recipes": [],

            "source": "No recipe found"

        }


    # Keep top 5 recipes

    top_recipes = recipes[:5]


    return {

        "query": food,

        "count": len(top_recipes),

        "recipes": top_recipes,

        "source": "TheMealDB"

    }
