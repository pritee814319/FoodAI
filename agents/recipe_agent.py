from api.mealdb_client import search_recipes


def recipe_agent(food):

    meals = search_recipes(food)


    if not meals:

        return {
            "error": "No recipes found"
        }


    recipes = []


    for meal in meals[:5]:

        ingredients = []


        for i in range(1, 21):

            ingredient = meal.get(
                f"strIngredient{i}"
            )

            measure = meal.get(
                f"strMeasure{i}"
            )


            if ingredient and ingredient.strip():

                ingredients.append(
                    f"{measure.strip()} {ingredient.strip()}"
                )


        recipes.append({

            "Recipe": meal["strMeal"],

            "Cuisine": meal["strArea"],

            "Category": meal["strCategory"],

            "Ingredients": ingredients,

            "Instructions": meal["strInstructions"],

            "Image": meal["strMealThumb"]

        })


    return recipes
