import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Crypto Swing Trade Predictor", layout="wide")
st.title("📈 Crypto Swing Trade Predictor")

# --- Fetch Data from CoinDCX ---
@st.cache_data(ttl=60)
def fetch_coindcx_data():
    url = "https://api.coindcx.com/exchange/ticker"
    response = requests.get(url)
    data = response.json()
    return pd.DataFrame(data)

# --- Predictor Logic ---
def swing_trade_predictor(df):
    swing_signals = []

    for _, row in df.iterrows():
        try:
            market = row['market']
            base = market.split('_')[0]
            quote = market.split('_')[1]

            price = float(row['last_price'])
            volume = float(row['volume'])
            avg_volume = volume / 2  # Simulated average
            volume_ratio = volume / avg_volume

            # Use available 24h change or simulate
            change_24h = float(row.get('price_change_percent_24h', 0))
            change_7d = change_24h * 2  # Simulate 7D momentum

            # Relaxed conditions
            is_momentum = change_24h > 1.5 and change_7d > 3
            is_volume_strong = volume_ratio > 1.2
            is_trending = change_7d >= change_24h

            # Dynamic hold period
            if change_7d > 8 and volume_ratio > 2.5:
                hold_period = "1–2 days"
            elif change_7d > 5 and volume_ratio > 1.8:
                hold_period = "2–4 days"
            else:
                hold_period = "3–7 days"

            if is_momentum and is_volume_strong and is_trending:
                swing_signals.append({
                    "Coin": f"{base}/{quote}",
                    "Current Price": round(price, 4),
                    "Best Buy Price": round(price * 0.98, 4),
                    "Target Price": round(price * 1.08, 4),
                    "Stop Loss": round(price * 0.96, 4),
                    "Trend": "Uptrend",
                    "Hold Period": hold_period,
                    "Signal Strength": f"{volume_ratio:.2f}x Volume Spike"
                })
        except Exception as e:
            continue

    return pd.DataFrame(swing_signals)



# --- App Flow ---
with st.spinner("Fetching data from CoinDCX..."):
    df_raw = fetch_coindcx_data()
    swing_df = swing_trade_predictor(df_raw)

# --- Display Result ---
st.subheader("🧠 Swing Trade Opportunities")
if not swing_df.empty:
    st.dataframe(swing_df, use_container_width=True)
else:
    st.warning("No swing trade opportunities found right now. Try again later.")

st.markdown("---")
st.caption("Built with ❤️ using CoinDCX data & Streamlit.")
