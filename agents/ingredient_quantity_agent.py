import re


def ingredient_quantity_agent(ingredients):

    """
    Converts recipe ingredient text into structured format.

    Input:
    [
        "2 cups poha",
        "1 medium onion",
        "2 tbsp oil"
    ]

    Output:
    [
        {
            "name": "poha",
            "quantity": 2,
            "unit": "cups"
        }
    ]
    """

    cleaned = []


    if not ingredients:
        return cleaned


    # If ingredients arrive as string
    if isinstance(ingredients, str):

        ingredients = ingredients.split("\n")



    for item in ingredients:


        if not item:
            continue


        # remove bullets and symbols

        text = item.strip()

        text = re.sub(
            r"^[▢•\-\*\d+\.\)]\s*",
            "",
            text
        )


        if len(text) < 3:
            continue



        quantity = 1

        unit = "serving"



        # Find fractions and numbers

        number_match = re.search(
            r"(\d+\s?\d*\/?\d*)",
            text
        )


        if number_match:

            number = number_match.group(1)


            try:

                if "/" in number:

                    parts = number.split()

                    if len(parts) == 2:

                        whole = float(parts[0])

                        frac = parts[1].split("/")

                        quantity = whole + (
                            float(frac[0]) /
                            float(frac[1])
                        )

                    else:

                        frac = number.split("/")

                        quantity = (
                            float(frac[0]) /
                            float(frac[1])
                        )


                else:

                    quantity = float(number)


            except:

                quantity = 1



        # Detect units

        units = [

            "cup",
            "cups",

            "tbsp",
            "tablespoon",
            "tablespoons",

            "tsp",
            "teaspoon",
            "teaspoons",

            "g",
            "gram",
            "grams",

            "kg",

            "ml",

            "litre",
            "liter",

            "oz",

            "lb",

            "piece",
            "pieces",

            "medium",
            "large",
            "small"

        ]


        for u in units:

            if re.search(
                r"\b" + u + r"\b",
                text,
                re.I
            ):

                unit = u
                break



        # Remove quantity from name

        name = re.sub(
            r"^[\d\s\/\.]+",
            "",
            text
        )


        # Remove unit words

        name = re.sub(
            r"\b(" +
            "|".join(units) +
            r")\b",
            "",
            name,
            flags=re.I
        )


        name = name.strip(
            " ,.-"
        )



        if name:


            cleaned.append(

                {
                    "name": name,

                    "quantity": round(
                        quantity,
                        2
                    ),

                    "unit": unit
                }

            )


    return cleaned
