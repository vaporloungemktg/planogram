import streamlit as st
import pandas as pd
import math
import random

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


import random


def highlight_brands(val):

    if val is None:
        return ""

    if val not in brand_palette:

        # Generate random readable color
        r = random.randint(80, 200)
        g = random.randint(80, 200)
        b = random.randint(80, 200)

        brand_palette[val] = f"#{r:02x}{g:02x}{b:02x}"

    color = brand_palette[val]

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

    # Layout Style
    layout_style = st.radio(
        "Layout Style",
        ["Brand Blocking", "Vertical"]
    )
    
    # Buttons
    generate_default = st.button("Generate Planogram")
    generate_tier = st.button("Optimize by Tier")
    generate_price = st.button("Optimize by Price")
    generate_alpha = st.button("Optimize Alphabetically")
    generate_priority = st.button("Optimize by Priority")

    # -----------------------------
    # Generate Layout
    # -----------------------------

    if generate_default or generate_tier or generate_price or generate_alpha or generate_priority:

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
        
        
        elif generate_alpha:
        
            working_df = working_df.sort_values(
                by=["product_name", "shelves_needed"],
                ascending=[True, False]
            )
        
            st.info("Alphabetical Optimization Active")
        
        
        elif generate_priority:
        
            working_df = working_df.sort_values(
                by=["priority", "shelves_needed"],
                ascending=[True, False]
            )
        
            st.info("Priority Optimization Active")
        
        
        else:
        
            working_df = working_df.sort_values(
                by="shelves_needed",
                ascending=False
            )
        
            st.info("Standard Layout")

        # -----------------------------
        # Layout Mode
        # -----------------------------

        if layout_style == "Brand Blocking":
            layout = brand_block_layout(products, rows, cols)
        elif layout_style == "Vertical":
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
        
        # Remove empty shelves
        grid_df = pd.DataFrame(layout)

        grid_df = grid_df.fillna("COMING SOON")
        
        grid_df.columns = [str(i+1) for i in range(len(grid_df.columns))]
        grid_df.index = [chr(65+i) for i in range(len(grid_df))]
        
        grid_df.index.name = "Shelf"
        
        table_height = (len(grid_df) * 45) + 40
        
        st.dataframe(
            grid_df.style.map(highlight_brands),
            use_container_width=True,
            height=table_height
        )
        # -----------------------------
        # Download Planogram
        # -----------------------------
        
        st.subheader("Download Planogram")
        
        csv = grid_df.to_csv(index=True)
        
        st.download_button(
            label="Download Planogram (CSV)",
            data=csv,
            file_name="planogram.csv",
            mime="text/csv",
        )
        
        # Excel download
        from io import BytesIO
        
        excel_buffer = BytesIO()
        
        with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
        
            grid_df.to_excel(writer, sheet_name="Planogram")
        
            workbook = writer.book
            worksheet = writer.sheets["Planogram"]
        
            # Loop through cells and apply color formatting
            for r in range(len(grid_df)):
                for c in range(len(grid_df.columns)):
        
                    brand = grid_df.iloc[r, c]
        
                    if brand is None:
                        continue
        
                    color = brand_palette.get(brand)
        
                    # If brand has no defined color, skip
                    if color is None:
                        continue
        
                    cell_format = workbook.add_format({
                        "bg_color": color,
                        "font_color": "white",
                        "bold": True,
                        "align": "center"
                    })
        
                    worksheet.write(r+1, c+1, brand, cell_format)
        
        st.download_button(
            label="Download Planogram (Excel)",
            data=excel_buffer.getvalue(),
            file_name="planogram.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
