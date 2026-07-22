
import requests


def search_food(food):

    url = "https://api.duckduckgo.com/"

    params = {
        "q": food + " food recipe",
        "format": "json",
        "no_html": 1,
        "skip_disambig": 0
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    if response.status_code != 200:
        return []

    data = response.json()

    matches = []

    heading = data.get("Heading")
    if heading:
        matches.append(heading)

    for topic in data.get("RelatedTopics", []):

        if isinstance(topic, dict):

            text = topic.get("Text")

            if text:
                matches.append(
                    text.split(" - ")[0]
                )

    # Remove duplicates while preserving order
    unique = []
    for item in matches:
        if item not in unique:
            unique.append(item)

    return unique[:5]
