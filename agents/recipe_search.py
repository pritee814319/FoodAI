from agents.recipe_agent import recipe_agent
from agents.web_recipe_agent import web_recipe_agent



def recipe_search_agent(food):


    print(
        "RECIPE SEARCH:",
        food
    )


    recipes = []


    # 1. TheMealDB

    try:

        mealdb = recipe_agent(food)

        if mealdb:

            recipes.extend(
                mealdb
            )


    except Exception as e:

        print(
            "MealDB error:",
            e
        )



    # 2. Internet fallback

    if len(recipes) < 5:


        try:

            web = web_recipe_agent(
                food
            )

            if web:

                recipes.extend(
                    web
                )


        except Exception as e:

            print(
                "Web search error:",
                e
            )
print("DEBUG RECIPES:")
print(recipes)


 return {

    "query": food,

    "count": len(recipes[:5]),

    "recipes": recipes[:5]

}
