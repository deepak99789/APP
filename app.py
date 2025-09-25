import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import numpy as np
import time

# Page config
st.set_page_config(page_title="Supply Demand Screener", layout="wide")

st.title("Supply Demand Stock Screener")

# Sidebar for inputs
st.sidebar.header("Screener Settings")

# 1. Script Type Selection
script_type = st.sidebar.selectbox(
    "Select Script Type",
    options=[
        "FNO NIFTY50 ALL STOCK",
        "NIFTY 100 ALL STOCK LIST",
        "NIFTY 200 ALL STOCK LIST",
        "NIFTY 500 ALL STOCK LIST"
    ],
    index=0
)

# Full symbol lists for Nifty indices (Yahoo Finance compatible with .NS suffix)
symbol_lists = {
    "FNO NIFTY50 ALL STOCK": [
        "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "HINDUNILVR.NS", "ICICIBANK.NS", "KOTAKBANK.NS",
        "SBIN.NS", "BHARTIARTL.NS", "LT.NS", "ASIANPAINT.NS", "AXISBANK.NS", "MARUTI.NS", "BAJFINANCE.NS",
        "HCLTECH.NS", "ITC.NS", "WIPRO.NS", "ULTRACEMCO.NS", "SUNPHARMA.NS", "TITAN.NS", "NESTLEIND.NS",
        "BAJAJFINSV.NS", "POWERGRID.NS", "M&M.NS", "NTPC.NS", "TECHM.NS", "JSWSTEEL.NS", "TATASTEEL.NS",
        "GRASIM.NS", "DIVISLAB.NS", "HDFCLIFE.NS", "SBILIFE.NS", "BRITANNIA.NS", "ADANIPORTS.NS",
        "CIPLA.NS", "BPCL.NS", "SHREECEM.NS", "EICHERMOT.NS", "HEROMOTOCO.NS", "DRREDDY.NS",
        "TATACONSUM.NS", "UPL.NS", "COALINDIA.NS", "ONGC.NS", "HINDALCO.NS", "INDUSINDBK.NS",
        "ADANIENT.NS", "TATAMOTORS.NS", "BAJAJ-AUTO.NS", "APOLLOHOSP.NS"
    ],
    "NIFTY 100 ALL STOCK LIST": [
        "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "HINDUNILVR.NS", "ICICIBANK.NS", "KOTAKBANK.NS",
        "SBIN.NS", "BHARTIARTL.NS", "LT.NS", "ASIANPAINT.NS", "AXISBANK.NS", "MARUTI.NS", "BAJFINANCE.NS",
        "HCLTECH.NS", "ITC.NS", "WIPRO.NS", "ULTRACEMCO.NS", "SUNPHARMA.NS", "TITAN.NS", "NESTLEIND.NS",
        "BAJAJFINSV.NS", "POWERGRID.NS", "M&M.NS", "NTPC.NS", "TECHM.NS", "JSWSTEEL.NS", "TATASTEEL.NS",
        "GRASIM.NS", "DIVISLAB.NS", "HDFCLIFE.NS", "SBILIFE.NS", "BRITANNIA.NS", "ADANIPORTS.NS",
        "CIPLA.NS", "BPCL.NS", "SHREECEM.NS", "EICHERMOT.NS", "HEROMOTOCO.NS", "DRREDDY.NS",
        "TATACONSUM.NS", "UPL.NS", "COALINDIA.NS", "ONGC.NS", "HINDALCO.NS", "INDUSINDBK.NS",
        "ADANIENT.NS", "TATAMOTORS.NS", "BAJAJ-AUTO.NS", "APOLLOHOSP.NS", "HINDZINC.NS", "PIDILITIND.NS",
        "HAVELLS.NS", "GODREJCP.NS", "DABUR.NS", "MARICO.NS", "SIEMENS.NS", "DMART.NS", "SBICARD.NS",
        "INFOEDGE.NS", "MCDOWELL-N.NS", "AMBUJACEM.NS", "DLF.NS", "BANKBARODA.NS", "INDIGO.NS",
        "COLPAL.NS", "PNB.NS", "IOC.NS", "LUPIN.NS", "BERGEPAINT.NS", "GAIL.NS", "AUROPHARMA.NS",
        "BOSCHLTD.NS", "JUBLFOOD.NS", "BIOCON.NS", "ICICIPRULI.NS", "MUTHOOTFIN.NS", "TORNTPHARM.NS",
        "ICICIGI.NS", "TRENT.NS", "LTIM.NS", "MPHASIS.NS", "ACC.NS", "HDFCAMC.NS", "NAUKRI.NS",
        "TATAPOWER.NS", "ZOMATO.NS", "IDFCFIRSTB.NS", "BANDHANBNK.NS", "BEL.NS",
        "GODREJPROP.NS", "CONCOR.NS", "PETRONET.NS", "ASHOKLEY.NS", "MRF.NS", "VBL.NS",
        "BALKRISIND.NS", "CHOLAFIN.NS"
    ],
    "NIFTY 200 ALL STOCK LIST": [
        "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "HINDUNILVR.NS", "ICICIBANK.NS", "KOTAKBANK.NS",
        "SBIN.NS", "BHARTIARTL.NS", "LT.NS", "ASIANPAINT.NS", "AXISBANK.NS", "MARUTI.NS", "BAJFINANCE.NS",
        "HCLTECH.NS", "ITC.NS", "WIPRO.NS", "ULTRACEMCO.NS", "SUNPHARMA.NS", "TITAN.NS", "NESTLEIND.NS",
        "BAJAJFINSV.NS", "POWERGRID.NS", "M&M.NS", "NTPC.NS", "TECHM.NS", "JSWSTEEL.NS", "TATASTEEL.NS",
        "GRASIM.NS", "DIVISLAB.NS", "HDFCLIFE.NS", "SBILIFE.NS", "BRITANNIA.NS", "ADANIPORTS.NS",
        "CIPLA.NS", "BPCL.NS", "SHREECEM.NS", "EICHERMOT.NS", "HEROMOTOCO.NS", "DRREDDY.NS",
        "TATACONSUM.NS", "UPL.NS", "COALINDIA.NS", "ONGC.NS", "HINDALCO.NS", "INDUSINDBK.NS",
        "ADANIENT.NS", "TATAMOTORS.NS", "BAJAJ-AUTO.NS", "APOLLOHOSP.NS", "HINDZINC.NS", "PIDILITIND.NS",
        "HAVELLS.NS", "GODREJCP.NS", "DABUR.NS", "MARICO.NS", "SIEMENS.NS", "DMART.NS", "SBICARD.NS",
        "INFOEDGE.NS", "MCDOWELL-N.NS", "AMBUJACEM.NS", "DLF.NS", "BANKBARODA.NS", "INDIGO.NS",
        "COLPAL.NS", "PNB.NS", "IOC.NS", "LUPIN.NS", "BERGEPAINT.NS", "GAIL.NS", "AUROPHARMA.NS",
        "BOSCHLTD.NS", "JUBLFOOD.NS", "BIOCON.NS", "ICICIPRULI.NS", "MUTHOOTFIN.NS", "TORNTPHARM.NS",
        "ICICIGI.NS", "TRENT.NS", "LTIM.NS", "MPHASIS.NS", "ACC.NS", "HDFCAMC.NS", "NAUKRI.NS",
        "TATAPOWER.NS", "ZOMATO.NS", "IDFCFIRSTB.NS", "BANDHANBNK.NS", "BEL.NS",
        "GODREJPROP.NS", "CONCOR.NS", "PETRONET.NS", "ASHOKLEY.NS", "MRF.NS", "VBL.NS",
        "BALKRISIND.NS", "CHOLAFIN.NS", "APOLLOTYRE.NS", "BATAINDIA.NS", "BHARATFORG.NS", "CANBK.NS",
        "CUMMINSIND.NS", "DEEPAKNTR.NS", "ESCORTS.NS", "EXIDEIND.NS", "GLENMARK.NS", "GMRINFRA.NS",
        "HAL.NS", "IGL.NS", "INDHOTEL.NS", "JINDALSTEL.NS", "LICHSGFIN.NS", "MFSL.NS", "NMDC.NS",
        "OBEROIRLTY.NS", "PVRINOX.NS", "SAIL.NS", "SYNGENE.NS", "TATACOMM.NS", "TVSMOTOR.NS",
        "UBL.NS", "VEDL.NS", "ZEEL.NS", "AARTIIND.NS", "ABBOTINDIA.NS", "ALKEM.NS", "ATUL.NS",
        "BHEL.NS", "COFORGE.NS", "COROMANDEL.NS", "CROMPTON.NS", "DIXON.NS", "EMAMILTD.NS",
        "FEDERALBNK.NS", "FORTIS.NS", "GUJGASLTD.NS", "IDEA.NS", "IPCALAB.NS", "JUBLPHARMA.NS",
        "LAURUSLABS.NS", "LTTS.NS", "MANAPPURAM.NS", "MCX.NS", "MGL.NS", "NATCOPHARM.NS",
        "NAVINFLUOR.NS", "PHOENIXLTD.NS", "POLYCAB.NS", "PRESTIGE.NS", "RAMCOCEM.NS", "RECLTD.NS",
        "SRF.NS", "SUNTV.NS", "TATACHEM.NS", "TIINDIA.NS", "TORNTPOWER.NS", "VOLTAS.NS",
        "WHIRLPOOL.NS", "YESBANK.NS", "ZYDUSLIFE.NS"
    ],
    "NIFTY 500 ALL STOCK LIST": [
        "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "HINDUNILVR.NS", "ICICIBANK.NS", "KOTAKBANK.NS",
        "SBIN.NS", "BHARTIARTL.NS", "LT.NS", "ASIANPAINT.NS", "AXISBANK.NS", "MARUTI.NS", "BAJFINANCE.NS",
        "HCLTECH.NS", "ITC.NS", "WIPRO.NS", "ULTRACEMCO.NS", "SUNPHARMA.NS", "TITAN.NS", "NESTLEIND.NS",
        "BAJAJFINSV.NS", "POWERGRID.NS", "M&M.NS", "NTPC.NS", "TECHM.NS", "JSWSTEEL.NS", "TATASTEEL.NS",
        "GRASIM.NS", "DIVISLAB.NS", "HDFCLIFE.NS", "SBILIFE.NS", "BRITANNIA.NS", "ADANIPORTS.NS",
        "CIPLA.NS", "BPCL.NS", "SHREECEM.NS", "EICHERMOT.NS", "HEROMOTOCO.NS", "DRREDDY.NS",
        "TATACONSUM.NS", "UPL.NS", "COALINDIA.NS", "ONGC.NS", "HINDALCO.NS", "INDUSINDBK.NS",
        "ADANIENT.NS", "TATAMOTORS.NS", "BAJAJ-AUTO.NS", "APOLLOHOSP.NS", "HINDZINC.NS", "PIDILITIND.NS",
        "HAVELLS.NS", "GODREJCP.NS", "DABUR.NS", "MARICO.NS", "SIEMENS.NS", "DMART.NS", "SBICARD.NS",
        "INFOEDGE.NS", "MCDOWELL-N.NS", "AMBUJACEM.NS", "DLF.NS", "BANKBARODA.NS", "INDIGO.NS",
        "COLPAL.NS", "PNB.NS", "IOC.NS", "LUPIN.NS", "BERGEPAINT.NS", "GAIL.NS", "AUROPHARMA.NS",
        "BOSCHLTD.NS", "JUBLFOOD.NS", "BIOCON.NS", "ICICIPRULI.NS", "MUTHOOTFIN.NS", "TORNTPHARM.NS",
        "ICICIGI.NS", "TRENT.NS", "LTIM.NS", "MPHASIS.NS", "ACC.NS", "HDFCAMC.NS", "NAUKRI.NS",
        "TATAPOWER.NS", "ZOMATO.NS", "IDFCFIRSTB.NS", "BANDHANBNK.NS", "BEL.NS",
        "GODREJPROP.NS", "CONCOR.NS", "PETRONET.NS", "ASHOKLEY.NS", "MRF.NS", "VBL.NS",
        "BALKRISIND.NS", "CHOLAFIN.NS", "APOLLOTYRE.NS", "BATAINDIA.NS", "BHARATFORG.NS", "CANBK.NS",
        "CUMMINSIND.NS", "DEEPAKNTR.NS", "ESCORTS.NS", "EXIDEIND.NS", "GLENMARK.NS", "GMRINFRA.NS",
        "HAL.NS", "IGL.NS", "INDHOTEL.NS", "JINDALSTEL.NS", "LICHSGFIN.NS", "MFSL.NS", "NMDC.NS",
        "OBEROIRLTY.NS", "PVRINOX.NS", "SAIL.NS", "SYNGENE.NS", "TATACOMM.NS", "TVSMOTOR.NS",
        "UBL.NS", "VEDL.NS", "ZEEL.NS", "AARTIIND.NS", "ABBOTINDIA.NS", "ALKEM.NS", "ATUL.NS",
        "BHEL.NS", "COFORGE.NS", "COROMANDEL.NS", "CROMPTON.NS", "DIXON.NS", "EMAMILTD.NS",
        "FEDERALBNK.NS", "FORTIS.NS", "GUJGASLTD.NS", "IDEA.NS", "IPCALAB.NS", "JUBLPHARMA.NS",
        "LAURUSLABS.NS", "LTTS.NS", "MANAPPURAM.NS", "MCX.NS", "MGL.NS", "NATCOPHARM.NS",
        "NAVINFLUOR.NS", "PHOENIXLTD.NS", "POLYCAB.NS", "PRESTIGE.NS", "RAMCOCEM.NS", "RECLTD.NS",
        "SRF.NS", "SUNTV.NS", "TATACHEM.NS", "TIINDIA.NS", "TORNTPOWER.NS", "VOLTAS.NS",
        "WHIRLPOOL.NS", "YESBANK.NS", "ZYDUSLIFE.NS", "3MINDIA.NS", "AIAENG.NS", "ABB.NS",
        "ABFRL.NS", "ADANIGREEN.NS", "ADANITRANS.NS", "AMARAJABAT.NS", "AMBER.NS", "APLLTD.NS",
        "ASHOKA.NS", "ASTRAL.NS", "BALRAMCHIN.NS", "BANKINDIA.NS", "BBTC.NS", "BIRLACORPN.NS",
        "BLUEDART.NS", "BSOFT.NS", "CENTURYTEX.NS", "CESC.NS", "CHAMBLFERT.NS", "CHOLAHLDNG.NS",
        "CLEAN.NS", "COCHINSHIP.NS", "CONTAINER.NS", "CREDITACC.NS", "CRISIL.NS", "CUB.NS",
        "CYIENT.NS", "DALBHARAT.NS", "DBL.NS", "DHANI.NS", "EDELWEISS.NS", "EIDPARRY.NS",
        "ELGIEQUIP.NS", "ENDURANCE.NS", "ENGINERSIN.NS", "FINCABLES.NS", "FINEORG.NS",
        "FSL.NS", "GALAXYSURF.NS", "GICRE.NS", "GLAXO.NS", "GNFC.NS", "GODREJAGRO.NS",
        "GODREJIND.NS", "GRANULES.NS", "GRAPHITE.NS", "GRINDWELL.NS", "GSPL.NS", "HAPPSTMNDS.NS",
        "HATHWAY.NS", "HBLPOWER.NS", "HEG.NS", "HINDCOPPER.NS", "HINDPETRO.NS", "HONAUT.NS",
        "HUDCO.NS", "IBULHSGFIN.NS", "IEX.NS", "INDIAMART.NS", "INDIANB.NS", "INDIGO.NS",
        "INFIBEAM.NS", "IRB.NS", "IRCON.NS", "IRCTC.NS", "ITI.NS", "JAMNAAUTO.NS", "JBCHEPHARM.NS",
        "JKCEMENT.NS", "JKLAKSHMI.NS", "JKTYRE.NS", "JMFINANCIL.NS", "JUSTDIAL.NS",
        "JYOTHYLAB.NS", "KAJARIACER.NS", "KALPATPOWR.NS", "KANSAINER.NS", "KARURVYSYA.NS",
        "KEC.NS", "KNRCON.NS", "KPITTECH.NS", "KRBL.NS", "KSB.NS", "LALPATHLAB.NS",
        "LEMONTREE.NS", "LINDEINDIA.NS", "LUXIND.NS", "MAHABANK.NS", "MAHINDCIE.NS", "MAHLIFE.NS",
        "MAHLOG.NS", "MANGLMCEM.NS", "METROBRAND.NS", "METROPOLIS.NS", "MINDACORP.NS",
        "MMTC.NS", "MOTILALOFS.NS", "MOTHERSUMI.NS", "MRPL.NS", "NAM-INDIA.NS", "NATIONALUM.NS",
        "NBCC.NS", "NCC.NS", "NH.NS", "NHPC.NS", "NIITLTD.NS", "NLCINDIA.NS", "OBCL.NS",
        "OFSS.NS", "OIL.NS", "PAGEIND.NS", "PATANJALI.NS", "PERSISTENT.NS", "PFIZER.NS",
        "PNBHOUSING.NS", "PNCINFRA.NS", "POWERINDIA.NS", "PRINCEPIPE.NS", "PRSMJOHNSN.NS",
        "RADICO.NS", "RAIN.NS", "RAJESHEXPO.NS", "RALLIS.NS", "RATNAMANI.NS", "RAYMOND.NS",
        "RBLBANK.NS", "RELAXO.NS", "ROSSARI.NS", "ROUTE.NS", "RVNL.NS", "SANOFI.NS",
        "SCHAEFFLER.NS", "SHILPAMED.NS", "SHRIRAMCIT.NS", "SKFINDIA.NS", "SOLARINDS.NS",
        "SONATSOFTW.NS", "SPARC.NS", "STAR.NS", "SUDARSCHEM.NS", "SUMICHEM.NS", "SUNDARMFIN.NS",
        "SUNDRMFAST.NS", "SUPRAJIT.NS", "SUPREMEIND.NS", "SUVENPHAR.NS", "SYMPHONY.NS",
        "TANLA.NS", "TATAELXSI.NS", "TATAINVEST.NS", "TCIEXP.NS", "TEAMLEASE.NS", "THERMAX.NS",
        "TRIDENT.NS", "TTKPRESTIG.NS", "TV18BRDCST.NS", "UCOBANK.NS", "UFLEX.NS", "UNIONBANK.NS",
        "VAIBHAVGBL.NS", "VGUARD.NS", "VINATIORGA.NS", "VIPIND.NS", "WELCORP.NS", "WELSPUNIND.NS",
        "WESTLIFE.NS", "ZENSARTECH.NS"
    ]
}
symbols = symbol_lists.get(script_type, ["RELIANCE.NS"])
custom_symbols = st.sidebar.text_area("Or Enter Custom Symbols (comma-separated)", value=",".join(symbols[:5]))
if custom_symbols:
    symbols = [s.strip() for s in custom_symbols.split(",") if s.strip()]

