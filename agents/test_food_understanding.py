
from agents.food_understanding_agent import food_understanding_agent


tests = [

    "chicken handi",

    "chicken hundi",

    "butter chiken",

    "PIZZA",

    "sushi"

]


for food in tests:

    result = food_understanding_agent(food)

    print(result)
