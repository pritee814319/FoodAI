import streamlit as st
import requests


st.title("🍽 Food AI Assistant")

st.write(
    "Enter any dish and AI will identify cuisine and ingredients"
)


dish = st.text_input(
    "Enter dish name"
)


if st.button("Analyze"):

    if dish:

        response = requests.get(
            "http://127.0.0.1:5000/analyze",
            params={
                "dish": dish
            }
        )


        result = response.json()


        st.subheader("Dish")
        st.write(result["dish"])


        st.subheader("AI Analysis")
        st.write(result["AI_Analysis"])


        st.subheader("Nutrition")
        st.write(result["Nutrition_note"])


    else:

        st.warning(
            "Please enter a dish name"
        )