start_date = st.sidebar.date_input("Start Date", datetime.now() - timedelta(days=30))
end_date = st.sidebar.date_input("End Date", datetime.now())

# 2. Number of Base Candles
num_base_candles = st.sidebar.slider("Number of Base Candles", min_value=1, max_value=6, value=1)

# 3. Time Interval
intervals = {
    "1 Min": "1m",
    "5 Min": "5m",
    "15 Min": "15m",
    "30 Min": "30m",
    "60 Min": "60m",
    "75 Min": "75m",
    "125 Min": "2h",
    "1 HR": "1h",
    "2 HR": "2h",
    "4 HR": "4h",
    "DAILY": "1d",
    "WEEKLY": "1wk"
}
display_intervals = list(intervals.keys())
selected_interval_display = st.sidebar.selectbox("Select Time Interval", options=display_intervals, index=10)
yf_interval = intervals[selected_interval_display]

# 4. Zone Status
zone_status = st.sidebar.selectbox("Zone Status", options=["ALL", "FRESH", "TARGET", "STOPLOSS"], index=0)

# 5. Zone Type
zone_type = st.sidebar.selectbox("Zone Type", options=["ALL", "SUPPLY", "DEMAND"], index=0)

# Pattern Settings
st.sidebar.header("Pattern Settings")
min_body_rally_drop = st.sidebar.slider("Min Body % for Rally/Drop", 0, 100, 80)
max_body_base = st.sidebar.slider("Max Body % for Base", 0, 100, 50)

