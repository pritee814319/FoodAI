import re



def clean_ingredient(text):


    text = text.lower()


    # remove symbols

    text = re.sub(
        r"[^a-zA-Z ]",
        " ",
        text
    )


    words = text.split()


    ignore = [

        "cup",
        "cups",
        "tbsp",
        "tsp",
        "tablespoon",
        "teaspoon",
        "half",
        "medium",
        "large",
        "small"

    ]


    cleaned = []


    for word in words:

        if word not in ignore:

            cleaned.append(
                word
            )


    return " ".join(
        cleaned
    )
