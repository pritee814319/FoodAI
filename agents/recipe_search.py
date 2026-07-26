from agents.recipe_agent import recipe_agent
from agents.web_recipe_agent import web_recipe_agent
from agents.food_understanding_agent import food_understanding_agent



def normalize_recipe(item):

    """
    Convert any recipe format into dictionary
    """

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

        food_info = food_understanding_agent(
            food
        )


    except:

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



    # -----------------------------
    # MealDB
    # -----------------------------

    try:

        mealdb = recipe_agent(
            standard_name
        )


        if mealdb:

            recipes.extend(
                mealdb
            )


    except Exception as e:

        print(
            "MealDB error:",
            e
        )



    # -----------------------------
    # Tavily
    # -----------------------------

    for term in search_terms:


        try:

            web = web_recipe_agent(
                term
            )


            if web:

                recipes.extend(
                    web
                )


        except Exception as e:

            print(
                "Web error:",
                e
            )



    # -----------------------------
    # Normalize recipes
    # -----------------------------

    cleaned = []


    for item in recipes:


        recipe = normalize_recipe(
            item
        )


        if recipe:

            cleaned.append(
                recipe
            )



    # -----------------------------
    # Remove bad websites
    # -----------------------------

    blocked = [

    "youtube",
    "pinterest",
    "facebook",
    "instagram",
    "/recipes/",
    "/category/",
    "/collections/",
    "/search"

]



    final = []

    seen = set()



    for recipe in cleaned:


        url = recipe.get(
            "URL",
            ""
        ).lower()



        if any(
            b in url
            for b in blocked
        ):

            continue



        name = recipe.get(
            "Recipe",
            "Unknown"
        )


        key = name.lower().strip()



        if key not in seen:

    food_words = food.lower().split()

    recipe_name = name.lower()


    # keep only recipes matching food name

    if all(
        word in recipe_name
        for word in food_words
    ):

        seen.add(
            key
        )

        final.append(
            recipe
        )



    print(
        "TOTAL RECIPES:",
        len(final)
    )



    return {


        "query": food,


        "food_info": food_info,


        "recipes": final[:10],


        "count": len(final)

    }
