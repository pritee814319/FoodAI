from tools.web_search import tavily_search


def recipe_search_agent(food):

    print(
        "========== RECIPE SEARCH AGENT =========="
    )


    queries = [
        food,
        f"{food} recipe"
    ]


    all_recipes = []


    for query in queries:

        print(
            "WEB SEARCH START:",
            query
        )


        try:

            results = tavily_search(
                query
            )


            print(
                "TAVILY RESULTS:",
                results
            )


            for r in results:

                url = r.get(
                    "url",
                    ""
                )


                title = r.get(
                    "title",
                    food
                )


                # ignore youtube videos
                if (
                    url
                    and
                    "youtube.com" not in url
                ):

                    all_recipes.append(
                        {
                            "Recipe": title,
                            "URL": url
                        }
                    )


            if len(all_recipes) >= 5:

                break


        except Exception as e:

            print(
                "SEARCH ERROR:",
                e
            )


    print(
        "FINAL RECIPES:",
        len(all_recipes)
    )


    return {

        "recipes": all_recipes[:5]

    }
