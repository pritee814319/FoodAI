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


if st.button("Analyze Food"):

    if food.strip():

        with st.spinner("FoodAI agents are working..."):

            try:

                result = manager_agent(food)


                # DEBUG
                st.subheader("DEBUG RESULT")
                st.json(result)


                st.success("Analysis Complete!")


                st.subheader("🥗 Nutrition Information")


                nutrition = result.get(
                    "nutrition",
                    {}
                )


                if nutrition:

                    st.json(
                        nutrition.get(
                            "Total Nutrition",
                            nutrition
                        )
                    )

                else:

                    st.warning(
                        "Nutrition information not available"
                    )


                st.subheader("🍛 Top Recipes")


                recipes = result.get(
                    "recipes",
                    []
                )


                if recipes:

                    for recipe in recipes:

                        st.markdown(
                            f"### {recipe.get('Recipe','Recipe')}"
                        )

                        st.write(
                            "Cuisine:",
                            recipe.get(
                                "Cuisine",
                                ""
                            )
                        )


                        st.write(
                            "Ingredients:"
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
                            "Instructions:"
                        )

                        st.write(
                            recipe.get(
                                "Instructions",
                                ""
                            )
                        )

                else:

                    st.warning(
                        "No recipes found"
                    )


            except Exception as e:

                st.error(
                    f"FoodAI Error: {e}"
                )


    else:

        st.warning(
            "Please enter food name"
        )
