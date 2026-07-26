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
            ""
        )


        if not name:

            continue


        key = name.lower().strip()


        if key in seen:

            continue


        food_words = food.lower().split()

        recipe_name = name.lower()


        if recipe_name.startswith(food.lower()):


            seen.add(
                key
            )


            final.append(
                recipe
            )
