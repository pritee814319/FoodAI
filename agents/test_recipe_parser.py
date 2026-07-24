from agents.recipe_parser_agent import recipe_parser_agent


recipe = {

    "Recipe":
    "Poha Recipe",

    "URL":
    "https://www.vegrecipesofindia.com/poha-recipe-poha/"

}


result = recipe_parser_agent(
    recipe
)


print("\nINGREDIENTS")
print(
    result.get("Ingredients")
)


print("\nINSTRUCTIONS")
print(
    result.get("Instructions")
)
