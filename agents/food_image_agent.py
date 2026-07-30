import requests
import streamlit as st


def food_image_agent(food_name):

    print("========== FOOD IMAGE AGENT ==========")
    print("SEARCHING IMAGE FOR:", food_name)


    try:

        api_key = st.secrets["UNSPLASH_ACCESS_KEY"]


        url = "https://api.unsplash.com/search/photos"


        params = {
            "query": food_name + " food",
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


        if data.get("results"):


            photo = data["results"][0]


            image_url = photo["urls"]["regular"]


            photographer = photo["user"]["name"]


            print(
                "IMAGE FOUND:",
                image_url
            )


            return {

                "image_url": image_url,

                "credit": photographer

            }


        else:

            print(
                "NO IMAGE FOUND"
            )

            return None



    except Exception as e:


        print(
            "IMAGE AGENT ERROR:",
            e
        )


        return None
