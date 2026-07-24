import json

try:
    import ollama
except ImportError:
    ollama = None


def food_understanding_agent(food):

    # Fallback if no LLM is available
    if ollama is None:
        return {
            "original": food,
            "standard_name": food.title(),
            "aliases": [food],
            "cuisine": "Unknown",
            "category": "Unknown",
            "search_terms": [
                food,
                f"{food} recipe",
                f"how to make {food}"
            ]
        }

    prompt = f"""
You are a food expert.

Analyze this food:

{food}

Return ONLY valid JSON in this format:

{{
    "standard_name":"",
    "aliases":[],
    "cuisine":"",
    "category":"",
    "search_terms":[]
}}

Rules:
- standard_name should be the most common international name.
- aliases should include regional names.
- search_terms should contain 4-6 useful recipe search phrases.
"""

    response = ollama.chat(
        model="qwen2.5",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    try:
        data = json.loads(
            response["message"]["content"]
        )

        data["original"] = food

        return data

    except Exception:

        return {
            "original": food,
            "standard_name": food.title(),
            "aliases": [food],
            "cuisine": "Unknown",
            "category": "Unknown",
            "search_terms": [
                food,
                f"{food} recipe"
            ]
        }