# Risk-Reward Settings
st.sidebar.header("Entry & Stoploss Settings")
rr_ratio = 5.0  # Fixed RR 1:5
sl_buffer_pct = st.sidebar.number_input("Stoploss Buffer %", min_value=0.0, value=1.0, step=0.5)

# Fetch data function with retry logic
@st.cache_data
def fetch_data(symbols, start, end, interval):
    data = {}
    for symbol in symbols:
        for attempt in range(3):  # Retry up to 3 times
            try:
                df = yf.download(symbol, start=start, end=end, interval=interval, progress=False)
                if not df.empty and all(col in df.columns for col in ['High', 'Low', 'Close', 'Open']):
                    # Ensure no NaN values in critical columns and convert to float
                    df = df.dropna(subset=['High', 'Low', 'Close', 'Open'])
                    df[['High', 'Low', 'Close', 'Open']] = df[['High', 'Low', 'Close', 'Open']].astype(float)
                    if not df.empty:
                        data[symbol] = df
                        st.info(f"Successfully fetched data for {symbol} ({len(df)} rows).")
                        break
                    else:
                        st.warning(f"No valid data for {symbol} after cleaning (all rows dropped due to NaN).")
                else:
                    st.warning(f"No valid data for {symbol} (empty or missing columns).")
            except Exception as e:
                st.error(f"Error fetching {symbol} (attempt {attempt+1}/3): {e}")
                time.sleep(1)  # Wait before retrying
            if attempt == 2:
                st.error(f"Failed to fetch data for {symbol} after 3 attempts.")
    return data

