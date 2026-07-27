#################################################
# RECIPE RANKING AGENT
#################################################

def recipe_rank_agent(recipes):


    print(
        "========== RECIPE RANK AGENT =========="
    )


    if not recipes:

        return {

            "Best Recipe": None,

            "Ranked Recipes": []

        }



    ranked=[]



    for recipe in recipes:


        score=0


        ingredients = recipe.get(
            "Ingredients",
            []
        )


        instructions = recipe.get(
            "Instructions",
            []
        )


        name = recipe.get(
            "Recipe",
            "Unknown"
        )



        #################################
        # INGREDIENT SCORE
        #################################

        ingredient_count=len(
            ingredients
        )


        if ingredient_count >= 10:

            score += 30


        elif ingredient_count >=5:

            score +=20



        #################################
        # INSTRUCTION SCORE
        #################################

        instruction_count=len(
            instructions
        )


        if instruction_count >=8:

            score +=40


        elif instruction_count >=3:

            score +=20



        #################################
        # RECIPE QUALITY
        #################################

        if "poha" in name.lower():

            score +=10


        if "traditional" in name.lower():

            score +=5



        ranked.append(

            {

            "Recipe": name,

            "Score": score,

            "Ingredients Count": ingredient_count,

            "Instruction Count": instruction_count

            }

        )



    ranked.sort(

        key=lambda x:x["Score"],

        reverse=True

    )



    return {


        "Best Recipe":

            ranked[0]["Recipe"],



        "Ranked Recipes":

            ranked

    }
