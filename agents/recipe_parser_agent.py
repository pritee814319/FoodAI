import requests
from bs4 import BeautifulSoup
import re



BAD_TEXT = [

    "tip",
    "tips",
    "note",
    "variation",
    "optional",
    "subscribe",
    "newsletter",
    "author",
    "comment",
    "google",
    "privacy",
    "cookie",
    "cookbook",
    "additional info",
    "nutrition",
    "equipment",
    "review",
    "kids loved",
    "delicious",
    "preferred source"

]



MEASURE_WORDS = [

    "cup",
    "cups",
    "tbsp",
    "tablespoon",
    "tablespoons",
    "tsp",
    "teaspoon",
    "teaspoons",
    "gram",
    "grams",
    "kg",
    "ml",
    "oz",
    "lb"

]



def clean_line(line):

    line = line.strip()

    line = re.sub(
        r"\s+",
        " ",
        line
    )

    return line



def is_ingredient(line):

    lower = line.lower()


    # remove bad text

    for word in BAD_TEXT:

        if word in lower:

            return False



    # remove long paragraphs

    if len(line) > 90:

        return False



    # ingredient usually starts with quantity

    if re.match(
        r"^[\d¼½¾⅓⅔]",
        line
    ):

        return True



    # contains measurement

    for word in MEASURE_WORDS:

        if word in lower:

            return True



    return False




def recipe_parser_agent(url):

    try:


        headers = {

            "User-Agent":

            "Mozilla/5.0"

        }



        page = requests.get(

            url,

            headers=headers,

            timeout=10

        )



        soup = BeautifulSoup(

            page.text,

            "html.parser"

        )



        # Remove unwanted HTML

        for tag in soup(

            [

                "script",

                "style",

                "nav",

                "footer",

                "header"

            ]

        ):

            tag.decompose()



        text = soup.get_text(
            "\n"
        )



        lines = [

            clean_line(x)

            for x in text.split("\n")

            if x.strip()

        ]



        ingredients=[]

        instructions=[]



        for line in lines:


            if is_ingredient(line):

                ingredients.append(line)



            else:


                lower=line.lower()


                if (

                    lower.startswith("add")

                    or lower.startswith("cook")

                    or lower.startswith("heat")

                    or lower.startswith("mix")

                    or lower.startswith("stir")

                    or lower.startswith("serve")

                    or lower.startswith("fry")

                    or lower.startswith("saute")

                ):

                    if len(line)<120:

                        instructions.append(line)



        return {


            "Ingredients":

            list(dict.fromkeys(ingredients))[:20],



            "Instructions":

            list(dict.fromkeys(instructions))[:15]

        }



    except Exception as e:


        print(
            "Parser error:",
            e
        )


        return {

            "Ingredients": [],

            "Instructions": []

        }
