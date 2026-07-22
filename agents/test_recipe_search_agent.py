from agents.recipe_search_agent import recipe_search_agent



foods = [

    "Chicken Handi",

    "Misal",

    "Sushi",

    "Ramen",

    "Pizza"

]



for food in foods:


    print("\n================")

    print(
        "SEARCH:",
        food
    )


    result = recipe_search_agent(food)


    print(
        "FOUND:",
        result["count"]
    )


    for recipe in result["recipes"]:

        print(
            "-",
            recipe.get("Recipe")
        )
