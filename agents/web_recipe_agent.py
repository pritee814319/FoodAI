from api.web_search_client import search_web_recipes


def web_recipe_agent(food):


    results = search_web_recipes(
        food
    )


    recipes = []


    for item in results:


        # Make sure every recipe is a dictionary

        if isinstance(item, dict):

            recipes.append({

                "Recipe": item.get(
                    "title",
                    "Unknown Recipe"
                ),

                "URL": item.get(
                    "url",
                    ""
                ),

                "Source": "Internet"

            })


    return recipes
