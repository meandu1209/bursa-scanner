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
    "GAMUDA.KL", "MAXIS.KL", "KLK.KL", "YTL.KL", "IOIPG.KL", "NESTLE.KL",
    "AMBANK.KL", "UTDPLT.KL", "WPRTS.KL", "HLFG.KL", "PETDAG.KL", "AXIATA.KL",
    "KLCC.KL", "MRDIY.KL", "SIME.KL", "KPJ.KL", "GENM.KL", "GENTING.KL",
    "PPB.KL", "QL.KL", "DIALOG.KL", "BKAWAN.KL", "HARTA.KL", "AIRPORT.KL",
    "TELEKOM.KL", "AASIA.KL", "IJMPLNT.KL", "YTLCMT.KL", "SUPERMAX.KL",
    "HSPLANT.KL", "AEON.KL", "HAPSENG.KL", "KFC.KL", "LITRAK.KL", "MEGB.KL",
    "NCB.KL", "UNISEM.KL", "POS.KL", "MAHSING.KL", "MPI.KL", "AFG.KL",
    "AFFIN.KL", "F&N.KL", "SPSETIA.KL", "TOPGLOV.KL", "BURSA.KL", "BSTEAD.KL",
    "AIRASIA.KL", "SHELL.KL", "JCY.KL", "ORIENT.KL", "MAYBULK.KL",
    "TCHONG.KL", "SAPCRES.KL", "IGB.KL", "STAR.KL", "IJMLAND.KL",
    "KULIM.KL", "KENCANA.KL", "GAB.KL", "MPHB.KL", "TITAN.KL", "LPI.KL",
    "MUDAJAYA.KL", "MEDIA.KL", "KNM.KL", "MRCB.KL", "DRBHCOM.KL", "WCT.KL",
    "VITROX.KL", "FRONTKN.KL", "TIMECOM.KL", "UWC.KL", "SLVEST.KL",
    "DUFU.KL", "SIMEPROP.KL", "KGB.KL", "SKYECHIP.KL", "DNEX.KL", "VELESTO.KL"
]

def normalize_columns(df):
    if isinstance(df.columns, pd.MultiIndex):
        if len(df.columns[0]) == 2:
            first_level = [col[0] for col in df.columns]
            second_level = [col[1] for col in df.columns]

            if "Close" in first_level or "Open" in first_level:
                df.columns = first_level
            elif "Close" in second_level or "Open" in second_level:
                df.columns = second_level
    return df

if st.button("Run Batch Scanner"):
    with st.spinner("Scanning Bursa stocks..."):
        results = []
        failed = []
        progress = st.progress(0)
        total = len(tickers)

        for idx, ticker in enumerate(tickers):
            try:
                df = yf.download(ticker, period="6mo", progress=False, auto_adjust=False)

                if df.empty:
                    failed.append(ticker.replace(".KL", ""))
                    progress.progress((idx + 1) / total)
                    time.sleep(0.15)
                    continue

                df = normalize_columns(df)
                df = df.dropna()

                required_cols = ["Open", "Close"]

                if len(df) < 60 or not all(col in df.columns for col in required_cols):
                    failed.append(ticker.replace(".KL", ""))
                    progress.progress((idx + 1) / total)
                    time.sleep(0.15)
                    continue

                sma10 = df["Close"].rolling(window=10).mean().iloc[-1]
                sma20 = df["Close"].rolling(window=20).mean().iloc[-1]
                sma60 = df["Close"].rolling(window=60).mean().iloc[-1]
                price = df["Close"].iloc[-1]

                if pd.isna(sma10) or pd.isna(sma20) or pd.isna(sma60) or pd.isna(price):
                    failed.append(ticker.replace(".KL", ""))
                    progress.progress((idx + 1) / total)
                    time.sleep(0.15)
                    continue

                is_uptrend = sma10 > sma20 > sma60
                is_green = df["Close"].iloc[-1] > df["Open"].iloc[-1]

                results.append({
                    "Ticker": ticker.replace(".KL", ""),
                    "Price": round(float(price), 2),
                    "SMA10": round(float(sma10), 2),
                    "SMA20": round(float(sma20), 2),
                    "SMA60": round(float(sma60), 2),
                    "Matches Criteria": bool(is_uptrend and is_green)
                })

            except Exception:
                failed.append(ticker.replace(".KL", ""))

            progress.progress((idx + 1) / total)
            time.sleep(0.15)

        df_results = pd.DataFrame(results)

        if df_results.empty:
            st.warning("No valid stock data returned.")
        else:
            df_results = df_results.sort_values(
                by=["Matches Criteria", "Ticker"],
                ascending=[False, True]
            ).reset_index(drop=True)

            st.dataframe(
                df_results,
                use_container_width=True,
                column_config={
                    "Matches Criteria": st.column_config.CheckboxColumn("Matches Criteria")
                }
            )

        if failed:
            st.caption(f"Skipped {len(failed)} tickers with missing or invalid data.")