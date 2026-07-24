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
    placeholder="Example: Poha, Pizza, Chicken Handi"
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



                    # -------------------------
                    # Nutrition
                    # -------------------------


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





                    # -------------------------
                    # Recipes
                    # -------------------------


                    st.subheader(
                        "🍛 Recipes"
                    )



                    recipes = result.get(
                        "recipes",
                        []
                    )



                    if not recipes:


                        st.warning(
                            "No recipes available"
                        )



                    for recipe in recipes:



                        recipe_name = recipe.get(
                            "Recipe",
                            "Recipe"
                        )


                        st.markdown(
                            f"## {recipe_name}"
                        )



                        # Recipe Image


                        image = recipe.get(
                            "Image",
                            ""
                        )


                        if image:


                            try:

                                st.image(
                                    image,
                                    width=400
                                )

                            except:

                                pass




                        # URL


                        url = recipe.get(
                            "URL",
                            ""
                        )


                        if url:


                            st.write(
                                "🔗 Recipe Source:"
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
                                "🥘 Ingredients"
                            )



                            for item in ingredients:


                                if isinstance(
                                    item,
                                    str
                                ):


                                    st.write(
                                        "-",
                                        item
                                    )



                        else:


                            st.info(
                                "Ingredients not available"
                            )






                        # Instructions


                        instructions = recipe.get(
                            "Instructions",
                            []
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


                            st.info(
                                "Instructions available on original source"
                            )



                        st.divider()




            except Exception as e:


                st.error(
                    f"FoodAI Error: {e}"
                )



    else:


        st.warning(
            "Please enter food name"
        )
