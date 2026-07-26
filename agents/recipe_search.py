from agents.recipe_agent import recipe_agent
from agents.web_recipe_agent import web_recipe_agent
from agents.food_understanding_agent import food_understanding_agent


def normalize_recipe(item):

    if isinstance(item, dict):
        return item

    if isinstance(item, str):
        return {
            "Recipe": "",
            "URL": item,
            "Ingredients": [],
            "Instructions": []
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

        result = recipe_agent(
            standard_name
        )

        if result:

            recipes.extend(result)


    except Exception as e:

        print(
            "MealDB error:",
            e
        )



    # Web search

    for term in search_terms:

        try:

            result = web_recipe_agent(
                term
            )

            if result:

                recipes.extend(result)


        except Exception as e:

            print(
                "Web error:",
                e
            )



    cleaned = []


    for item in recipes:

        recipe = normalize_recipe(item)

        if recipe:

            cleaned.append(recipe)



    blocked_words = [

        "youtube",
        "pinterest",
        "facebook",
        "instagram",
        "category",
        "collection",
        "search",
        "author"

    ]



    final = []

    seen = set()



    for recipe in cleaned:


        url = recipe.get(
            "URL",
            ""
        ).lower()


        if any(
            word in url
            for word in blocked_words
        ):

            continue



        name = recipe.get(
            "Recipe",
            ""
        )


        if not name:

            name = (
                url
                .split("/")[-1]
                .replace("-", " ")
                .title()
            )


        if not name:

            continue



        # Keep only matching recipes

        food_check = food.lower()


        if (
            food_check not in name.lower()
            and food_check not in url
        ):

            continue



        key = name.lower().strip()


        if key in seen:

            continue



        seen.add(key)


        recipe["Recipe"] = name


        final.append(recipe)



    print(
        "FINAL RECIPES:",
        len(final)
    )



    return {

        "query": food,

        "food_info": food_info,

        "recipes": final[:5],

        "count": len(final)

    }
