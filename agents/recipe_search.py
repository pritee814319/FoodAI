from agents.recipe_agent import recipe_agent
from agents.web_recipe_agent import web_recipe_agent
from agents.food_understanding_agent import food_understanding_agent


def recipe_search_agent(food):

    print("=" * 50)
    print("RECIPE SEARCH")
    print("=" * 50)

    recipes = []

    # -----------------------------
    # Step 1: Understand the food
    # -----------------------------
    food_info = food_understanding_agent(food)

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

print(
    "SEARCH TERMS:",
    search_terms
)

    # -----------------------------
    # Step 2: Search TheMealDB
    # -----------------------------
    try:

        mealdb_results = recipe_agent(
            food_info["standard_name"]
        )

        if mealdb_results:

            print(
                "TheMealDB:",
                len(mealdb_results),
                "recipes"
            )

            recipes.extend(mealdb_results)

    except Exception as e:

        print(
            "MealDB Error:",
            e
        )

    # -----------------------------
    # Step 3: Search Internet
    # -----------------------------
    for search_term in food_info["search_terms"]:

        if len(recipes) >= 5:
            break

        try:

            print(
                "Searching:",
                search_term
            )

            web_results = web_recipe_agent(
                search_term
            )

            if web_results:

                print(
                    "Found:",
                    len(web_results)
                )

                recipes.extend(web_results)

        except Exception as e:

            print(
                "Web Search Error:",
                e
            )

    # -----------------------------
    # Step 4: Remove duplicates
    # -----------------------------
    unique = []
    seen = set()

    for recipe in recipes:

        if not isinstance(recipe, dict):
            continue

        name = recipe.get(
            "Recipe",
            ""
        ).strip().lower()

        if not name:
            continue

        if name in seen:
            continue

        seen.add(name)
        unique.append(recipe)

    print(
        "FINAL RECIPES:",
        len(unique)
    )

    return {

        "query": food,

        "food_info": food_info,

        "count": len(unique),

        "recipes": unique[:5]

    }
