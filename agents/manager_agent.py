from agents.recipe_search import recipe_search_agent


def manager_agent(food_name, people):

    print("MANAGER START:", food_name)

    search_result = recipe_search_agent(food_name)

    print(search_result)

    return {
        "query": food_name,
        "recipes": [],
        "nutrition": {
            "Total Recipe Nutrition": {},
            "Nutrition Per Person": {}
        }
    }
