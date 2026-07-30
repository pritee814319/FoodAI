import requests
import streamlit as st
import os


def food_image_agent(food_name):

    print("==============================")
    print("FOOD IMAGE AGENT START")
    print("SEARCH:", food_name)


    try:

        # Try Streamlit secret first
        api_key = None

        try:
            api_key = st.secrets["UNSPLASH_ACCESS_KEY"]

            print("SECRET FOUND")

        except Exception as e:

            print(
                "SECRET ERROR:",
                e
            )


        if not api_key:

            api_key = os.getenv(
                "UNSPLASH_ACCESS_KEY"
            )

            print(
                "ENV KEY FOUND:",
                bool(api_key)
            )


        print(
            "FINAL KEY STATUS:",
            bool(api_key)
        )


        if not api_key:

            print(
                "NO UNSPLASH KEY"
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
            "STATUS:",
            response.status_code
        )


        print(
            "RESPONSE:",
            response.text[:500]
        )



        if response.status_code != 200:

            return None



        data = response.json()



        if len(data.get("results", [])) == 0:

            print(
                "NO RESULTS"
            )

            return None



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



    except Exception as e:


        print(
            "IMAGE AGENT ERROR:",
            e
        )


        return None
