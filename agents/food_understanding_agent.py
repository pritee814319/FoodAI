import json

try:
    import ollama
except ImportError:
    ollama = None



def food_understanding_agent(food):

    print("FOOD UNDERSTANDING:", food)


    # -----------------------------
    # Fallback data
    # -----------------------------

    fallback = {

        "original": food,

        "standard_name": food,

        "aliases": [
            food
        ],

        "cuisine": "Unknown",

        "category": "Unknown",

        "search_terms": [

            food,

            f"{food} recipe",

            f"how to make {food}",

            f"{food} ingredients"

        ]

    }


    # -----------------------------
    # If Ollama unavailable
    # -----------------------------

    if ollama is None:

        return fallback



    prompt = f"""

You are an expert food AI assistant.

Analyze this food:

{food}


Return ONLY valid JSON.

Do not add explanations.

Format:

{{
    "standard_name": "",
    "aliases": [],
    "cuisine": "",
    "category": "",
    "search_terms": []
}}


Rules:

- standard_name = most common name worldwide
- aliases = regional names or alternate names
- cuisine = country or region
- category = breakfast, snack, main course, dessert etc.
- search_terms = useful recipe search phrases


Example:

Input:
poha


Output:

{{
"standard_name":"Kanda Poha",
"aliases":["Poha","Avalakki","Flattened Rice"],
"cuisine":"Indian",
"category":"Breakfast",
"search_terms":[
"Kanda Poha recipe",
"Poha recipe",
"Maharashtrian Poha recipe",
"Indian flattened rice recipe"
]
}}

"""


    try:


        response = ollama.chat(

            model="qwen2.5",

            messages=[

                {
                    "role":"user",
                    "content":prompt
                }

            ]

        )


        text = response["message"]["content"]


        # Remove markdown JSON if returned

        text = text.replace(
            "```json",
            ""
        ).replace(
            "```",
            ""
        ).strip()



        data = json.loads(text)



        # Safety defaults

        result = {

            "original": food,

            "standard_name": data.get(
                "standard_name",
                food
            ),

            "aliases": data.get(
                "aliases",
                [food]
            ),

            "cuisine": data.get(
                "cuisine",
                "Unknown"
            ),

            "category": data.get(
                "category",
                "Unknown"
            ),

            "search_terms": data.get(
                "search_terms",
                [
                    food,
                    f"{food} recipe",
                    f"how to make {food}"
                ]
            )

        }


        print(
            "FOOD INFO:",
            result
        )


        return result



    except Exception as e:


        print(
            "FOOD UNDERSTANDING ERROR:",
            e
        )


        return fallback
