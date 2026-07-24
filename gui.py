import streamlit as st

from agents.manager_agent import manager_agent


st.set_page_config(
    page_title="FoodAI",
    page_icon="🍲"
)


st.title("🍲 FoodAI")
st.write("AI Food Nutrition & Recipe Analyzer")


with st.form("food_form"):

    food = st.text_input(
        "Enter food name",
        placeholder="Example: Chicken Handi"
    )


    people = st.number_input(
        "How many people are you cooking for?",
        min_value=1,
        max_value=50,
        value=2
    )


    submitted = st.form_submit_button(
        "Analyze Food"
    )



if submitted:


    if food.strip():

        with st.spinner(
            "FoodAI agents are working..."
        ):


            try:

                result = manager_agent(
                    food,
                    people
                )


                if "error" in result:

                    st.error(
                        result["error"]
                    )


                else:

                    st.success(
                        "Analysis Complete!"
                    )


                    st.subheader(
                        "🥗 Nutrition Information"
                    )


                    nutrition = result.get(
                        "nutrition",
                        {}
                    )


                    st.write(
                        "Total Recipe Nutrition"
                    )

                    st.json(
                        nutrition.get(
                            "Total Recipe Nutrition",
                            {}
                        )
                    )


                    st.write(
                        f"Nutrition Per Person ({people} people)"
                    )

                    st.json(
                        nutrition.get(
                            "Nutrition Per Person",
                            {}
                        )
                    )



                    st.subheader(
                        "🍛 Recipes"
                    )


                    recipes = result.get(
                        "recipes",
                        []
                    )


                    for recipe in recipes:


                        st.markdown(
                            f"## {recipe.get('Recipe','Recipe')}"
                        )


                        if recipe.get("URL"):

                            st.write(
                                "🔗 Recipe Source:"
                            )

                            st.write(
                                recipe["URL"]
                            )


                        ingredients = recipe.get(
                            "Ingredients"
                        )


                        if ingredients:


                            st.write(
                                "🥘 Ingredients"
                            )

                            for item in ingredients:

                                st.write(
                                    "-",
                                    item
                                )

                        else:

                            st.info(
                                "Ingredients not available."
                            )


                        instructions = recipe.get(
                            "Instructions"
                        )


                        if instructions:


                            st.write(
                                "👩‍🍳 Instructions"
                            )

                            if isinstance(
                                instructions,
                                list
                            ):

                                for step in instructions:

                                    st.write(
                                        step
                                    )

                            else:

                                st.write(
                                    instructions
                                )

                        else:

                            st.write(
                                "Recipe instructions are available on the original source."
                            )



            except Exception as e:


                st.error(
                    f"FoodAI Error: {e}"
                )


    else:

        st.warning(
            "Please enter food name"
        )
