import streamlit as st
import pandas as pd

from agents.manager_agent import manager_agent
from agents.food_image_agent import food_image_agent


# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="FoodAI",
    page_icon="🍲",
    layout="wide"
)


# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.title("🍲 FoodAI")
st.subheader("AI Food Nutrition & Recipe Analyzer")


# ---------------------------------------------------
# INPUT
# ---------------------------------------------------

# ---------------------------------------------------
# INPUT FORM (ENTER KEY ENABLED)
# ---------------------------------------------------

with st.form(
    "food_form"
):

    food = st.text_input(
        "Enter food name",
        placeholder="Example: Poha, Ramen, Biryani"
    )


    people = st.number_input(
        "How many people are you cooking for?",
        min_value=1,
        value=2
    )


    analyze = st.form_submit_button(
        "🔍 Analyze Food"
    )


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

if analyze:

    if not food:

        st.warning(
            "Please enter a food name first."
        )

        st.stop()


    # -----------------------------
    # RUN FOOD AI
    # -----------------------------

    with st.spinner(
        "Analyzing food..."
    ):

        try:

            result = manager_agent(
                food_name=food,
                people=people
            )


        except Exception as e:

            st.error(
                f"FoodAI Error: {e}"
            )

            st.stop()



    st.success(
        "Analysis Complete!"
    )


    # ===================================================
    # FOOD IMAGE
    # ===================================================

    st.subheader(
        "🍽 Food Image"
    )


    image_data = result.get(
        "food_image"
    )


    # fallback if manager did not return image

    if not image_data:

        try:

            image_data = food_image_agent(
                food
            )

        except Exception as e:

            print(
                "IMAGE ERROR:",
                e
            )

            image_data = None



    if image_data and image_data.get(
        "image_url"
    ):


        st.image(
            image_data["image_url"],
            caption=food.title(),
            use_container_width=True
        )


        if image_data.get(
            "credit"
        ):

            st.caption(
                "Image credit: "
                +
                image_data["credit"]
            )


    else:

        st.write(
            "Food image not available"
        )



    # ===================================================
    # NUTRITION
    # ===================================================

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


    st.divider()


    st.subheader(
        "🥗 Nutrition Information"
    )


    c1,c2,c3 = st.columns(3)


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



    c4,c5,c6 = st.columns(3)


    c4.metric(
        "🥑 Fat",
        f"{total.get('Fat (g)',0)} g"
    )


    c5.metric(
        "🌾 Fiber",
        f"{total.get('Fiber (g)',0)} g"
    )


    c6.metric(
        "🧂 Sodium",
        f"{total.get('Sodium (mg)',0)} mg"
    )



    # ===================================================
    # PER PERSON
    # ===================================================

    st.subheader(
        f"🍽 Nutrition Per Person ({people} people)"
    )


    p1,p2,p3 = st.columns(3)


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



    p4,p5,p6 = st.columns(3)


    p4.metric(
        "🥑 Fat",
        f"{per_person.get('Fat (g)',0)} g"
    )


    p5.metric(
        "🌾 Fiber",
        f"{per_person.get('Fiber (g)',0)} g"
    )


    p6.metric(
        "🧂 Sodium",
        f"{per_person.get('Sodium (mg)',0)} mg"
    )



    # ===================================================
    # MACRO CHART
    # ===================================================

    st.subheader(
        "📊 Macronutrient Calories"
    )


    chart = pd.DataFrame(
        {

            "Nutrient":[
                "Protein",
                "Carbs",
                "Fat"
            ],


            "Calories":[

                total.get(
                    "Protein (g)",
                    0
                ) * 4,


                total.get(
                    "Carbohydrates (g)",
                    0
                ) * 4,


                total.get(
                    "Fat (g)",
                    0
                ) * 9

            ]

        }
    )


    st.bar_chart(
        chart.set_index(
            "Nutrient"
        )
    )



    # ===================================================
    # RECIPES
    # ===================================================

    st.divider()


    st.subheader(
        "🍛 Recipes"
    )


    recipes = result.get(
        "recipes",
        []
    )


    if not recipes:

        st.info(
            "No recipes found"
        )


    for recipe in recipes:


        st.markdown(
            f"## 🍲 {recipe.get('Recipe','Recipe')}"
        )


        if recipe.get(
            "URL"
        ):

            st.write(
                "🔗 Recipe Source:",
                recipe["URL"]
            )



        ingredients = recipe.get(
            "Ingredients",
            []
        )


        if ingredients:

            st.markdown(
                "### 🥘 Ingredients"
            )


            for item in ingredients:

                st.write(
                    "•",
                    item
                )



        instructions = recipe.get(
            "Instructions",
            []
        )


        if instructions:


            st.markdown(
                "### 👩‍🍳 Instructions"
            )


            if isinstance(
                instructions,
                list
            ):


                for i, step in enumerate(
                    instructions,
                    1
                ):

                    st.write(
                        f"{i}. {step}"
                    )


            else:

                st.write(
                    instructions
                )


        else:

            st.info(
                "Recipe instructions available on original source."
            )


        st.divider()
