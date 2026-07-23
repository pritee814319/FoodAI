def rank_recipes(recipes):


    priority_domains = [

        "allrecipes.com",
        "bbcgoodfood.com",
        "vegrecipesofindia.com",
        "foodnetwork.com",
        "seriouseats.com",
        "tiffinandteaofficial.com",
        "justonecookbook.com"

    ]


    ranked = []


    for recipe in recipes:


        score = 0


        url = recipe.get(
            "URL",
            ""
        ).lower()


        title = recipe.get(
            "Recipe",
            ""
        ).lower()



        for domain in priority_domains:

            if domain in url:

                score += 5



        if "recipe" in title:

            score += 2



        if "youtube" in url:

            score -= 2



        if "facebook" in url:

            score -= 5



        recipe["score"] = score


        ranked.append(recipe)



    ranked.sort(

        key=lambda x:x["score"],

        reverse=True

    )


    return ranked
