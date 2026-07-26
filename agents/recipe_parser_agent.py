from bs4 import BeautifulSoup
import requests



def recipe_parser_agent(recipe):

    try:

        # -----------------------------
        # Get recipe information
        # -----------------------------

        if isinstance(recipe, dict):

            url = recipe.get(
                "url",
                ""
            )

            title = recipe.get(
                "title",
                "Recipe"
            )

            content = recipe.get(
                "content",
                ""
            )

        else:

            url = recipe
            title = "Recipe"
            content = ""


        text = content


        # -----------------------------
        # Try website extraction
        # -----------------------------

        if url:


            try:

                headers = {
                    "User-Agent":
                    "Mozilla/5.0"
                }


                page = requests.get(
                    url,
                    headers=headers,
                    timeout=8
                )


                soup = BeautifulSoup(
                    page.text,
                    "html.parser"
                )


                website_text = soup.get_text(
                    "\n"
                )


                if len(website_text) > len(text):

                    text = website_text


            except Exception:

                pass



        # -----------------------------
        # Extract lines
        # -----------------------------


        lines = [

            x.strip()

            for x in text.split("\n")

            if x.strip()

        ]



        ingredients = []

        instructions = []



        for line in lines:


            lower = line.lower()



            # Ingredients detection

            if (
    any(
        unit in lower
        for unit in [
            "cup",
            "tbsp",
            "tsp",
            "gram",
            "kg",
            "ml",
            "oz",
            "lb"
        ]
    )
    and len(line.split()) < 12
):

    ingredients.append(line) replace(
                        "-",
                        ""
                    ).strip()
                )



            # Instructions detection

            elif (

                lower.startswith(
                    (
                        "step",
                        "add",
                        "mix",
                        "cook",
                        "heat",
                        "pour",
                        "serve",
                        "rinse",
                        "fry",
                        "boil",
                        "combine"
                    )
                )

            ):

                instructions.append(
                    line
                )



        ingredients = list(
            dict.fromkeys(
                ingredients
            )
        )


        instructions = list(
            dict.fromkeys(
                instructions
            )
        )



        return {

            "Recipe":
                title,

            "URL":
                url,

            "Ingredients":
                ingredients[:30],

            "Instructions":
                instructions[:30]

        }



    except Exception as e:


        print(
            "PARSER ERROR:",
            e
        )


        return {

            "Recipe":
                "error",

            "URL":
                "",

            "Ingredients":
                [],

            "Instructions":
                []

        }
