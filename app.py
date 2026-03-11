import streamlit as st
import pandas as pd
from layout_engine import continuous_flow

st.title("Dynamic Planogram Builder")

uploaded_file = st.file_uploader("Upload Product CSV")

rows = st.number_input("Shelves",1,20,6)
cols = st.number_input("Columns",1,50,10)

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.write("Product Data", df)

    products = df.to_dict("records")

    if st.button("Generate Planogram"):

        layout = continuous_flow(products, rows, cols)

        st.write("Planogram Layout")

        for r in layout:
            st.write(r)
