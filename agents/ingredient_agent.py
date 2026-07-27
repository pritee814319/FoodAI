from api.usda_client import search_usda_food
import re


#################################################
# INGREDIENT NORMALIZATION
#################################################

REMOVE_WORDS = [
    "chopped",
    "finely chopped",
    "roughly chopped",
    "sliced",
    "diced",
    "minced",
    "crushed",
    "grated",
    "fresh",
    "optional",
    "to taste",
    "as needed",
    "divided",
    "small",
    "medium",
    "large"
]


UNITS = [
    "cup",
    "cups",
    "tbsp",
    "tablespoon",
    "tablespoons",
    "tsp",
    "teaspoon",
    "teaspoons",
    "gram",
    "grams",
    "kg",
    "ml",
    "oz",
    "lb"
]



def normalize_ingredient(text):

    if not isinstance(text, str):
        return None


    text = text.lower()


    # special Indian ingredient mapping

    replacements = {

        "poha": "rice",

        "beaten rice flakes": "rice",

        "flattened rice": "rice",

        "hing": "asafoetida",

        "jeera": "cumin",

        "dhania": "coriander",

        "curry leaves": "curry leaf"

    }


    for old,new in replacements.items():

        text=text.replace(
            old,
            new
        )



    # remove quantity

    text=re.sub(
        r"\d+[/\d]*",
        "",
        text
    )


    # remove fractions

    text=re.sub(
        r"[¼½¾]",
        "",
        text
    )


    # remove units

    for unit in UNITS:

        text=text.replace(
            unit,
            ""
        )



    # remove words

    for word in REMOVE_WORDS:

        text=text.replace(
            word,
            ""
        )



    # remove brackets

    text=re.sub(
        r"\(.*?\)",
        "",
        text
    )


    # remove symbols

    text=re.sub(
        "[^a-zA-Z ]",
        "",
        text
    )


    text=" ".join(
        text.split()
    )


    if len(text)<3:

        return None


    return text





#################################################
# USDA EXTRACTION DEBUG VERSION
#################################################

def extract_nutrition(result):


    print("USDA RAW RESPONSE:")
    print(result)



    nutrition={

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



    # check different possible formats

    data=result.get(
        "nutrition",
        {}
    )


    if not data:

        return nutrition



    for key,value in data.items():


        key=key.lower()


        try:

            value=float(value)

        except:

            continue



        if "energy" in key:

            nutrition["Calories (kcal)"]=value


        elif "protein" in key:

            nutrition["Protein (g)"]=value


        elif "carbohydrate" in key:

            nutrition["Carbohydrates (g)"]=value


        elif "fat" in key or "lipid" in key:

            nutrition["Fat (g)"]=value


        elif "fiber" in key:

            nutrition["Fiber (g)"]=value


        elif "sugar" in key:

            nutrition["Sugar (g)"]=value


        elif "sodium" in key:

            nutrition["Sodium (mg)"]=value



    return nutrition





#################################################
# MAIN AGENT
#################################################

def ingredient_agent(ingredients):


    print("\n========== INGREDIENT AGENT ==========")


    cleaned=[]

    seen=set()



    for item in ingredients:


        name=normalize_ingredient(
            item
        )


        if name and name not in seen:

            seen.add(name)

            cleaned.append(name)



    print(
        "CLEAN INGREDIENTS:",
        cleaned
    )



    total={

        "Calories (kcal)":0,
        "Protein (g)":0,
        "Carbohydrates (g)":0,
        "Fat (g)":0,
        "Fiber (g)":0,
        "Sugar (g)":0,
        "Sodium (mg)":0

    }



    used=[]



    for ingredient in cleaned:


        print(
            "\nSEARCH USDA:",
            ingredient
        )


        try:


            result=search_usda_food(
                ingredient
            )


            nutrition=extract_nutrition(
                result
            )


            print(
                "NUTRITION FOUND:",
                nutrition
            )



            if nutrition["Calories (kcal)"]==0:

                print(
                    "SKIPPED:",
                    ingredient
                )

                continue



            used.append(
                ingredient
            )


            for key in total:

                total[key]+=nutrition[key]



        except Exception as e:


            print(
                "ERROR:",
                ingredient,
                e
            )



    for key in total:

        total[key]=round(
            total[key],
            2
        )


    print(
        "\nUSED INGREDIENTS:",
        used
    )


    print(
        "FINAL TOTAL:",
        total
    )


    return {


        "Ingredients Used":
        used,


        "Total Nutrition":
        total

    }
