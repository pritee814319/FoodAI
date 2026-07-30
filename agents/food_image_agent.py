import requests
import streamlit as st
import os


def get_unsplash_key():

    # Streamlit Cloud secrets
    try:
        key = st.secrets["UNSPLASH_ACCESS_KEY"]

        if key:
            return key

    except Exception as e:
        print("STREAMLIT SECRET ERROR:", e)


    # Local environment fallback
    key = os.getenv(
        "UNSPLASH_ACCESS_KEY"
    )

    return key



def food_image_agent(food_name):

    print("==============================")
    print("FOOD IMAGE AGENT START")
    print("SEARCH:", food_name)


    key = get_unsplash_key()


    if not key:

        print("NO UNSPLASH KEY")

        return None



    print("UNSPLASH KEY FOUND")


    url = "https://api.unsplash.com/search/photos"


    params = {

        "query": food_name + " food",

        "client_id": key,

        "per_page": 1

    }



    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )


        print(
            "UNSPLASH STATUS:",
            response.status_code
        )


        data = response.json()


        if data.get("results"):


            photo = data["results"][0]


            return {

                "image_url":
                    photo["urls"]["regular"],


                "credit":
                    photo["user"]["name"]

            }


        else:

            print(
                "NO IMAGE RESULTS"
            )


    except Exception as e:

        print(
            "IMAGE REQUEST ERROR:",
            e
        )


    return None
