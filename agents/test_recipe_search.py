from agents.recipe_parser_agent import recipe_parser_agent


recipe = {

    "Recipe":
    "Misal Pav",

    "URL":
    "PASTE_WORKING_URL_HERE"

}


result = recipe_parser_agent(recipe)


print("\nINGREDIENTS")
for i in result.get("Ingredients", []):
    print("-", i)


print("\nINSTRUCTIONS")
print(result.get("Instructions"))
