from api.web_search_client import search_web_recipes


def web_recipe_agent(food):

    print("WEB SEARCH START:", food)


    results = search_web_recipes(food)


    print("TAVILY RESULTS:")
    print(results)


    recipes = []


    for item in results:


        recipes.append({

            "Recipe": item.get(
                "title",
                "Unknown Recipe"
            ),

            "URL": item.get(
                "url",
                ""
            ),

            "Description": item.get(
                "content",
                ""
            ),

            "Source": "Tavily"

        })


    print(
        "WEB RECIPES FOUND:",
        len(recipes)
    )


    return recipes
