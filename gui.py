st.success("Analysis Complete!")

# ---------------------------------------------------
# Food Image
# ---------------------------------------------------

image_url = food_image_agent(food)

if image_url:
    st.image(
        image_url,
        caption=food.title(),
        use_container_width=True
    )

# ---------------------------------------------------
# Nutrition
# ---------------------------------------------------

nutrition = result.get(
    "nutrition",
    {}
)

total = nutrition.get(
    "Total Recipe Nutrition",
    {}
)

per = nutrition.get(
    "Nutrition Per Person",
    {}
)

st.subheader("🥗 Nutrition")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Calories",
        f"{round(total.get('Calories (kcal)',0),1)} kcal"
    )

with c2:
    st.metric(
        "Protein",
        f"{round(total.get('Protein (g)',0),1)} g"
    )

with c3:
    st.metric(
        "Carbs",
        f"{round(total.get('Carbohydrates (g)',0),1)} g"
    )

c4, c5, c6 = st.columns(3)

with c4:
    st.metric(
        "Fat",
        f"{round(total.get('Fat (g)',0),1)} g"
    )

with c5:
    st.metric(
        "Fiber",
        f"{round(total.get('Fiber (g)',0),1)} g"
    )

with c6:
    st.metric(
        "Sodium",
        f"{round(total.get('Sodium (mg)',0),1)} mg"
    )

st.divider()

st.subheader("🍽 Nutrition Per Person")

pc1, pc2, pc3 = st.columns(3)

with pc1:
    st.metric(
        "Calories",
        f"{round(per.get('Calories (kcal)',0),1)} kcal"
    )

with pc2:
    st.metric(
        "Protein",
        f"{round(per.get('Protein (g)',0),1)} g"
    )

with pc3:
    st.metric(
        "Carbs",
        f"{round(per.get('Carbohydrates (g)',0),1)} g"
    )

pc4, pc5, pc6 = st.columns(3)

with pc4:
    st.metric(
        "Fat",
        f"{round(per.get('Fat (g)',0),1)} g"
    )

with pc5:
    st.metric(
        "Fiber",
        f"{round(per.get('Fiber (g)',0),1)} g"
    )

with pc6:
    st.metric(
        "Sodium",
        f"{round(per.get('Sodium (mg)',0),1)} mg"
    )

# ---------------------------------------------------
# Pie Chart
# ---------------------------------------------------

st.subheader("📊 Calories by Macronutrients")

protein = total.get(
    "Protein (g)",
    0
)

carbs = total.get(
    "Carbohydrates (g)",
    0
)

fat = total.get(
    "Fat (g)",
    0
)

protein_cal = protein * 4
carb_cal = carbs * 4
fat_cal = fat * 9

values = [
    protein_cal,
    carb_cal,
    fat_cal
]

labels = [
    "Protein",
    "Carbs",
    "Fat"
]

fig, ax = plt.subplots(figsize=(5,5))

ax.pie(
    values,
    labels=labels,
    autopct="%1.1f%%",
    startangle=90
)

ax.axis("equal")

st.pyplot(fig)

st.divider()

# ---------------------------------------------------
# Recipes
# ---------------------------------------------------

st.subheader("🍛 Recipes")

recipes = result.get(
    "recipes",
    []
)

for recipe in recipes:

    st.markdown(
        f"## {recipe.get('Recipe','Recipe')}"
    )

    if recipe.get("URL"):
        st.markdown(
            f"🔗 **Recipe Source:** {recipe['URL']}"
        )

    ingredients = recipe.get(
        "Ingredients",
        []
    )

    if ingredients:

        st.markdown("### 🥘 Ingredients")

        for item in ingredients:
            st.write("•", item)

    else:

        st.info(
            "Ingredients unavailable."
        )

    instructions = recipe.get(
        "Instructions",
        []
    )

    if instructions:

        st.markdown(
            "### 👩‍🍳 Instructions"
        )

        if isinstance(
            instructions,
            list
        ):

            for i, step in enumerate(
                instructions,
                1
            ):
                st.write(
                    f"{i}. {step}"
                )

        else:

            st.write(
                instructions
            )

    else:

        st.info(
            "Instructions unavailable."
        )

    st.divider()
