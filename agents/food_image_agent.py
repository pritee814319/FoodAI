import requests
import streamlit as st


def food_image_agent(food_name):

    print("========== FOOD IMAGE AGENT ==========")

    print("SEARCH IMAGE:", food_name)


    try:

        # Streamlit Cloud Secrets
        api_key = st.secrets.get(
            "UNSPLASH_ACCESS_KEY"
        )


        if not api_key:

            print(
                "Unsplash API key missing"
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


        data = response.json()

print(
    "UNSPLASH RESPONSE:",
    data
)


        if data.get("results"):


            image = data["results"][0]


            result = {

                "image_url":
                    image["urls"]["regular"],

                "credit":
                    image["user"]["name"]

            }


            print(
                "IMAGE FOUND:",
                result
            )


            return result



        print(
            "NO IMAGE FOUND"
        )


        return None



    except Exception as e:


        print(
            "IMAGE ERROR:",
            e
        )


        return None
