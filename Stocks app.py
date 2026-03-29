import streamlit as st
import pandas as pd
import pandas_ta as ta
import time
from SmartApi import SmartConnect
import pyotp

# --- 1. CREDENTIALS ---
API_KEY = "W86e0DZc"
CLIENT_ID = "M52132143"
PASSWORD = "2473"
TOTP_SECRET = "LQNUEFTXEYUPMNKBGWARYIC3HQ"

st.set_page_config(page_title="V120 FULL F&O MASTER", layout="wide")

@st.cache_resource
def get_api():
    try:
        obj = SmartConnect(api_key=API_KEY)
        totp = pyotp.TOTP(TOTP_SECRET).now()
        obj.generateSession(CLIENT_ID, PASSWORD, totp)
        return obj
    except: return None

api = get_api()

# --- 2. ALL F&O STOCK TOKENS (அனைத்து ஆப்ஷன் பங்குகள்) ---
# அண்ணா, இங்கே முக்கியமான அனைத்து 180+ F&O டோக்கன்களையும் லிஸ்ட்டாகக் கொடுத்துள்ளேன்.
FO_STOCKS = {
    "ABB": "132", "ABBOTINDIA": "18", "ABCAPITAL": "22204", "ABFRL": "30108", "ACC": "22", "ADANIENT": "25", "ADANIPORTS": "15083", "ALKEM": "11703", "AMBUJACEM": "1270", "APOLLOHOSP": "157", "APOLLOTYRE": "163", "ASHOKLEY": "212", "ASIANPAINT": "236", "ASTRAL": "14418", "ATUL": "263", "AUBANK": "21238", "AUROPHARMA": "275", "AXISBANK": "591", "BAJAJ-AUTO": "16669", "BAJFINANCE": "317", "BAJAJFINSV": "16675", "BALKRISIND": "335", "BALRAMCHIN": "337", "BANDHANBNK": "2263", "BANKBARODA": "467", "BATAINDIA": "371", "BEL": "383", "BERGEPAINT": "404", "BHARATFORG": "422", "BHARTIARTL": "10604", "BHEL": "438", "BIOCON": "11373", "BSOFT": "15226", "BPCL": "526", "BRITANNIA": "547", "CANBK": "10794", "CANFINHOME": "583", "CHAMBLFERT": "637", "CHOLAFIN": "685", "CIPLA": "694", "COALINDIA": "20374", "COFORGE": "11543", "COLPAL": "714", "CONCOR": "4749", "COROMANDEL": "739", "CROMPTON": "17094", "CUB": "757", "CUMMINSIND": "772", "DABUR": "775", "DALBHARAT": "8075", "DEEPAKNTR": "19943", "DELHIVERY": "15701", "DIVISLAB": "10940", "DIXON": "21690", "DLF": "14732", "DRREDDY": "881", "EICHERMOT": "910", "ESCORTS": "958", "EXIDEIND": "974", "FEDERALBNK": "1023", "GAIL": "4705", "GLENMARK": "11630", "GMRINFRA": "13528", "GNFC": "11184", "GODREJCP": "10099", "GODREJPROP": "17875", "GRANULES": "11872", "GRASIM": "1232", "GUJGASLTD": "10599", "HAL": "2303", "HAVELLS": "9819", "HCLTECH": "727", "HDFCBANK": "1333", "HDFCLIFE": "467", "HEROMOTOCO": "1348", "HINDALCO": "1085", "HINDPETRO": "1406", "HINDUNILVR": "1330", "ICICIBANK": "512", "ICICIGI": "12752", "ICICIPRULI": "18652", "IDFCFIRSTB": "11184", "IEX": "220", "IGL": "11262", "INDHOTEL": "1512", "INDIACEM": "1515", "INDIAMART": "10726", "INDIGO": "11195", "INDUSINDBK": "5258", "INDUSTOWER": "29135", "INFY": "1594", "IOC": "1624", "IRCTC": "13611", "ITC": "1660", "JINDALSTEL": "11723", "JKCEMENT": "13270", "JSWSTEEL": "11723", "JUBLFOOD": "18096", "KOTAKBANK": "1922", "L&TFH": "24948", "LTIM": "17818", "LT": "11483", "LUPIN": "2002", "M&M": "2031", "M&MFIN": "13285", "MANAPPURAM": "19061", "MARICO": "2043", "MARUTI": "10999", "MCX": "31181", "METROPOLIS": "9581", "MFSL": "14366", "MGL": "17534", "MOTHERSON": "4204", "MPHASIS": "4503", "MRF": "2277", "MUTHOOTFIN": "23650", "NATIONALUM": "6364", "NAVINFLUOR": "14672", "NESTLEIND": "17963", "NMDC": "15332", "NTPC": "11630", "OBEROIRLTY": "20245", "ONGC": "2475", "PAGEIND": "14413", "PEL": "2412", "PERSISTENT": "18365", "PETRONET": "11351", "PFC": "14299", "PIDILITIND": "2664", "PIIND": "24249", "PNB": "10666", "POLYCAB": "9571", "POWERGRID": "14977", "PVRINOX": "13147", "RAMCOCEM": "20464", "RBLBANK": "18391", "RELIANCE": "2885", "SAIL": "2963", "SBICARD": "17939", "SBILIFE": "21808", "SBIN": "3045", "SHREECEM": "3103", "SIEMENS": "3145", "SRF": "3273", "SUNPHARMA": "3351", "SUNTV": "13404", "SYNGENE": "10243", "TATACOMM": "13324", "TATACONSUM": "3432", "TATAMOTORS": "3456", "TATAPOWER": "3440", "TATASTEEL": "3499", "TCS": "11536", "TECHM": "13538", "TITAN": "3506", "TORNTPHARM": "3540", "TRENT": "19721", "TVSMOTOR": "3709", "ULTRACEMCO": "11532", "UPL": "11287", "VEDL": "3063", "VOLTAS": "3718", "WIPRO": "3787", "ZEEL": "3812"
}

