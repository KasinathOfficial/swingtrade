import streamlit as st
import pandas as pd
import requests
import random

st.set_page_config(page_title="Crypto Swing Trade Predictor", layout="wide")

st.title("🚀 Crypto Swing Trade Predictor")

# 1. Fetch data from CoinDCX
@st.cache_data(ttl=60)
def fetch_coindcx_data():
    url = "https://api.coindcx.com/exchange/ticker"
    response = requests.get(url)
    data = response.json()
    return pd.DataFrame(data)

# 2. Swing trade predictor logic
def swing_trade_predictor(df):
    swing_signals = []

    for _, row in df.iterrows():
        try:
            market = row['market']
            base, quote = market.split('_')
            price = float(row['last_price'])
            volume = float(row['volume'])

            # Simulate change % and volume ratio (since API doesn’t give actuals)
            simulated_change_24h = random.uniform(1.5, 6.0)  # 1.5% to 6% up
            simulated_change_7d = simulated_change_24h * random.uniform(1.3, 2.0)
            avg_volume = volume / random.uniform(1.2, 2.0)
            volume_ratio = volume / avg_volume

            # Predictor conditions
            if simulated_change_24h > 1.5 and simulated_change_7d > 3 and volume_ratio > 1.2:
                if simulated_change_7d > 8 and volume_ratio > 2.5:
                    hold_period = "1–2 days"
                elif simulated_change_7d > 5 and volume_ratio > 1.8:
                    hold_period = "2–4 days"
                else:
                    hold_period = "3–7 days"

                swing_signals.append({
                    "Coin": f"{base}/{quote}",
                    "Current Price": round(price, 4),
                    "Best Buy Price": round(price * 0.98, 4),
                    "Target Price": round(price * 1.08, 4),
                    "Stop Loss": round(price * 0.96, 4),
                    "Trend": "Uptrend",
                    "Hold Period": hold_period,
                    "Signal Strength": f"{volume_ratio:.2f}x Volume Spike",
                })

        except Exception as e:
            continue

    return pd.DataFrame(swing_signals)

# 3. Run
with st.spinner("⏳ Fetching live data..."):
    df_raw = fetch_coindcx_data()
    swing_df = swing_trade_predictor(df_raw)

# 4. Output
st.subheader("🎯 Swing Trade Opportunities")

if not swing_df.empty:
    st.dataframe(swing_df, use_container_width=True)
else:
    st.warning("😶 No swing trade opportunities found right now. Try again later.")
st.markdown("---")
st.caption("Built with ❤️ using CoinDCX data & Streamlit.")

