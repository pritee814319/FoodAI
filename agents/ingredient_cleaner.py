import re



def clean_ingredient(text):


    text = text.lower()



    # Remove bullet symbols

    text = re.sub(
        r"[▢•\-]",
        "",
        text
    )



    # Remove quantities

    text = re.sub(
        r"\d+[\d½¼¾\s/]*",
        "",
        text
    )



    # Remove measurements

    units = [

        "cups",
        "cup",
        "tbsp",
        "tsp",
        "tablespoon",
        "tablespoons",
        "teaspoon",
        "teaspoons",
        "medium",
        "large",
        "small"

    ]


    for unit in units:

        text = text.replace(
            unit,
            ""
        )



    # Remove brackets

    text = re.sub(
        r"\(.*?\)",
        "",
        text
    )



    # Keep only letters

    text = re.sub(
        r"[^a-z\s]",
        "",
        text
    )



    text = text.strip()



    # ignore sentences

    bad_words = [

        "recipe",
        "make",
        "cook",
        "add",
        "heat",
        "mix",
        "serve",
        "instructions",
        "version",
        "using"

    ]


    if len(text.split()) > 4:

        return ""



    if any(
        word in text
        for word in bad_words
    ):

        return ""



    return text
