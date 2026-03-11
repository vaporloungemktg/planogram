import streamlit as st
import pandas as pd
import math
from layout_engine import continuous_flow

st.title("Dynamic Planogram Builder")

# Upload CSV
uploaded_file = st.file_uploader("Upload Product CSV")

# Planogram dimensions
rows = st.number_input("Shelves", 1, 20, 6)
cols = st.number_input("Columns", 1, 50, 10)

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

    # Calculate total products
    # Convert numeric columns
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

# Calculate shelves needed safely
df["shelves_needed"] = (
    df["total_products"] / df["capacity_per_foot"]
).apply(lambda x: math.ceil(x))

    st.subheader("Product Data")
    st.write(df)

    # Capacity diagnostics
    total_shelf_demand = df["shelves_needed"].sum()
    max_capacity = rows * cols

    st.subheader("Capacity Check")
    st.write("Total Shelf Demand:", total_shelf_demand)
    st.write("Grid Capacity:", max_capacity)

    if total_shelf_demand > max_capacity:
        st.warning("Products exceed available shelf capacity.")

    # Convert dataframe to records for layout engine
    products = df.to_dict("records")

    if st.button("Generate Planogram"):

        layout = continuous_flow(products, rows, cols)

        if layout is None:
            st.error(
                "Planogram overflow: Increase columns or reduce shelf requirements."
            )
        else:

            st.subheader("Planogram Layout")

            for r in layout:
                st.write(r)
