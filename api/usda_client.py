import os
import requests
from dotenv import load_dotenv

# Load .env file when running locally
load_dotenv()


def get_usda_key():

    # First check Streamlit Cloud secrets
    try:
        import streamlit as st

        if "USDA_API_KEY" in st.secrets:
            return st.secrets["USDA_API_KEY"]

    except Exception:
        pass


    # Otherwise use local .env
    return os.getenv("USDA_API_KEY")



def search_food(food):

    api_key = get_usda_key()


    if not api_key:
        return {
            "error": "USDA API key missing"
        }


    url = "https://api.nal.usda.gov/fdc/v1/foods/search"


    params = {

        "api_key": api_key,

        "query": food,

        "pageSize": 1

    }


    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )


        print("USDA STATUS:", response.status_code)


        data = response.json()


        if response.status_code != 200:

            return {
                "error": data
            }


        foods = data.get(
            "foods",
            []
        )


        if not foods:

            return {
                "error": "Food not found"
            }


        return foods[0]


    except requests.exceptions.Timeout:

        return {
            "error": "USDA request timeout"
        }


    except Exception as e:

        return {
            "error": str(e)
        }
