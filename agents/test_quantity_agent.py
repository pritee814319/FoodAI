from agents.ingredient_quantity_agent import ingredient_quantity_agent


ingredients = [

"2½ cup poha",

"2 tbsp oil",

"1 onion chopped",

"½ tsp turmeric",

"4 oz ramen noodles"

]


result = ingredient_quantity_agent(
    ingredients
)


for r in result:
    print(r)
