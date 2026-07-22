import streamlit as st

from agents.manager_agent import manager_agent


st.title("🍲 FoodAI")

food = st.text_input("Enter food")

grams = st.number_input(
    "Quantity (grams)",
    min_value=1,
    value=100
)

if st.button("Analyze"):

    if food:

        result = manager_agent(food, grams)

        st.subheader("Nutrition Information")
        st.json(result["nutrition"])

        st.subheader("Top Recipes")

        if isinstance(result["recipe"], dict) and "error" in result["recipe"]:
            st.warning(result["recipe"]["error"])
        else:
            for recipe in result["recipe"]:
                st.markdown(f"### {recipe['Recipe']}")
                st.write(f"**Cuisine:** {recipe['Cuisine']}")
                st.write(f"**Category:** {recipe['Category']}")

                with st.expander("Ingredients"):
                    for ingredient in recipe["Ingredients"]:
                        st.write(f"- {ingredient}")

                with st.expander("Instructions"):
                    st.write(recipe["Instructions"])

                st.image(recipe["Image"], width=300)

    else:
        st.warning("Please enter a food name.")
