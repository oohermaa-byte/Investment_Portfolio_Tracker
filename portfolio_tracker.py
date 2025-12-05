import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

st.set_page_config(page_title="Investment Portfolio Tracker", layout="wide")
st.title("📊 Investment Portfolio Tracker")

# --- Input Section ---
st.sidebar.header("Tambah Data Portofolio")

tickers = st.sidebar.text_input("Ticker saham/krypto (pisahkan koma)", "AAPL, MSFT, TSLA")
buy_prices = st.sidebar.text_input("Harga beli (pisahkan koma)", "150, 300, 250")
quantities = st.sidebar.text_input("Jumlah (pisahkan koma)", "10, 5, 8")

# --- Load Data ---
try:
    ticker_list = [t.strip().upper() for t in tickers.split(",")]
    buy_price_list = [float(x) for x in buy_prices.split(",")]
    quantity_list = [float(x) for x in quantities.split(",")]
except:
    st.error("Format input tidak valid.")
    st.stop()

if len(ticker_list) != len(buy_price_list) or len(ticker_list) != len(quantity_list):
    st.error("Jumlah ticker, harga beli, dan quantity harus sama.")
    st.stop()

# --- Fetch Prices ---
def fetch_price(ticker):
    try:
        data = yf.download(ticker, period="1d")["Close"].iloc[-1]
        return data
    except:
        return None

prices = {ticker: fetch_price(ticker) for ticker in ticker_list}

# --- Build Portfolio DataFrame ---
portfolio = pd.DataFrame({
    "Ticker": ticker_list,
    "Buy Price": buy_price_list,
    "Quantity": quantity_list,
    "Current Price": [prices[t] for t in ticker_list]
})

portfolio["Investment"] = portfolio["Buy Price"] * portfolio["Quantity"]
portfolio["Current Value"] = portfolio["Current Price"] * portfolio["Quantity"]
portfolio["Unrealized P/L"] = portfolio["Current Value"] - portfolio["Investment"]
portfolio["Return %"] = (portfolio["Unrealized P/L"] / portfolio["Investment"]) * 100

st.subheader("📈 Portfolio Overview")
st.dataframe(portfolio, use_container_width=True)

# --- KPIs ---
total_investment = portfolio["Investment"].sum()
total_value = portfolio["Current Value"].sum()
total_pl = portfolio["Unrealized P/L"].sum()
total_return_pct = (total_pl / total_investment) * 100

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Investment", f"${total_investment:,.2f}")
col2.metric("Portfolio Value", f"${total_value:,.2f}")
col3.metric("Unrealized P/L", f"${total_pl:,.2f}")
col4.metric("Return %", f"{total_return_pct:.2f}%")

# --- Pie Chart Allocation ---
st.subheader("📌 Portfolio Allocation")
fig1, ax1 = plt.subplots()
ax1.pie(portfolio["Current Value"], labels=portfolio["Ticker"], autopct="%1.1f%%")
st.pyplot(fig1)

# --- Price History Chart ---
st.subheader("📉 Price History")
hist_ticker = st.selectbox("Pilih ticker untuk melihat history", ticker_list)

hist_data = yf.download(hist_ticker, period="6mo")["Close"]

fig2, ax2 = plt.subplots()
ax2.plot(hist_data, label=hist_ticker)
ax2.set_title(f"{hist_ticker} - 6 Month Price History")
ax2.set_xlabel("Tanggal")
ax2.set_ylabel("Harga")
ax2.legend()
st.pyplot(fig2)

st.success("Aplikasi Portfolio Tracker berhasil dijalankan!")
