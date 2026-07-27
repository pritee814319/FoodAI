from api.usda_client import search_usda_food



#################################################
# FOOD NORMALIZATION
#################################################

FOOD_MAPPING = {

    "poha": "Rice, white, raw",

    "rice flakes": "Rice, white, raw",

    "beaten rice": "Rice, white, raw",

    "flattened rice": "Rice, white, raw",

    "vegetable oil": "Vegetable oil",

    "oil": "Vegetable oil",

    "peanut": "Peanuts, all types, raw",

    "peanuts": "Peanuts, all types, raw",

    "jeera": "Cumin seed",

    "cumin": "Cumin seed",

    "cumin seeds": "Cumin seed",

    "mustard": "Mustard seed",

    "mustard seeds": "Mustard seed",

    "coriander leaves": "Cilantro",

    "green chilli": "Green pepper",

    "chilli": "Green pepper",

    "hing": "Asafoetida"

}





#################################################
# USDA NUTRITION EXTRACTION
#################################################

def extract_nutrition(result):


    nutrition = {

        "Calories (kcal)":0,

        "Protein (g)":0,

        "Carbohydrates (g)":0,

        "Fat (g)":0,

        "Fiber (g)":0,

        "Sugar (g)":0,

        "Sodium (mg)":0

    }



    if not result:

        return nutrition



    data = result.get(
        "nutrition",
        {}
    )



    for key,value in data.items():


        key = key.lower()


        try:

            value=float(value)

        except:

            continue



        if "energy" in key:

            nutrition["Calories (kcal)"] = value


        elif "protein" in key:

            nutrition["Protein (g)"] = value


        elif "carbohydrate" in key:

            nutrition["Carbohydrates (g)"] = value


        elif "fat" in key or "lipid" in key:

            nutrition["Fat (g)"] = value


        elif "fiber" in key:

            nutrition["Fiber (g)"] = value


        elif "sugar" in key:

            nutrition["Sugar (g)"] = value


        elif "sodium" in key:

            nutrition["Sodium (mg)"] = value



    return nutrition





#################################################
# MAIN INGREDIENT AGENT
#################################################

def ingredient_agent(ingredients):


    print(
        "========== INGREDIENT AGENT =========="
    )


    print(
        "INPUT:",
        ingredients
    )



    total = {

        "Calories (kcal)":0,

        "Protein (g)":0,

        "Carbohydrates (g)":0,

        "Fat (g)":0,

        "Fiber (g)":0,

        "Sugar (g)":0,

        "Sodium (mg)":0

    }



    used=[]



    for item in ingredients:


        try:


            name = item.get(
                "name"
            )


            grams = item.get(
                "grams",
                100
            )



            if not name:

                continue



            if name in [
                "salt",
                "sugar"
            ]:

                continue



            search_name = FOOD_MAPPING.get(
                name,
                name
            )



            print(
                "USDA SEARCH:",
                search_name,
                grams,
                "grams"
            )



            result = search_usda_food(
                search_name
            )



            per100 = extract_nutrition(
                result
            )



            # DEBUG
            print(
                "USDA PER 100G:",
                search_name,
                per100
            )



            multiplier = grams / 100



            for key in total:


                total[key] += (
                    per100[key]
                    *
                    multiplier
                )



            used.append(
                {
                    "ingredient": search_name,
                    "grams": grams
                }
            )



        except Exception as e:


            print(
                "INGREDIENT ERROR:",
                e
            )





    for key in total:


        total[key] = round(
            total[key],
            2
        )



    print(
        "========== FINAL USDA NUTRITION =========="
    )


    print(
        total
    )



    return {

        "Ingredients Used": used,

        "Total Nutrition": total

    }
