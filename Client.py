import requests


dish = input("Enter any dish name: ")


response = requests.get(
    "http://127.0.0.1:5000/analyze",
    params={
        "dish": dish
    }
)


print("\nServer response:")
print(response.text)


if response.status_code != 200:
    exit()


result = response.json()



print("\n====================")
print("Food Information")
print("====================")


print("\nDish:")
print(result["Dish"])


print("\nCuisine:")
print(result["Cuisine"])


print("\nIngredients:")

for item in result["Ingredients"]:
    print(
        "-",
        item["name"],
        "(",
        item["quantity"],
        ")"
    )


print("\nNutrition:")

for key, value in result["Nutrition"].items():
    print(
        key,
        ":",
        value
    )