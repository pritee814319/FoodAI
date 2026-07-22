import requests


def recipe_agent(food):

    url = "https://www.themealdb.com/api/json/v1/1/search.php"


    params = {
        "s": food
    }


    response = requests.get(
        url,
        params=params
    )


    data = response.json()


    if not data["meals"]:
        return {
            "error": "No recipes found"
        }


    recipes = []


    for meal in data["meals"][:5]:

        recipes.append({

            "Recipe": meal["strMeal"],

            "Category": meal["strCategory"],

            "Cuisine": meal["strArea"],

            "Instructions": meal["strInstructions"],

            "Image": meal["strMealThumb"]

        })


    return recipes
