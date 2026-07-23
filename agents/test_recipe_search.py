from agents.recipe_search import recipe_search_agent


foods = [

    "Chicken Handi",

    "Misal",

    "Pizza",

    "Sushi",

    "Ramen"

]


for food in foods:

    print("\n====================")

    print(
        "SEARCH:",
        food
    )


    result = recipe_search_agent(food)


    print(
        "RECIPES FOUND:",
        result.get(
            "count",
            0
        )
    )


    for recipe in result.get(
        "recipes",
        []
    ):

        print(
            "-",
            recipe.get(
                "Recipe",
                recipe.get(
                    "title",
                    "Unknown"
                )
            )
        )


        if recipe.get("URL"):

            print(
                "URL:",
                recipe["URL"]
            )