# Function to classify a single candle
def classify_candle(row, min_body_rd, max_body_b):
    try:
        high_low_range = float(row['High'] - row['Low'])
        if high_low_range <= 0:
            return 'Neutral'
        
        body = abs(float(row['Close'] - row['Open']))
        body_pct = (body / high_low_range) * 100
        
        is_green = float(row['Close']) > float(row['Open'])
        is_red = float(row['Close']) < float(row['Open'])
        
        if body_pct > min_body_rd:
            if is_green:
                return 'Rally'
            elif is_red:
                return 'Drop'
        elif body_pct < max_body_b:
            return 'Base'
        
        return 'Neutral'
    except (TypeError, ValueError):
        return 'Neutral'  # Handle invalid data

# Function to detect patterns with Entry/Stoploss
def detect_pattern(df, min_body_rd, max_body_b, num_bases, required_zone_type, rr_ratio, sl_buffer_pct):
    if len(df) < 2 + num_bases:
        return 'No Pattern', 0.0, 0.0, 0, 0.0, 0.0, 0.0, 'NONE'
    
    df['Candle_Type'] = df.apply(lambda row: classify_candle(row, min_body_rd, max_body_b), axis=1)
    recent_candles = df.iloc[-(2 + num_bases):]
    candle_types = recent_candles['Candle_Type'].values
    
    if len(candle_types) < 2 + num_bases:
        return 'No Pattern', 0.0, 0.0, 0, 0.0, 0.0, 0.0, 'NONE'
    
    leg_in = candle_types[0]
    bases = candle_types[1:1+num_bases]
    leg_out = candle_types[-1]
    
    if all(b == 'Base' for b in bases):
        pattern = None
        is_demand = False
        
        # Check if base_candles has valid data
        base_candles = recent_candles.iloc[1:1+num_bases]
        if base_candles.empty or base_candles['High'].isna().all() or base_candles['Low'].isna().all():
            return 'No Pattern', 0.0, 0.0, 0, 0.0, 0.0, 0.0, 'NONE'
        
        try:
            zone_low = float(min(recent_candles['Low']))
            zone_high = float(max(recent_candles['High']))
            base_max_high = float(max(base_candles['High']))  # Max high of base candles
            base_min_low = float(min(base_candles['Low']))   # Min low of base candles
        except (ValueError, TypeError):
            return 'No Pattern', 0.0, 0.0, 0, 0.0, 0.0, 0.0, 'NONE'
        
        # Pattern detection
        if leg_in == 'Rally' and leg_out == 'Rally':
            pattern = 'RBR'
            is_demand = True
        elif leg_in == 'Rally' and leg_out == 'Drop':
            pattern = 'RBD'
            is_demand = False
        elif leg_in == 'Drop' and leg_out == 'Drop':
            pattern = 'DBD'
            is_demand = False
        elif leg_in == 'Drop' and leg_out == 'Rally':
            pattern = 'DBR'
            is_demand = True
        
        if not pattern:
            return 'No Pattern', 0.0, 0.0, 0, 0.0, 0.0, 0.0, 'NONE'
        
        # Filter by zone type
        if required_zone_type != "ALL" and ((required_zone_type == "DEMAND" and not is_demand) or (required_zone_type == "SUPPLY" and is_demand)):
            return 'No Pattern', 0.0, 0.0, 0, 0.0, 0.0, 0.0, 'NONE'
        
        # Entry and Stoploss logic
        try:
            current_price = float(df.iloc[-1]['Close'])
        except (ValueError, TypeError):
            return 'No Pattern', 0.0, 0.0, 0, 0.0, 0.0, 0.0, 'NONE'
        
        entry_price = base_max_high if is_demand else base_min_low
        sl_price = zone_low * (1 - sl_buffer_pct / 100) if is_demand else zone_high * (1 + sl_buffer_pct / 100)
        risk = abs(entry_price - sl_price)
        target_price = entry_price + (risk * rr_ratio) if is_demand else entry_price - (risk * rr_ratio)
        
        # Zone Status
        if is_demand:
            if current_price >= base_max_high:
                if current_price >= target_price:
                    status = 'TARGET'
                elif current_price <= sl_price:
                    status = 'STOPLOSS'
                else:
                    status = 'FRESH'
            else:
                status = 'FRESH'
        else:
            if current_price <= base_min_low:
                if current_price <= target_price:
                    status = 'TARGET'
                elif current_price >= sl_price:
                    status = 'STOPLOSS'
                else:
                    status = 'FRESH'
            else:
                status = 'FRESH'
        
        # Filter by zone status
        if zone_status != "ALL" and zone_status != status:
            return 'No Pattern', 0.0, 0.0, 0, 0.0, 0.0, 0.0, 'NONE'
        
        demand_score = 1.0 if is_demand else 0.0
        supply_score = 1.0 - demand_score
        return (
            f"{pattern} ({'Demand' if is_demand else 'Supply'})",
            demand_score,
            supply_score,
            1,
            entry_price,
            sl_price,
            target_price,
            status
        )
    
    return 'No Pattern', 0.0, 0.0, 0, 0.0, 0.0, 0.0, 'NONE'

