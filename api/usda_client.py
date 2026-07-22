import requests
import os
import streamlit as st


def get_usda_key():

    try:
        return st.secrets["USDA_API_KEY"]

    except:
        return os.getenv("USDA_API_KEY")


USDA_API_KEY = get_usda_key()


def search_food(food_name):

    url = "https://api.nal.usda.gov/fdc/v1/foods/search"

    params = {
        "api_key": USDA_API_KEY,
        "query": food_name,
        "pageSize": 1
    }

    response = requests.get(
        url,
        params=params
    )

    data = response.json()

    if "foods" in data and len(data["foods"]) > 0:
        return data["foods"][0]

    return None