import streamlit as st
import pandas as pd
import math

from layout_engine import continuous_flow, vertical_layout


# -----------------------------
# Brand Colors
# -----------------------------

brand_palette = {
    "Zyn": "#e41a1c",
    "Wyn": "#fff700",
    "Nic Nic": "#ffd92f",
    "Pillowz": "#4daf4a",
    "Juice Head": "#00bfc4",
    "Hyde Strips": "#f781bf",
    "Berker": "#a65628",
    "Mojo": "#66a61e",
    "Zippix": "#a6d854",
    "Velo Plus": "#8da0cb",
    "On!": "#4dd2ff",
    "Rogue": "#ff0055",
    "NiQ": "#7cd859",
    "Zimo": "#8dd3c7",
    "BSX": "#4dd07f"
}


def highlight_brands(val):

    if val is None:
        return ""

    color = brand_palette.get(val, "#444")

    return f"background-color: {color}; color: white; font-weight: bold"


# -----------------------------
# App Title
# -----------------------------

st.title("Dynamic Planogram Builder")

# -----------------------------
# Upload CSV
# -----------------------------

uploaded_file = st.file_uploader("Upload Product CSV")

# -----------------------------
# Fixture dimensions
# -----------------------------

rows = st.number_input("Rows", 1, 20, 11)
cols = st.number_input("Columns", 1, 50, 4)


# -----------------------------
# Main App
# -----------------------------

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    numeric_columns = [
        "flavor_count",
        "strength_count",
        "capacity_per_foot"
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=numeric_columns)

    # -----------------------------
    # Product Calculations
    # -----------------------------

    df["total_products"] = df["flavor_count"] * df["strength_count"]

    df["shelves_needed"] = (
        df["total_products"] / df["capacity_per_foot"]
    ).apply(lambda x: math.ceil(x))

    st.subheader("Product Data")
    st.write(df)

    # -----------------------------
    # Controls
    # -----------------------------

    st.subheader("Planogram Controls")

    layout_mode = st.radio(
        "Layout Style",
        ["Brand Blocking", "Vertical"]
    )

    col1, col2, col3 = st.columns(3)

    generate_default = col1.button("Generate Planogram")
    generate_tier = col2.button("Optimize by Tier")
    generate_price = col3.button("Optimize by Price")

    # -----------------------------
    # Generate Layout
    # -----------------------------

    if generate_default or generate_tier or generate_price:

        working_df = df.copy()

        # -----------------------------
        # Optimization
        # -----------------------------

        if generate_tier:

            tier_priority = {
                "Premium": 0,
                "Core": 1,
                "Value": 2
            }

            working_df["tier_rank"] = working_df["tier"].map(tier_priority)

            working_df = working_df.sort_values(
                by=["tier_rank", "shelves_needed"],
                ascending=[True, False]
            )

            st.info("Tier Optimization Active")

        elif generate_price:

            working_df = working_df.sort_values(
                by=["price", "shelves_needed"],
                ascending=[False, False]
            )

            st.info("Price Optimization Active")

        else:

            working_df = working_df.sort_values(
                by="shelves_needed",
                ascending=False
            )

            st.info("Standard Layout")

        products = working_df.to_dict("records")

        # -----------------------------
        # Layout Mode
        # -----------------------------

        if layout_mode == "Brand Blocking":

            layout = continuous_flow(products, rows, cols)

        else:

            layout = vertical_layout(products, rows, cols)

        # -----------------------------
        # Metrics
        # -----------------------------

        total_shelves = rows * cols
        used_shelves = working_df["shelves_needed"].sum()

        st.metric(
            "Fixture Utilization",
            f"{used_shelves} / {total_shelves} shelves"
        )

        # -----------------------------
        # Display Planogram
        # -----------------------------

        st.subheader("Planogram Layout")

        grid_df = pd.DataFrame(layout)

        grid_df.columns = [f"Pos {i+1}" for i in range(len(grid_df.columns))]
        grid_df.index = [f"Shelf {i+1}" for i in range(len(grid_df))]

        st.dataframe(
            grid_df.style.map(highlight_brands),
            use_container_width=True
        )
