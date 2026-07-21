import json
import requests
from dotenv import load_dotenv
import os

from flask import Flask, request, jsonify
import ollama


app = Flask(__name__)


load_dotenv()

USDA_KEY = os.getenv("USDA_API_KEY")



# Qwen AI
def ask_qwen(dish):

    prompt = f"""
You are a food expert.

Analyze this dish:

{dish}

Return ONLY JSON format.

Example:

{{
    "dish": "Chicken Biryani",
    "cuisine": "Indian",
    "ingredients": [
        {{
            "name": "chicken",
            "quantity": "150g"
        }},
        {{
            "name": "rice",
            "quantity": "200g"
        }},
        {{
            "name": "yogurt",
            "quantity": "50g"
        }}
    ]
}}

Only return JSON.
"""


    response = ollama.chat(
        model="qwen2.5:latest",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )


    return response["message"]["content"]



# USDA nutrition lookup
def get_nutrition(food):

    url = "https://api.nal.usda.gov/fdc/v1/foods/search"

    params = {
        "api_key": USDA_KEY,
        "query": food,
        "pageSize": 1
    }


    response = requests.get(
        url,
        params=params
    )


    data = response.json()


    if "foods" not in data:
        return {}


    nutrients = {}


    for item in data["foods"][0]["foodNutrients"]:

        name = item.get("nutrientName")


        if name in [
            "Energy",
            "Protein",
            "Carbohydrate, by difference",
            "Total lipid (fat)"
        ]:
            nutrients[name] = item.get("value")


    return nutrients



# Calculate complete recipe
def calculate_recipe_nutrition(ingredients):

    total = {

        "Calories": 0,
        "Protein": 0,
        "Carbs": 0,
        "Fat": 0

    }


    for item in ingredients:

        food = item["name"]


        nutrition = get_nutrition(food)


        total["Calories"] += nutrition.get("Energy",0)

        total["Protein"] += nutrition.get("Protein",0)

        total["Carbs"] += nutrition.get(
            "Carbohydrate, by difference",0
        )

        total["Fat"] += nutrition.get(
            "Total lipid (fat)",0
        )


    return total




@app.route("/analyze", methods=["GET"])
def analyze():

    dish = request.args.get("dish")


    if not dish:

        return jsonify({
            "error":"Please enter a dish"
        })


    # Ask Qwen
    qwen_result = ask_qwen(dish)


    # Convert JSON text into Python data
    food_data = json.loads(qwen_result)


    # Calculate nutrition ingredient by ingredient
    nutrition = calculate_recipe_nutrition(
        food_data["ingredients"]
    )


    return jsonify({

        "Dish": food_data["dish"],

        "Cuisine": food_data["cuisine"],

        "Ingredients": food_data["ingredients"],

        "Nutrition": nutrition

    })




if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000
    )