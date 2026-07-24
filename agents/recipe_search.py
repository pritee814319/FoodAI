from agents.recipe_agent import recipe_agent
from agents.web_recipe_agent import web_recipe_agent
from agents.food_understanding_agent import food_understanding_agent



def recipe_search_agent(food):

    print("=" * 50)
    print("RECIPE SEARCH:", food)
    print("=" * 50)


    recipes = []


    # -----------------------------
    # Food Understanding
    # -----------------------------

    food_info = food_understanding_agent(
        food
    )


    standard_name = food_info.get(
        "standard_name",
        food
    )


    search_terms = food_info.get(
        "search_terms",
        [
            food,
            f"{food} recipe",
            f"how to make {food}"
        ]
    )


    print(
        "STANDARD NAME:",
        standard_name
    )



    # -----------------------------
    # TheMealDB
    # -----------------------------

    try:

        mealdb_results = recipe_agent(
            standard_name
        )


        if mealdb_results:

            recipes.extend(
                mealdb_results
            )


    except Exception as e:

        print(
            "MEALDB ERROR:",
            e
        )



    # -----------------------------
    # Tavily Web Search
    # -----------------------------

    for term in search_terms:


        if len(recipes) >= 10:

            break


        try:

            web_results = web_recipe_agent(
                term
            )


            if web_results:

                recipes.extend(
                    web_results
                )


        except Exception as e:

            print(
                "WEB SEARCH ERROR:",
                e
            )



    # -----------------------------
    # Remove bad sources
    # -----------------------------

    blocked_sites = [

        "pinterest",
        "youtube",
        "facebook",
        "instagram"

    ]


    filtered = []


    for recipe in recipes:


        url = recipe.get(
            "URL",
            ""
        ).lower()



        if any(
            site in url
            for site in blocked_sites
        ):

            continue



        filtered.append(
            recipe
        )



    # -----------------------------
    # Remove duplicates
    # -----------------------------

    final_recipes = []

    seen = set()


    for recipe in filtered:


        if not isinstance(
            recipe,
            dict
        ):

            continue



        name = recipe.get(
            "Recipe",
            "Unknown Recipe"
        )


        key = name.lower().strip()



        if key not in seen:

            seen.add(
                key
            )

            final_recipes.append(
                recipe
            )



    print(
        "TOTAL RECIPES:",
        len(final_recipes)
    )


    return {

        "query": food,

        "food_info": food_info,

        "count": len(final_recipes),

        "recipes": final_recipes[:5]

    }
