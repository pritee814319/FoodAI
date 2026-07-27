from api.usda_client import search_usda_food
import re



#################################################
# COMMON INGREDIENT CLEANING
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
    "divided"

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

    """
    Convert:
    '2 cups chopped onion'
    into:
    'onion'
    """

    if not isinstance(text,str):

        return None



    text=text.lower().strip()



    # remove quantities

    text=re.sub(
        r"\d+([./]\d+)?",
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

        text=re.sub(
            r"\b"+unit+r"\b",
            "",
            text
        )



    # remove cooking words

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



    # remove punctuation

    text=re.sub(
        r"[^a-zA-Z\s]",
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



    data=result.get(
        "nutrition",
        {}
    )



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



        elif "total lipid" in key or "fat" in key:

            nutrition["Fat (g)"]=value



        elif "fiber" in key:

            nutrition["Fiber (g)"]=value



        elif "sugar" in key:

            nutrition["Sugar (g)"]=value



        elif "sodium" in key:

            nutrition["Sodium (mg)"]=value



    return nutrition





#################################################
# MAIN INGREDIENT AGENT
#################################################

def ingredient_agent(ingredients):


    print(
        "RAW INGREDIENTS:",
        ingredients
    )



    cleaned=[]

    seen=set()



    ####################################
    # CLEAN INGREDIENT LIST
    ####################################


    for item in ingredients:


        name=normalize_ingredient(
            item
        )


        if not name:

            continue



        if name in seen:

            continue



        seen.add(name)


        cleaned.append(name)



    print(
        "NORMALIZED INGREDIENTS:",
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



    ####################################
    # USDA LOOKUP
    ####################################


    for ingredient in cleaned:


        try:


            print(
                "USDA SEARCH:",
                ingredient
            )



            result=search_usda_food(
                ingredient
            )



            nutrition=extract_nutrition(
                result
            )



            # skip bad USDA results

            if (
                nutrition["Calories (kcal)"]==0
                and
                nutrition["Protein (g)"]==0
            ):

                continue



            used.append(
                ingredient
            )



            for key in total:


                total[key]+=nutrition[key]



        except Exception as e:


            print(
                "USDA ERROR:",
                ingredient,
                e
            )




    ####################################
    # ROUND VALUES
    ####################################


    for key in total:

        total[key]=round(
            total[key],
            2
        )



    print(
        "FINAL NUTRITION:",
        total
    )



    return {


        "Ingredients Used":

            used,


        "Total Nutrition":

            total

    }
