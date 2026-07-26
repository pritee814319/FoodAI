from agents.recipe_search import recipe_search_agent
from agents.recipe_parser_agent import recipe_parser_agent
from agents.ingredient_agent import ingredient_agent


def divide_nutrition(total, people):

    if people <= 0:
        people = 1

    return {
        key: round(value / people, 2)
        for key, value in total.items()
    }



def manager_agent(food_name, people):

    print("MANAGER START:", food_name)


    search_result = recipe_search_agent(food_name)


    recipes = search_result.get(
        "recipes",
        []
    )


    print(
        "RECIPES FOUND:",
        len(recipes)
    )


    final_recipes = []


    for recipe in recipes:

        print(
            "PROCESSING RECIPE:",
            recipe.get("URL", "")
        )


        try:

            parsed = recipe_parser_agent(
                recipe.get("URL", "")
            )


            print(
                "PARSER OUTPUT:",
                parsed
            )


            if parsed.get("Ingredients"):

                final_recipes.append(parsed)


        except Exception as e:

            print(
                "Parser error:",
                e
            )



    print(
        "FINAL RECIPES:",
        len(final_recipes)
    )



    if not final_recipes:

        return {

            "query": food_name,

            "recipes": [],

            "nutrition": {

                "Total Recipe Nutrition": {},

                "Nutrition Per Person": {}

            }

        }



    first_recipe = final_recipes[0]



    nutrition = ingredient_agent(
    first_recipe.get("Ingredients", [])
)


    total = nutrition.get(
        "Total Nutrition",
        {}
    )



    return {

        "query": food_name,

        "servings": people,

        "recipes": final_recipes,


        "nutrition": {

            "Total Recipe Nutrition": total,


            "Nutrition Per Person":

                divide_nutrition(
                    total,
                    people
                )

        }

    }
