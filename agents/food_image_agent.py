import requests
import os
import streamlit as st


def food_image_agent(food_name):

    print("========== FOOD IMAGE AGENT ==========")
    print("SEARCH IMAGE:", food_name)


    try:

        # Get API key from Streamlit Cloud secrets
        try:
            api_key = st.secrets["UNSPLASH_ACCESS_KEY"]
        except:
            api_key = os.getenv("UNSPLASH_ACCESS_KEY")


        if not api_key:

            print("❌ UNSPLASH KEY NOT FOUND")

            return None



        url = "https://api.unsplash.com/search/photos"


        params = {
            "query": f"{food_name} food dish",
            "per_page": 1
        }


        headers = {
            "Authorization": f"Client-ID {api_key}"
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



        if "results" in data and len(data["results"]) > 0:


            image = data["results"][0]


            print(
                "IMAGE FOUND:",
                image["urls"]["regular"]
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
