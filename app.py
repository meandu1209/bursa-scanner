import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="Bursa Top 100 Scanner", layout="wide")
st.title("Bursa Malaysia Top 100 Stocks Scanner")

tickers = [
    "MAYBANK.KL", "PBBANK.KL", "TENAGA.KL", "CIMB.KL", "IHH.KL", "PMETAL.KL",
    "HLBANK.KL", "SDG.KL", "RHBBANK.KL", "MISC.KL", "YTLPOWR.KL", "SUNWAY.KL",
    "PETGAS.KL", "PCHEM.KL", "CDB.KL", "99SMART.KL", "TM.KL", "IOICORP.KL",
    "GAMUDA.KL", "MAXIS.KL"
]

if st.button("Run Batch Scanner"):
    with st.spinner("Fetching data in batches..."):
        results = []
        debug_rows = []
        chunk_size = 5

        for i in range(0, len(tickers), chunk_size):
            chunk = tickers[i:i + chunk_size]
            data = yf.download(chunk, period="3mo", group_by="ticker", progress=False, auto_adjust=False)

            st.write("Chunk:", chunk)
            st.write("Columns:", data.columns)

            for ticker in chunk:
                try:
                    df = data[ticker] if len(chunk) > 1 else data

                    if df.empty:
                        debug_rows.append({"Ticker": ticker, "Status": "Empty dataframe"})
                        continue

                    if len(df) < 60:
                        debug_rows.append({"Ticker": ticker, "Status": f"Only {len(df)} rows"})
                        continue

                    sma10 = df["Close"].rolling(10).mean().iloc[-1]
                    sma20 = df["Close"].rolling(20).mean().iloc[-1]
                    sma60 = df["Close"].rolling(60).mean().iloc[-1]
                    price = df["Close"].iloc[-1]
                    is_green = df["Close"].iloc[-1] > df["Open"].iloc[-1]
                    is_uptrend = sma10 > sma20 > sma60

                    results.append({
                        "Ticker": ticker.replace(".KL", ""),
                        "Price": round(float(price), 2),
                        "SMA10": round(float(sma10), 2),
                        "SMA20": round(float(sma20), 2),
                        "SMA60": round(float(sma60), 2),
                        "Matches Criteria": bool(is_uptrend and is_green)
                    })

                    debug_rows.append({"Ticker": ticker, "Status": "OK"})

                except Exception as e:
                    debug_rows.append({"Ticker": ticker, "Status": f"Error: {str(e)}"})

            time.sleep(1)

        st.subheader("Debug Status")
        st.dataframe(pd.DataFrame(debug_rows), use_container_width=True)

        df_results = pd.DataFrame(results)

        if df_results.empty:
            st.warning("No results returned.")
        else:
            st.dataframe(
                df_results.sort_values(by="Matches Criteria", ascending=False).reset_index(drop=True),
                use_container_width=True
            )