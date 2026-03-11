import streamlit as st
import pandas as pd
import math
from layout_engine import continuous_flow

def highlight_brands(val):

    colors = {
        "Zyn": "#1f77b4",
        "Wyn": "#ff7f0e",
        "Nic Nac": "#2ca02c",
        "Pillowz": "#9467bd",
        "Juice Head": "#d62728",
        "Hyde Strips": "#17becf"
    }

    color = colors.get(val, "#444444")

    return f"background-color: {color}; color: white"

st.title("Dynamic Planogram Builder")

# Upload CSV
uploaded_file = st.file_uploader("Upload Product CSV")

# Planogram dimensions
rows = st.number_input("Rows", 1, 20, 11)
cols = st.number_input("Columns", 1, 50, 4)

if uploaded_file:

    # Load CSV
    df = pd.read_csv(uploaded_file)

    # Convert numeric columns safely
    numeric_columns = [
        "flavor_count",
        "strength_count",
        "capacity_per_foot"
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Remove rows with missing numeric values
    df = df.dropna(subset=numeric_columns)

    # Calculate totals
    df["total_products"] = df["flavor_count"] * df["strength_count"]

    # Calculate shelves needed
    df["shelves_needed"] = (
        df["total_products"] / df["capacity_per_foot"]
    ).apply(lambda x: math.ceil(x))

    st.subheader("Product Data")
    st.write(df)

    products = df.to_dict("records")

    if st.button("Generate Planogram"):
    
        layout = continuous_flow(products, rows, cols)
    
        total_shelves = rows * cols
        used_shelves = df["shelves_needed"].sum()
    
        st.metric(
            "Fixture Utilization",
            f"{used_shelves} / {total_shelves} shelves"
        )
    
        st.subheader("Planogram Layout")
        
        # Convert layout to dataframe grid
        grid_df = pd.DataFrame(layout)
        grid_df.columns = [f"Pos {i+1}" for i in range(len(grid_df.columns))]
        
        # Label rows as shelves
        grid_df.index = [f"Shelf {i+1}" for i in range(len(grid_df))]
        
        st.dataframe(
            grid_df.style.map(highlight_brands),
            use_container_width=True
        )
