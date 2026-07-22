import streamlit as st

from agents.nutrition_agent import nutrition_agent


st.title("🍲 FoodAI Nutrition Agent")


food = st.text_input(
    "Enter food",
    placeholder="Example: pizza, apple, chicken"
)


grams = st.number_input(
    "Quantity (grams)",
    min_value=1,
    value=100
)


if st.button("Analyze"):

    if food:

        result = from agents.manager_agent import manager_agent

result = manager_agent(food, grams)

        st.subheader("Nutrition Information")

        st.json(result)

    else:
        st.warning(
            "Please enter food name"
        )
