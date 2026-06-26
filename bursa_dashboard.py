import streamlit as st
import yfinance as yf

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

if st.button("Run Scanner"):
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, ticker in enumerate(tickers):
        # Update progress
        progress = (i + 1) / len(tickers)
        progress_bar.progress(progress)
        status_text.text(f"Scanning {ticker} ({i+1}/{len(tickers)})...")
        
        # Fetch data
        stock = yf.Ticker(ticker)
        data = stock.history(period="1mo")
        
        if not data.empty:
            with st.expander(f"Chart for {ticker}"):
                st.line_chart(data['Close'])
    
    status_text.text("Scan Complete!")

st.write("Click 'Run Scanner' to load charts for the Top 100 constituents.")