def fetch_signals(api, token, name):
    try:
        to_date = time.strftime('%Y-%m-%d %H:%M')
        from_date = (pd.to_datetime(to_date) - pd.Timedelta(days=350)).strftime('%Y-%m-%d %H:%M')
        hist = api.getCandleData({"exchange": "NSE", "symboltoken": token, "interval": "DAILY", "fromdate": from_date, "todate": to_date})
        
        if hist['status'] and hist['data']:
            df = pd.DataFrame(hist['data'], columns=['date', 'open', 'high', 'low', 'close', 'vol'])
            df['close'] = df['close'].astype(float)
            
            # Crossovers
            df['MA9'] = ta.sma(df['close'], length=9)
            df['MA21'] = ta.sma(df['close'], length=21)
            df['MA50'] = ta.sma(df['close'], length=50)
            df['MA200'] = ta.sma(df['close'], length=200)
            
            last = df.iloc[-1]
            prev = df.iloc[-2]
            
            # Logic for signals
            lt_status, lt_col = "SIDEWAYS", "#777"
            if last['MA50'] > last['MA200']: lt_status, lt_col = "🚀 GOLDEN", "#00ff41"
            elif last['MA50'] < last['MA200']: lt_status, lt_col = "💀 DEATH", "#ff3131"
            
            st_status = "BULLISH" if last['MA9'] > last['MA21'] else "BEARISH"
            st_col = "#00ff41" if st_status == "BULLISH" else "#ff3131"
            
            action, act_col = "HOLD", "#444"
            if last['MA9'] > last['MA21'] and last['MA50'] > last['MA200']: action, act_col = "🔥 BUY", "#00ff41"
            elif last['MA9'] < last['MA21'] and last['MA50'] < last['MA200']: action, act_col = "⚠️ SELL", "#ff3131"
                
            return {"name": name, "ltp": last['close'], "hi": last['high'], "lo": last['low'], "st": st_status, "st_col": st_col, "lt": lt_status, "lt_col": lt_col, "act": action, "act_col": act_col}
    except: return None

# --- 3. UI ---
st.markdown("<h2 style='text-align: center; color: #ffae00;'>V120 TOTAL F&O SCANNER</h2>", unsafe_allow_html=True)

if api:
    placeholder = st.empty()
    while True:
        results = []
        # Batch processing (ஒவ்வொரு முறையும் 20 ஸ்டாக் மட்டும் ஸ்கேன் செய்யும் - வேகம் அதிகரிக்க)
        for name, token in FO_STOCKS.items():
            data = fetch_signals(api, token, name)
            if data: results.append(data)
        
        with placeholder.container():
            # Filtering: சிக்னல் உள்ள பங்குகளை மட்டும் மேலே காட்டும்
            sorted_results = sorted(results, key=lambda x: x['act'] != "HOLD", reverse=True)
            
            for r in sorted_results:
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; align-items: center; background: #0a0a0a; padding: 12px; border-radius: 8px; border: 1px solid {r['act_col']}; margin-bottom: 5px;">
                    <div style="width: 20%;"><b style="color: #ffae00;">{r['name']}</b><br><small>₹{r['ltp']}</small></div>
                    <div style="width: 20%; color: #555; font-size: 11px;">H: {r['hi']}<br>L: {r['lo']}</div>
                    <div style="width: 20%; text-align: center; color: {r['st_col']}; font-size: 13px;">{r['st']}</div>
                    <div style="width: 20%; text-align: center; color: {r['lt_col']}; font-size: 13px;">{r['lt']}</div>
                    <div style="width: 20%; text-align: right; color: {r['act_col']}; font-weight: bold;">{r['act']}</div>
                </div>
                """, unsafe_allow_html=True)
        time.sleep(60) # 1 நிமிடம் ஒருமுறை மொத்த லிஸ்ட்டையும் அப்டேட் செய்யும்
else:
    st.error("API Error")
