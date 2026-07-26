import streamlit as st
import pandas as pd

from agents.manager_agent import manager_agent
from agents.food_image_agent import food_image_agent


# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="FoodAI",
    page_icon="🍲",
    layout="wide"
)


# ---------------------------------------------------
# Header
# ---------------------------------------------------

st.title("🍲 FoodAI")
st.subheader("AI Food Nutrition & Recipe Analyzer")


# ---------------------------------------------------
# User Input
# ---------------------------------------------------

food = st.text_input(
    "Enter food name",
    placeholder="Example: Poha, Ramen, Biryani"
)

people = st.number_input(
    "How many people are you cooking for?",
    min_value=1,
    value=2
)


analyze = st.button(
    "🔍 Analyze Food"
)


# ---------------------------------------------------
# Run Analysis
# ---------------------------------------------------

if analyze and food:

    with st.spinner("Analyzing food..."):

        try:

            result = manager_agent(
                food_name=food,
                people=people
            )

            # Uncomment if you want to see the returned data
            # st.write(result)

        except Exception as e:

            st.error(f"FoodAI Error: {e}")
            st.stop()

    st.success("Analysis Complete!")

    
    # ---------------------------------------------------
    # Food Image
    # ---------------------------------------------------

    st.subheader("🍽 Food Image")

    try:

        image_url = food_image_agent(food)

        if image_url:

            st.image(
                image_url,
                caption=food.title(),
                use_container_width=True
            )

    except Exception:

        st.info(
            "Food image not available"
        )


    # ---------------------------------------------------
    # Nutrition
    # ---------------------------------------------------

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


    # Total nutrition cards

    col1, col2, col3 = st.columns(3)


    col1.metric(
        "🔥 Calories",
        f"{total.get('Calories (kcal)',0)} kcal"
    )


    col2.metric(
        "💪 Protein",
        f"{total.get('Protein (g)',0)} g"
    )


    col3.metric(
        "🍚 Carbs",
        f"{total.get('Carbohydrates (g)',0)} g"
    )


    col4, col5, col6 = st.columns(3)


    col4.metric(
        "🥑 Fat",
        f"{total.get('Fat (g)',0)} g"
    )


    col5.metric(
        "🌾 Fiber",
        f"{total.get('Fiber (g)',0)} g"
    )


    col6.metric(
        "🧂 Sodium",
        f"{total.get('Sodium (mg)',0)} mg"
    )


    # ---------------------------------------------------
    # Per Person
    # ---------------------------------------------------

    st.subheader(
        f"🍽 Nutrition Per Person ({people} people)"
    )


    p1, p2, p3 = st.columns(3)


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


    p4, p5, p6 = st.columns(3)


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


    # ---------------------------------------------------
    # Nutrition Chart
    # ---------------------------------------------------

    st.subheader(
        "📊 Macronutrient Calories"
    )


    protein = total.get(
        "Protein (g)",
        0
    )

    carbs = total.get(
        "Carbohydrates (g)",
        0
    )

    fat = total.get(
        "Fat (g)",
        0
    )


    chart = pd.DataFrame(
        {
            "Nutrient": [
                "Protein",
                "Carbs",
                "Fat"
            ],

            "Calories": [
                protein * 4,
                carbs * 4,
                fat * 9
            ]
        }
    )


    st.bar_chart(
        chart.set_index(
            "Nutrient"
        )
    )


    # ---------------------------------------------------
    # Recipes
    # ---------------------------------------------------

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


        name = recipe.get(
            "Recipe",
            "Recipe"
        )


        st.markdown(
            f"## 🍲 {name}"
        )


        url = recipe.get(
            "URL"
        )


        if url:

            st.markdown(
                f"🔗 Recipe Source: {url}"
            )


        ingredients = recipe.get(
            "Ingredients",
            []
        )


        if ingredients:

            st.markdown(
                "### 🥘 Ingredients"
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

                for index, step in enumerate(
                    instructions,
                    1
                ):

                    st.write(
                        f"{index}. {step}"
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


elif analyze and not food:

    st.warning(
        "Please enter a food name first."
    )
