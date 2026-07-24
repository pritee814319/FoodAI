import streamlit as st

from agents.manager_agent import manager_agent


st.set_page_config(
    page_title="FoodAI",
    page_icon="🍲",
    layout="wide"
)


st.title("🍲 FoodAI")
st.subheader("AI Food Nutrition & Recipe Analyzer")


# -------------------------
# Input Form
# -------------------------

with st.form("food_form"):

    food = st.text_input(
        "Enter food name",
        placeholder="Example: Poha, Pizza, Ramen"
    )


    people = st.number_input(
        "How many people are you cooking for?",
        min_value=1,
        max_value=50,
        value=2
    )


    submitted = st.form_submit_button(
        "🔍 Analyze Food"
    )



# -------------------------
# Analysis
# -------------------------

if submitted:


    if not food.strip():

        st.warning(
            "Please enter food name"
        )


    else:


        with st.spinner(
            "FoodAI is analyzing your food..."
        ):


            try:


                result = manager_agent(
                    food,
                    people
                )


                if "error" in result:


                    st.error(
                        result["error"]
                    )


                else:


                    st.success(
                        "Analysis Complete!"
                    )


                    # =========================
                    # Nutrition Dashboard
                    # =========================


                    st.divider()

                    st.header(
                        "🥗 Nutrition Summary"
                    )


                    nutrition = result.get(
                        "nutrition",
                        {}
                    )


                    total = nutrition.get(
                        "Total Recipe Nutrition",
                        {}
                    )


                    per_person = nutrition.get(
                        "Nutrition Per Person",
                        {}
                    )


                    st.subheader(
                        "🍲 Total Recipe Nutrition"
                    )


                    c1,c2,c3,c4 = st.columns(4)


                    c1.metric(
                        "🔥 Calories",
                        f"{total.get('Calories (kcal)',0)} kcal"
                    )


                    c2.metric(
                        "💪 Protein",
                        f"{total.get('Protein (g)',0)} g"
                    )


                    c3.metric(
                        "🍚 Carbs",
                        f"{total.get('Carbohydrates (g)',0)} g"
                    )


                    c4.metric(
                        "🥑 Fat",
                        f"{total.get('Fat (g)',0)} g"
                    )



                    c5,c6,c7 = st.columns(3)


                    c5.metric(
                        "🌾 Fiber",
                        f"{total.get('Fiber (g)',0)} g"
                    )


                    c6.metric(
                        "🍬 Sugar",
                        f"{total.get('Sugar (g)',0)} g"
                    )


                    c7.metric(
                        "🧂 Sodium",
                        f"{total.get('Sodium (mg)',0)} mg"
                    )



                    st.subheader(
                        f"👤 Per Person ({people} servings)"
                    )


                    p1,p2,p3,p4 = st.columns(4)


                    p1.metric(
                        "🔥 Calories",
                        f"{per_person.get('Calories (kcal)',0)} kcal"
                    )


                    p2.metric(
                        "💪 Protein",
                        f"{per_person.get('Protein (g)',0)} g"
                    )


                    p3.metric(
                        "🍚 Carbs",
                        f"{per_person.get('Carbohydrates (g)',0)} g"
                    )


                    p4.metric(
                        "🥑 Fat",
                        f"{per_person.get('Fat (g)',0)} g"
                    )



                    # =========================
                    # Recipes
                    # =========================


                    st.divider()

                    st.header(
                        "🍛 Recipes"
                    )


                    recipes = result.get(
                        "recipes",
                        []
                    )


                    for recipe in recipes:


                        if not isinstance(
                            recipe,
                            dict
                        ):
                            continue



                        recipe_name = recipe.get(
                            "Recipe",
                            "Recipe"
                        )


                        with st.expander(
                            f"🍽️ {recipe_name}",
                            expanded=True
                        ):


                            url = recipe.get(
                                "URL"
                            )


                            if url:


                                st.write(
                                    "🔗 Source:"
                                )

                                st.write(
                                    url
                                )



                            # Ingredients

                            ingredients = recipe.get(
                                "Ingredients"
                            )


                            if ingredients:


                                st.subheader(
                                    "🥘 Ingredients"
                                )


                                if isinstance(
                                    ingredients,
                                    list
                                ):


                                    for item in ingredients:

                                        st.write(
                                            "•",
                                            item
                                        )

                                else:

                                    st.write(
                                        ingredients
                                    )


                            else:


                                st.info(
                                    "Ingredients not available."
                                )



                            # Instructions

                            instructions = recipe.get(
                                "Instructions"
                            )


                            if instructions:


                                st.subheader(
                                    "👩‍🍳 Instructions"
                                )


                                if isinstance(
                                    instructions,
                                    list
                                ):


                                    for i,step in enumerate(
                                        instructions,
                                        start=1
                                    ):

                                        st.write(
                                            f"{i}. {step}"
                                        )

                                else:

                                    st.write(
                                        instructions
                                    )


                            else:


                                st.caption(
                                    "Full cooking instructions available at source."
                                )



            except Exception as e:


                st.error(
                    f"FoodAI Error: {e}"
                )
