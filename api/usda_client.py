import os
import requests


USDA_API_KEY = os.getenv("USDA_API_KEY")

USDA_URL = (
    "https://api.nal.usda.gov/fdc/v1/foods/search"
)


# Better USDA names for common cooking ingredients
FOOD_MAPPING = {

    "poha": "Rice flakes",
    "rice flakes": "Rice flakes",

    "potato": "Potatoes, raw",

    "onion": "Onions, raw",

    "curry leaves": "Curry leaves, raw",

    "cilantro": "Coriander leaves, raw",

    "lemon": "Lemon juice, raw",

    "peas": "Green peas, raw",

    "peanuts": "Peanuts, raw",

    "mustard seeds": "Mustard seed",

    "turmeric": "Turmeric, ground",

    "sugar": "Sugar, granulated",

    "salt": "Salt",

    "vegetable oil": "Vegetable oil"

}



def normalize_food_name(food):

    food_lower = food.lower().strip()

    return FOOD_MAPPING.get(
        food_lower,
        food
    )



def choose_best_food(results, search_term):


    if not results:

        return None


    search_term = search_term.lower()


    preferred = []


    for food in results:


        description = (
            food.get(
                "description",
                ""
            )
            .lower()
        )


        data_type = (
            food.get(
                "dataType",
                ""
            )
        )


        score = 0


        # Prefer exact words
        if search_term in description:
            score += 5


        # Prefer USDA databases
        if data_type == "Foundation":
            score += 5


        if data_type == "SR Legacy":
            score += 4


        # Avoid bad categories
        bad_words = [

            "recipe",
            "patty",
            "dressing",
            "sauce",
            "cookie",
            "cereal bar",
            "frozen",
            "prepared",
            "restaurant"

        ]


        for word in bad_words:

            if word in description:
                score -= 10



        preferred.append(
            (
                score,
                food
            )
        )



    preferred.sort(
        key=lambda x:x[0],
        reverse=True
    )


    return preferred[0][1]




def extract_nutrients(food):


    nutrients = {}


    for item in food.get(
        "foodNutrients",
        []
    ):


        name = item.get(
            "nutrientName"
        )


        value = item.get(
            "value",
            0
        )


        if name in [

            "Energy",
            "Protein",
            "Carbohydrate, by difference",
            "Total lipid (fat)",
            "Fiber, total dietary",
            "Total Sugars",
            "Sodium, Na"

        ]:

            nutrients[name] = value



    return {


        "Calories (kcal)":
            nutrients.get(
                "Energy",
                0
            ),


        "Protein (g)":
            nutrients.get(
                "Protein",
                0
            ),


        "Carbohydrates (g)":
            nutrients.get(
                "Carbohydrate, by difference",
                0
            ),


        "Fat (g)":
            nutrients.get(
                "Total lipid (fat)",
                0
            ),


        "Fiber (g)":
            nutrients.get(
                "Fiber, total dietary",
                0
            ),


        "Sugar (g)":
            nutrients.get(
                "Total Sugars",
                0
            ),


        "Sodium (mg)":
            nutrients.get(
                "Sodium, Na",
                0
            )

    }




def search_usda_food(food):


    if not USDA_API_KEY:

        return {

            "error":
            "USDA API KEY missing"

        }



    search_term = normalize_food_name(food)


    params = {

        "api_key": USDA_API_KEY,

        "query": search_term,

        "pageSize": 20

    }


    response = requests.get(

        USDA_URL,

        params=params,

        timeout=20

    )



    if response.status_code != 200:


        return {

            "error":
            f"USDA ERROR {response.status_code}"

        }



    data = response.json()


    foods = data.get(
        "foods",
        []
    )


    best_food = choose_best_food(

        foods,

        search_term

    )



    if not best_food:


        return {

            "error":
            "Food not found"

        }



    nutrition = extract_nutrients(
        best_food
    )



    return {


        "food":
        best_food.get(
            "description"
        ),


        "nutrition":
        nutrition,


        "source":
        "USDA FoodData Central"


    }
