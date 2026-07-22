from api.duckduckgo_client import search_food


def food_understanding_agent(food):

    query = food.strip()

    if not query:
        return {
            "query": "",
            "matches": []
        }

    matches = search_food(query)

    if not matches:
        matches = [query.title()]

    return {

        "query": query,

        "matches": matches,

        "selected": matches[0]

    }