# Scan Button
if st.sidebar.button("SCAN"):
    if not symbols:
        st.warning("Please select script type or enter symbols.")
    else:
        with st.spinner(f"Fetching data for {len(symbols)} symbols and scanning..."):
            data = fetch_data(symbols, start_date, end_date, yf_interval)
        
        results = []
        for symbol, df in data.items():
            if not df.empty:
                st.info(f"Processing {symbol} with {len(df)} candles.")
                pattern, demand_score, supply_score, match, entry_price, sl_price, target_price, status = detect_pattern(
                    df, min_body_rally_drop, max_body_base, num_base_candles, zone_type, rr_ratio, sl_buffer_pct
                )
                if match > 0:
                    results.append({
                        'Symbol': symbol,
                        'Pattern': pattern,
                        'Zone_Type': 'Demand' if demand_score > 0 else 'Supply',
                        'Zone_Status': status,
                        'Current_Price': df.iloc[-1]['Close'],
                        'Entry_Price': entry_price,
                        'Stoploss_Price': sl_price,
                        'Target_Price': target_price,
                        'Demand_Score': demand_score,
                        'Supply_Score': supply_score
                    })
                else:
                    st.info(f"No matching pattern found for {symbol}.")
            else:
                st.warning(f"No data available for {symbol}.")
        
        if results:
            df_results = pd.DataFrame(results)
            st.subheader("Scan Results")
            st.dataframe(
                df_results[['Symbol', 'Pattern', 'Zone_Type', 'Zone_Status', 'Current_Price', 'Entry_Price', 'Stoploss_Price', 'Target_Price']],
                use_container_width=True
            )
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Matches", len(df_results))
            with col2:
                demand_count = len(df_results[df_results['Demand_Score'] > 0])
                st.metric("Demand Zones", demand_count)
            with col3:
                supply_count = len(df_results[df_results['Supply_Score'] > 0])
                st.metric("Supply Zones", supply_count)
        else:
            st.info("No matching zones found. Try adjusting the date range (e.g., last 60 days), interval (e.g., DAILY), or symbols.")

# Instructions
with st.expander("Deployment Instructions"):
    st.markdown("""
    1. Create GitHub repo, add `app.py`.
    2. Create `requirements.txt`:
       ```
       streamlit
       pandas
       yfinance>=0.2.41
       numpy
       ```
    3. Deploy on Streamlit Cloud via GitHub (streamlit.io/cloud).
    4. If issues persist, check logs in 'Manage app' and verify symbol list, date range, and interval.
    """)
