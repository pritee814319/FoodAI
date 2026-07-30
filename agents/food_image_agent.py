import requests
import streamlit as st
import os


def food_image_agent(food_name):

    print("========== FOOD IMAGE AGENT ==========")
    print("SEARCH IMAGE:", food_name)


    try:

        # Get key from Streamlit Cloud secrets
        try:

            api_key = st.secrets["UNSPLASH_ACCESS_KEY"]

            print(
                "SECRET FOUND FROM STREAMLIT"
            )

        except Exception as e:

            print(
                "STREAMLIT SECRET ERROR:",
                e
            )

            api_key = os.getenv(
                "UNSPLASH_ACCESS_KEY"
            )


        print(
            "API KEY EXISTS:",
            bool(api_key)
        )


        if not api_key:

            print(
                "NO API KEY FOUND"
            )

            return None



        url = "https://api.unsplash.com/search/photos"


        params = {

            "query": food_name + " food",

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


        print(
            "UNSPLASH RESPONSE:",
            response.text[:300]
        )


        data = response.json()


        if data.get("results"):


            image = data["results"][0]


            print(
                "IMAGE FOUND"
            )


            return {

                "image_url":
                    image["urls"]["regular"],

                "credit":
                    image["user"]["name"]

            }


        print(
            "NO IMAGE RESULTS"
        )


        return None



    except Exception as e:


        print(
            "IMAGE ERROR:",
            e
        )


        return None
