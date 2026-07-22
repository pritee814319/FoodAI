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

      def manager_agent(food):

        st.subheader("Nutrition Information")
        st.json(result["nutrition"])

        st.subheader("Top Recipes")

        if isinstance(result["recipes"], dict) and "error" in result["recipes"]:
            st.warning(result["recipes"]["error"])
        else:
            for recipe in result["recipes"]:
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
