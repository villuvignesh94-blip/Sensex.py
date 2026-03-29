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
