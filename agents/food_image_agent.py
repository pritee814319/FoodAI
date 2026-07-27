import requests
import streamlit as st


def food_image_agent(food_name):

    print("========== FOOD IMAGE AGENT ==========")
    print("SEARCH IMAGE:", food_name)


    try:

        api_key = st.secrets.get(
            "UNSPLASH_ACCESS_KEY"
        )


        print(
            "API KEY FOUND:",
            bool(api_key)
        )


        if not api_key:

            print(
                "Missing Unsplash API Key"
            )

            return None



        url = "https://api.unsplash.com/search/photos"


        params = {
            "query": food_name + " dish food",
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
            "STATUS:",
            response.status_code
        )


        print(
            "RAW RESPONSE:",
            response.text[:500]
        )


        data = response.json()



        if "results" in data and len(data["results"]) > 0:


            image = data["results"][0]


            print(
                "IMAGE FOUND:",
                image["urls"]["regular"]
            )


            return {

                "image_url": image["urls"]["regular"],

                "credit": image["user"]["name"]

            }


        else:

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
