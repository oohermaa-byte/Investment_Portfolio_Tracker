import streamlit as st
import pandas as pd
import yfinance as yf

st.title("📊 Investment Portfolio Tracker")

st.write("Upload file portofolio Anda (CSV atau Excel dengan kolom: Ticker, Buy Price, Quantity).")

# ⬇ File uploader — now accepts CSV & EXCEL
uploaded_file = st.file_uploader(
    "Upload file",
    type=["csv", "xlsx"]
)

# Process uploaded file
if uploaded_file is not None:

    # Read CSV or Excel
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("📄 Data Portofolio")
    st.dataframe(df)

    # Fetch latest stock prices
    st.subheader("💹 Mengambil Harga Saham Terkini...")

    df["Current Price"] = 0.0

    tickers = df["Ticker"].tolist()

    for i, ticker in enumerate(tickers):
        try:
            stock = yf.Ticker(ticker)
            price = stock.history(period="1d")["Close"].iloc[-1]
            df.loc[i, "Current Price"] = price
        except:
            df.loc[i, "Current Price"] = 0

    # Calculate values
    df["Investment"] = df["Buy Price"] * df["Quantity"]
    df["Current Value"] = df["Current Price"] * df["Quantity"]
    df["Profit/Loss"] = df["Current Value"] - df["Investment"]

    st.subheader("📈 Hasil Perhitungan")
    st.dataframe(df)

    # Summary
    total_investment = df["Investment"].sum()
    total_value = df["Current Value"].sum()
    total_profit = df["Profit/Loss"].sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Investment", f"${total_investment:,.2f}")
    col2.metric("Portfolio Value", f"${total_value:,.2f}")
    col3.metric("Profit / Loss", f"${total_profit:,.2f}")

    # Bar chart
    st.subheader("📊 Portfolio Value Chart")
    st.bar_chart(df.set_index("Ticker")["Current Value"])
