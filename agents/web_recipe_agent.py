from api.web_search_client import search_web_recipes



def web_recipe_agent(food):


    results = search_web_recipes(
        food
    )


    recipes = []


    for item in results:

        recipes.append({

            "Recipe":
                item["title"],

            "URL":
                item["url"],

            "Source":
                "Web"

        })


    return recipes
