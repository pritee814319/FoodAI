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


    # -----------------------------
    # Food understanding
    # -----------------------------

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



    # -----------------------------
    # MealDB recipes
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
    # Web recipes
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
    # Normalize
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
    # Remove unwanted sources
    # -----------------------------

    blocked_words = [

        "youtube",
        "pinterest",
        "facebook",
        "instagram",
        "category",
        "collection",
        "search",
        "tag",
        "author"

    ]


    final = []

    seen = set()



    # -----------------------------
    # Keep only matching recipes
    # -----------------------------

    food_words = food.lower().split()


    for recipe in cleaned:


        url = recipe.get(
            "URL",
            ""
        )


        name = recipe.get(
            "Recipe",
            ""
        )


        url_lower = url.lower()

        name_lower = name.lower()



        # Create name if missing

        if not name:

            name = (

                url.split("/")[-1]

                .replace("-", " ")

                .replace("_", " ")

                .title()

            )

            name_lower = name.lower()



        # Skip empty

        if not name:

            continue



        # Skip bad websites

        if any(
            word in url_lower
            for word in blocked_words
        ):

            continue



        # Must match food name

        match = any(

            word in name_lower
            or word in url_lower

            for word in food_words

        )


        if not match:

            continue



        key = name_lower.strip()



        if key in seen:

            continue



        seen.add(
            key
        )


        recipe["Recipe"] = name


        final.append(
            recipe
        )



        # limit

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
