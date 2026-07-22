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

            ingredient = meal.get(f"strIngredient{i}")
            measure = meal.get(f"strMeasure{i}")

            if ingredient and ingredient.strip():

                ingredients.append(
                    f"{measure.strip()} {ingredient.strip()}"
                )

        recipes.append({
    "name": meal["strMeal"],
    "cuisine": meal["strArea"],
    "category": meal["strCategory"],
    "image": meal["strMealThumb"],
    "ingredients": ingredients,
    "instructions": meal["strInstructions"]
})

    return recipes
