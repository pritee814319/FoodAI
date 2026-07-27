from agents.recipe_agent import recipe_agent
from agents.web_recipe_agent import web_recipe_agent
from agents.food_understanding_agent import food_understanding_agent


def normalize_recipe(item):

    """
    Convert different recipe outputs into one format
    """

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



def create_recipe_name(url, food):

    """
    Create readable recipe name from URL
    """

    if not url:

        return food.title()


    name = (
        url
        .split("/")
        [-1]
        .replace("-", " ")
        .replace("_", " ")
        .title()
    )


    bad_names = [

        "Recipe",
        "Recipes",
        "Index",
        "Home"

    ]


    if name in bad_names:

        return food.title()


    return name



def recipe_search_agent(food):


    print("=" * 50)
    print("RECIPE SEARCH:", food)
    print("=" * 50)



    recipes = []



    ################################################
    # FOOD UNDERSTANDING
    ################################################


    try:

        food_info = food_understanding_agent(
            food
        )


    except Exception as e:

        print(
            "Food understanding error:",
            e
        )


        food_info = {

            "standard_name": food,

            "search_terms": [
                food
            ]

        }



    standard_name = food_info.get(
        "standard_name",
        food
    )


    search_terms = food_info.get(
        "search_terms",
        [food]
    )



    ################################################
    # MEALDB
    ################################################


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
            "MealDB Error:",
            e
        )



    ################################################
    # WEB SEARCH
    ################################################


    for term in search_terms:


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
                "Web recipe error:",
                e
            )



    print(
        "RAW RECIPES:",
        len(recipes)
    )



    ################################################
    # CLEAN RECIPES
    ################################################


    blocked = [

        "youtube",
        "pinterest",
        "facebook",
        "instagram",
        "tiktok",
        "/category/",
        "/categories/",
        "/search",
        "/tag/",
        "/author/",
        "/collections/"

    ]



    final = []

    seen = set()



    food_words = food.lower().split()



    for item in recipes:


        recipe = normalize_recipe(
            item
        )


        if not recipe:

            continue



        url = recipe.get(
            "URL",
            ""
        )



        url_lower = url.lower()



        # remove bad websites

        if any(
            word in url_lower
            for word in blocked
        ):

            continue



        name = recipe.get(
            "Recipe",
            ""
        )


        if not name:

            name = create_recipe_name(
                url,
                food
            )



        name_lower = name.lower()



        ################################################
        # FOOD MATCHING
        ################################################


        match = False



        for word in food_words:


            if word in name_lower:

                match = True

                break



            if word in url_lower:

                match = True

                break



        if not match:

            continue



        ################################################
        # DUPLICATES
        ################################################


        key = (

            name_lower.strip(),

            url_lower.strip()

        )



        if key in seen:

            continue



        seen.add(key)



        recipe["Recipe"] = name



        final.append(
            recipe
        )



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
