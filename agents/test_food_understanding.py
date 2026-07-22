from agents.food_understanding_agent import food_understanding_agent


foods = [

    "vada",

    "misal",

    "ramen",

    "pizza",

    "butter chicken"

]

for food in foods:

    print("\n===================")

    result = food_understanding_agent(food)

    print(result)
