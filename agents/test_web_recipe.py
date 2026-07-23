from agents.web_recipe_agent import web_recipe_agent


for food in [
    "misal pav",
    "vada pav",
    "poha"
]:

    print("\n================")
    print(food)

    result = web_recipe_agent(food)

    print(result)
