import streamlit as st
import pandas as pd

st.set_page_config(page_title="Pouch Planogram", layout="wide")

st.title("Nicotine Pouch Planogram Worksheet")
st.write("Welcome to the vaporloungemktg planogram builder.")

# Simple Layout Example
st.header("Shelf Layout")
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Tier 1")
    st.text_input("Product 1", value="ZYN Wintergreen 6mg")
    st.text_input("Product 2", value="ZYN Cool Mint 6mg")

with col2:
    st.subheader("Tier 2")
    st.text_input("Product 3", value="ROGUE Apple 6mg")
    st.text_input("Product 4", value="ROGUE Honey Lemon 6mg")

with col3:
    st.subheader("Tier 3")
    st.text_input("Product 5", value="ON! Berry 4mg")
    st.text_input("Product 6", value="ON! Coffee 4mg")
