def clean_ingredients(items):

    bad_words = [
        "recipe",
        "about",
        "photo",
        "tips",
        "more",
        "share",
        "comment",
        "faq",
        "breakfast"
    ]


    cleaned=[]


    for item in items:

        text=item.lower()


        if any(
            word in text
            for word in bad_words
        ):
            continue


        cleaned.append(item)


    return cleaned
