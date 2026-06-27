import streamlit as st
import yfinance as yf
import pandas as pd

# Set page configuration
st.set_page_config(page_title="Bursa Top 100 Scanner", layout="wide")
st.title("Bursa Malaysia Top 100 Stocks Scanner")

# List of 100 major Bursa Malaysia tickers
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

if st.button("Run Batch Scanner"):
    with st.spinner("Fetching data and calculating indicators..."):
        # Batch download for speed
        data = yf.download(tickers, period="3mo", group_by='ticker', progress=False)
        
        results = []
        for ticker in tickers:
            try:
                # Ensure data exists for this ticker
                if ticker not in data: continue
                df = data[ticker]
                if len(df) < 60: continue
                
                # Calculate SMAs
                sma10 = df['Close'].rolling(window=10).mean().iloc[-1]
                sma20 = df['Close'].rolling(window=20).mean().iloc[-1]
                sma60 = df['Close'].rolling(window=60).mean().iloc[-1]
                price = df['Close'].iloc[-1]
                
                # Logic: SMA10 > SMA20 > SMA60 AND price > open (Green)
                is_uptrend = (sma10 > sma20 > sma60)
                is_green = df['Close'].iloc[-1] > df['Open'].iloc[-1]
                
                results.append({
                    "Ticker": ticker.replace(".KL", ""),
                    "Price": round(float(price), 2),
                    "SMA10": round(float(sma10), 2),
                    "SMA20": round(float(sma20), 2),
                    "SMA60": round(float(sma60), 2),
                    "Matches Criteria": (is_uptrend and is_green)
                })
            except Exception:
                continue

        # Convert to DataFrame
        df_results = pd.DataFrame(results)
        
        # Display as a clean, sortable table
        st.dataframe(
            df_results.sort_values(by="Matches Criteria", ascending=False).reset_index(drop=True),
            use_container_width=True,
            column_config={
                "Matches Criteria": st.column_config.CheckboxColumn("Matches Criteria")
            }
        )

st.write("Click 'Run Batch Scanner' to load the consolidated table.")