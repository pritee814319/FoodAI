import streamlit as st

from agents.manager_agent import manager_agent



st.set_page_config(
    page_title="FoodAI",
    page_icon="🍲"
)



st.title("🍲 FoodAI")

st.write(
    "AI Food Nutrition & Recipe Analyzer"
)



food = st.text_input(
    "Enter food name",
    placeholder="Example: Poha, Pizza, Sushi, Ramen"
)



people = st.number_input(
    "How many people are you cooking for?",
    min_value=1,
    max_value=50,
    value=2
)



if st.button("Analyze Food"):


    if not food.strip():

        st.warning(
            "Please enter food name"
        )


    else:


        with st.spinner(
            "FoodAI agents are working..."
        ):


            try:


                result = manager_agent(
                    food,
                    people
                )



                if result.get("error"):


                    st.error(
                        result["error"]
                    )


                else:


                    st.success(
                        "Analysis Complete!"
                    )



                    # -----------------------
                    # Nutrition
                    # -----------------------

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



                    # -----------------------
                    # Recipes
                    # -----------------------

                    st.subheader(
                        "🍛 Recipes"
                    )



                    recipes = result.get(
                        "recipes",
                        []
                    )



                    if not recipes:


                        st.warning(
                            "No recipes found"
                        )



                    for recipe in recipes:



                        if not isinstance(
                            recipe,
                            dict
                        ):

                            continue



                        if recipe.get(
                            "error"
                        ):

                            continue



                        st.markdown(
                            "---"
                        )



                        st.markdown(
                            f"## {recipe.get('Recipe','Recipe')}"
                        )



                        url = recipe.get(
                            "URL",
                            ""
                        )



                        if url:


                            st.write(
                                "🔗 Recipe URL:"
                            )


                            st.write(
                                url
                            )



                        # Ingredients

                        ingredients = recipe.get(
                            "Ingredients",
                            []
                        )



                        if ingredients:


                            st.write(
                                "### 🥘 Ingredients"
                            )


                            for item in ingredients:


                                st.write(
                                    "-",
                                    item
                                )


                        else:


                            st.info(
                                "Ingredients will be extracted by Recipe Parser Agent"
                            )



                        # Instructions

                        instructions = recipe.get(
                            "Instructions",
                            ""
                        )



                        if instructions:


                            st.write(
                                "### 👩‍🍳 Instructions"
                            )


                            st.write(
                                instructions
                            )


                        else:


                            st.info(
                                "Instructions will be extracted by Recipe Parser Agent"
                            )



            except Exception as e:


                st.error(
                    f"FoodAI Error: {e}"
                )
