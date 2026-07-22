from agents.recipe_agent import recipe_agent


result = recipe_agent("Chicken")


for recipe in result:
    print(recipe["Recipe"])
