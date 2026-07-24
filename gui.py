st.subheader("🍛 Recipes")


recipes = result.get(
    "recipes",
    []
)



for recipe in recipes:


    st.markdown(
        f"## {recipe.get('Recipe','Recipe')}"
    )


    # Recipe Image

    image = recipe.get(
        "Image",
        ""
    )


    if image:

        st.image(
            image,
            width=400
        )



    st.write(
        "🔗 Recipe Source:"
    )


    st.write(
        recipe.get(
            "URL",
            ""
        )
    )



    ingredients = recipe.get(
        "Ingredients",
        []
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


    instructions = recipe.get(
        "Instructions",
        []
    )


    if instructions:


        st.write(
            "👩‍🍳 Instructions"
        )


        for step in instructions:

            st.write(
                step
            )


    st.divider()
