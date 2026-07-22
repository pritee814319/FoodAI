import streamlit as st

from agents.manager_agent import manager_agent


# Page setup
st.set_page_config(
    page_title="FoodAI",
    page_icon="🍲"
)


st.title("🍲 FoodAI")
st.write("AI Food Nutrition & Recipe Analyzer")


# User input
food = st.text_input(
    "Enter food name",
    placeholder="Example: Chicken Handi"
)


if st.button("Analyze Food"):

    if food.strip():

        with st.spinner("FoodAI agents are working..."):

            try:

                # Call Manager Agent
                result = manager_agent(food)


                st.success("Analysis Complete!")


                # ------------------------
                # Nutrition Section
                # ------------------------

                st.subheader("🥗 Nutrition Information")


                if (
                    "nutrition" in result
                    and result["nutrition"]
                ):

                    total_nutrition = result["nutrition"].get(
                        "Total Nutrition",
                        {}
                    )

                    st.json(
                        total_nutrition
                    )

                else:

                    st.warning(
                        "Nutrition information not available"
                    )


                # ------------------------
                # Recipe Section
                # ------------------------

                st.subheader("🍛 Top Recipes")


                recipes = result.get(
                    "recipes",
                    []
                )


                if recipes:

                    for recipe in recipes:

                        with st.expander(
                            recipe.get(
                                "Recipe",
                                "Recipe"
                            )
                        ):

                            st.write(
                                "Cuisine:",
                                recipe.get(
                                    "Cuisine",
                                    ""
                                )
                            )

                            st.write(
                                "Category:",
                                recipe.get(
                                    "Category",
                                    ""
                                )
                            )


                            st.subheader(
                                "Ingredients"
                            )

                            for item in recipe.get(
                                "Ingredients",
                                []
                            ):

                                st.write(
                                    "-",
                                    item
                                )


                            st.subheader(
                                "Instructions"
                            )

                            st.write(
                                recipe.get(
                                    "Instructions",
                                    ""
                                )
                            )


                            image = recipe.get(
                                "Image"
                            )

                            if image:

                                st.image(
                                    image,
                                    width=400
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
            "Please enter a food name"
        )
