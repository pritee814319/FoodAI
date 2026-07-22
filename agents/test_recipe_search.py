from agents.recipe_search import recipe_search_agent


foods = [

    "Chicken Handi",

    "Pizza",

    "Sushi",

    "Pasta"

]


for food in foods:

    print("\n====================")

    print("SEARCH:", food)


    result = recipe_search_agent(food)


    print(
        "SOURCE:",
        result["source"]
    )


    print(
        "RECIPES FOUND:",
        result["count"]
        if "count" in result
        else 0
    )


    for recipe in result.get(
        "recipes",
        []
    ):

        print(
            "-",
            recipe.get(
                "Recipe"
            )
        )
