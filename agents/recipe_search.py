from agents.recipe_agent import recipe_agent
from agents.web_recipe_agent import web_recipe_agent
from agents.food_understanding_agent import food_understanding_agent


def normalize_recipe(item):

    if isinstance(item, dict):
        return item

    if isinstance(item, str):
        return {
            "Recipe": item,
            "URL": "",
            "Ingredients": [],
            "Instructions": ""
        }

    return None



def recipe_search_agent(food):

    print("=" * 40)
    print("RECIPE SEARCH:", food)
    print("=" * 40)


    recipes = []


    # Food understanding

    try:

        food_info = food_understanding_agent(food)

    except Exception:

        food_info = {
            "standard_name": food,
            "search_terms": [food]
        }



    standard_name = food_info.get(
        "standard_name",
        food
    )


    search_terms = food_info.get(
        "search_terms",
        [food]
    )



    # MealDB

    try:

        mealdb = recipe_agent(
            standard_name
        )

        if mealdb:

            recipes.extend(mealdb)


    except Exception as e:

        print(
            "MealDB error:",
            e
        )



    # Web search

    for term in search_terms:

        try:

            web = web_recipe_agent(term)

            if web:

                recipes.extend(web)


        except Exception as e:

            print(
                "Web error:",
                e
            )



    # Normalize

    cleaned = []

    for item in recipes:

        recipe = normalize_recipe(item)

        if recipe:

            cleaned.append(recipe)



    # Remove duplicates

    final = []

    seen = set()


    for recipe in cleaned:


        name = recipe.get(
            "Recipe",
            ""
        )


        url = recipe.get(
            "URL",
            ""
        )


        if not name:

            name = (
                url.split("/")[-1]
                .replace("-", " ")
                .title()
            )


        if not name:

            continue



        name_lower = name.lower()


        # keep only matching food

        if food.lower() not in name_lower:

            continue



        if name_lower in seen:

            continue



        seen.add(name_lower)


        recipe["Recipe"] = name


        final.append(recipe)



        if len(final) >= 5:

            break



    print(
        "TOTAL RECIPES:",
        len(final)
    )


    return {

        "query": food,

        "food_info": food_info,

        "recipes": final,

        "count": len(final)

    }
