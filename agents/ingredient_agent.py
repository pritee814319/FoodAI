from agents.nutrition_agent import nutrition_agent


def clean_ingredient_name(ingredient):

    words = ingredient.split()

    measurements = [
        "kg",
        "g",
        "ml",
        "cup",
        "tbsp",
        "tsp",
        "tablespoon",
        "teaspoon",
        "to",
        "taste",
        "¼",
        "½",
        "¾"
    ]

    cleaned = []

    for word in words:

        if word.lower() not in measurements:
            cleaned.append(word)

    return " ".join(cleaned)



def ingredient_agent(ingredients):

    nutrition_results = []


    total = {

        "Calories (kcal)": 0,
        "Protein (g)": 0,
        "Carbohydrates (g)": 0,
        "Fat (g)": 0,
        "Fiber (g)": 0,
        "Sugar (g)": 0,
        "Sodium (mg)": 0

    }


    for ingredient in ingredients:

        name = clean_ingredient_name(
            ingredient
        )


        nutrition = nutrition_agent(
            name
        )


        if "error" not in nutrition:

            nutrition_results.append(
                nutrition
            )


            for key in total:

                total[key] += nutrition.get(
                    key,
                    0
                )


    return {

        "Ingredients Analyzed": nutrition_results,

        "Total Nutrition": total

    }
