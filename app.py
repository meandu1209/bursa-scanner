import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Bursa Debug", layout="wide")
st.title("Bursa Debug Test")

ticker = st.text_input("Ticker", value="MAYBANK.KL")

if st.button("Test One Ticker"):
    df = yf.download(ticker, period="6mo", progress=False, auto_adjust=False)

    st.subheader("Raw Data")
    st.write(df)

    st.subheader("Columns")
    st.write(df.columns.tolist())

    st.subheader("Shape")
    st.write(df.shape)

    st.subheader("Tail")
    st.write(df.tail())

    if df.empty:
        st.error("DataFrame is empty")
    else:
        st.success("Data received")