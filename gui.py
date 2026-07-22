import streamlit as st

from agents.nutrition_agent import nutrition_agent


st.title("🍲 FoodAI Nutrition Agent")


dish = st.text_input(
    "Enter food name",
    placeholder="Example: apple, chicken breast"
)


if st.button("Analyze"):

    if dish:

        result = nutrition_agent(dish)

        st.subheader("Nutrition Information")

        st.json(result)

    else:
        st.warning("Please enter a food name")
