import streamlit as st

from agents.manager_agent import manager_agent


st.set_page_config(
    page_title="FoodAI",
    page_icon="🍲"
)


st.title("🍲 FoodAI")
st.write("AI Food Nutrition & Recipe Analyzer")


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



if st.button("Analyze Food"):


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


                    # Nutrition

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


                    # Recipes

                    st.subheader(
                        "🍛 Recipe"
                    )


                    recipes = result.get(
                        "recipes",
                        []
                    )


                    for recipe in recipes:


                        st.markdown(
                            f"## {recipe.get('Recipe')}"
                        )


                        st.write(
                            "Cuisine:",
                            recipe.get(
                                "Cuisine"
                            )
                        )


                        st.write(
                            "Category:",
                            recipe.get(
                                "Category"
                            )
                        )


                        st.write(
                            "### Ingredients"
                        )


                        for item in recipe.get(
                            "Ingredients",
                            []
                        ):

                            st.write(
                                "-",
                                item
                            )


                        st.write(
                            "### Instructions"
                        )


                        st.write(
                            recipe.get(
                                "Instructions"
                            )
                        )


            except Exception as e:


                st.error(
                    f"FoodAI Error: {e}"
                )


    else:


        st.warning(
            "Please enter food name"
        )
