from agents.web_recipe_agent import web_recipe_agent



foods = [

    "vada",

    "misal pav",

    "ramen",

    "tacos"

]


for food in foods:

    print("\n==============")

    print(
        "SEARCH:",
        food
    )


    result = web_recipe_agent(
        food
    )


    for recipe in result:

        print(
            recipe["Recipe"]
        )

        print(
            recipe["URL"]
        )
