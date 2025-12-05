import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Investment Portfolio Tracker")

uploaded_file = st.file_uploader("Upload Portfolio Excel/CSV", type=["csv", "xlsx"])

if uploaded_file is not None:

    file_name = uploaded_file.name.lower()

    try:
        # Deteksi file
        if file_name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
        elif file_name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            st.error("Format file tidak didukung.")
            st.stop()

        st.success("File berhasil dibaca!")

        st.subheader("Data Portfolio")
        st.write(df)

        # ---------- BAR CHART NILAI INVESTASI ----------
        if "Asset" in df.columns and "Current Value" in df.columns:
            fig_value = px.bar(
                df,
                x="Asset",
                y="Current Value",
                title="Current Value per Asset",
                text="Current Value"
            )
            st.plotly_chart(fig_value)
        else:
            st.warning("Kolom 'Asset' dan 'Current Value' tidak ditemukan.")

        # ---------- PIE CHART ALOKASI ----------
        if "Asset" in df.columns and "Allocation" in df.columns:
            fig_alloc = px.pie(
                df,
                names="Asset",
                values="Allocation",
                title="Portfolio Allocation (%)"
            )
            st.plotly_chart(fig_alloc)
        else:
            st.warning("Kolom 'Asset' dan 'Allocation' tidak ditemukan.")

    except Exception as e:
        st.error(f"Terjadi error saat membaca file: {e}")
