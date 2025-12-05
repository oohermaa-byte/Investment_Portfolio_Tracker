import streamlit as st
import pandas as pd
import yfinance as yf

# ================================
# FUNCTION: Fetch Current Stock Price
# ================================
def fetch_price(ticker):
    try:
        data = yf.download(ticker, period="1d", progress=False)
        price = float(data["Close"].iloc[-1])
        return price
    except:
        return 0.0   # return 0 jika gagal fetch

# ================================
# STREAMLIT APP
# ================================
st.title("📊 Investment Portfolio Tracker")

st.write("Upload file portofolio Anda (CSV dengan kolom: Ticker, Buy Price, Quantity).")
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:
    # Read portfolio
    portfolio = pd.read_csv(uploaded_file)

    st.subheader("📄 Data Portofolio Awal")
    st.dataframe(portfolio)

    # Extract ticker list
    tickers = portfolio["Ticker"].tolist()

    # Fetch current prices
    st.subheader("📈 Fetching Current Prices...")
    current_prices = {}

    for t in tickers:
        price = fetch_price(t)
        current_prices[t] = price

    portfolio["Current Price"] = portfolio["Ticker"].apply(lambda t: current_prices[t])

    # Calculate investment values
    portfolio["Investment"] = portfolio["Buy Price"] * portfolio["Quantity"]
    portfolio["Current Value"] = portfolio["Current Price"] * portfolio["Quantity"]

    st.subheader("📊 Portfolio Dengan Harga Saat Ini")
    st.dataframe(portfolio)

    # ================================
    # SUMMARY SECTION
    # ================================
    total_investment = float(portfolio["Investment"].sum())
    total_value = float(portfolio["Current Value"].sum())
    profit_loss = total_value - total_investment

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Investment", f"${total_investment:,.2f}")
    col2.metric("Portfolio Value", f"${total_value:,.2f}")
    col3.metric("Profit / Loss", f"${profit_loss:,.2f}", delta=f"{profit_loss:,.2f}")

    # ================================
    # PLOT
    # ================================
    st.subheader("📉 Comparison Chart")
    chart_df = portfolio[["Ticker", "Investment", "Current Value"]]
    chart_df = chart_df.set_index("Ticker")

    st.bar_chart(chart_df)
