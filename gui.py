import streamlit as st
import requests

st.set_page_config(
    page_title="FoodAI",
    page_icon="🍽️"
)

st.title("🍽️ FoodAI")
st.write("Find cuisine, ingredients and nutrition for any dish.")

dish = st.text_input("Enter any dish")

if st.button("Analyze"):

    if dish:

        from agents.nutrition_agent import nutrition_agent


result = nutrition_agent(dish)

st.write(result)

        if response.status_code == 200:

            result = response.json()

            st.success("Analysis Complete")

            st.subheader("Dish")
            st.write(result["Dish"])

            st.subheader("Cuisine")
            st.write(result["Cuisine"])

            st.subheader("Ingredients")

            for item in result["Ingredients"]:
                st.write(f"• {item['name']} ({item['quantity']})")

            st.subheader("Nutrition")

            nutrition = result["Nutrition"]

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Calories", round(nutrition["Calories"],1))
                st.metric("Protein", round(nutrition["Protein"],1))

            with col2:
                st.metric("Carbs", round(nutrition["Carbs"],1))
                st.metric("Fat", round(nutrition["Fat"],1))

        else:
            st.error("Server Error")
