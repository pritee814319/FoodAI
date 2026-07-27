import requests
import os
import streamlit as st


def food_image_agent(food_name):

    print("========== FOOD IMAGE AGENT ==========")

    print(
        "SEARCH IMAGE:",
        food_name
    )


    try:

        # Try Streamlit Cloud Secrets first
        try:
            api_key = st.secrets["UNSPLASH_ACCESS_KEY"]
        except:
            api_key = os.getenv(
                "UNSPLASH_ACCESS_KEY"
            )


        if not api_key:

            print(
                "UNSPLASH KEY MISSING"
            )

            return None



        url = "https://api.unsplash.com/search/photos"


        params = {

            "query": f"{food_name} food",

            "per_page": 1

        }


        headers = {

            "Authorization":
            f"Client-ID {api_key}"

        }



        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )


        print(
            "UNSPLASH STATUS:",
            response.status_code
        )


        data = response.json()


        print(
            "UNSPLASH DATA:",
            data
        )


        if data.get("results"):


            image = data["results"][0]


            return {

                "image_url":
                    image["urls"]["regular"],

                "credit":
                    image["user"]["name"]

            }



        return None



    except Exception as e:

        print(
            "IMAGE ERROR:",
            e
        )

        return None
