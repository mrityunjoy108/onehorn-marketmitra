import streamlit as st
import pandas as pd
import plotly.express as px
from data import get_budget_data, get_sector_performance

# --- Page Setup ---
st.set_page_config(page_title="Onehorn Community Policy Results Vs Market Returns", layout="wide")

# --- Header ---
st.title("📊 Onehorn MarketMitra")
st.caption("Connecting India's Union Budgets (Feb) to Sector-wise Market Performance Policy Results Vs Market Returns")

st.markdown("""
Explore how **Union Budget allocations** (presented every February)  
correlate with **stock market performance (Jan–Jun)**.  

This version compares **Budget 2023 (Feb)** vs **Budget 2024 (Feb)**  
and **NSE sector indices (Jan–Jun 2024)**.
""")

# --- Fetch Data ---
with st.spinner("⏳ Loading budget and market data..."):
    budget_df = get_budget_data()
    tickers = {
        "Infrastructure": "^CNXINFRA",
        "Energy": "^CNXENERGY",
        "Agriculture": "^CNXPHARMA",
        "FMCG": "^CNXFMCG",
        "IT": "^CNXIT",
        "Healthcare": "^CNXPHARMA",
        "Auto": "^CNXAUTO"
    }
    stock_df = get_sector_performance(tickers)

# --- Validate and Display Data ---
if budget_df.empty:
    st.error("❌ No budget data found!")
elif stock_df.empty:
    st.error("❌ No stock performance data found!")
else:
    # Merge datasets
    merged = pd.merge(budget_df, stock_df, on="Sector", how="left")
    merged["Change_%"] = pd.to_numeric(merged["Change_%"], errors="coerce")
    merged["Stock_Performance_%"] = pd.to_numeric(merged["Stock_Performance_%"], errors="coerce")

    # Sidebar filter
    st.sidebar.header("🔍 Filter Sectors")
    selected_sectors = st.sidebar.multiselect(
        "Select sectors to compare:",
        options=merged["Sector"].unique(),
        default=list(merged["Sector"].unique())
    )
    filtered = merged[merged["Sector"].isin(selected_sectors)]

    # --- Display Data Tables ---
    st.subheader("📘 Union Budget Comparison (₹ Lakh Crores) — Feb 2023 vs Feb 2024")
    st.dataframe(budget_df, use_container_width=True)

    st.subheader("💹 Sector-wise Market Performance (Jan–Jun 2024)")
    st.dataframe(stock_df, use_container_width=True)

    # --- Chart 1: Budget Change vs Stock Return ---
    st.subheader("📈 Budget Allocation Change (Feb 2023 → Feb 2024) vs Stock Return (Jan–Jun 2024)")

    plot_df = filtered.melt(
        id_vars=["Sector"],
        value_vars=["Change_%", "Stock_Performance_%"],
        var_name="Metric",
        value_name="Percentage"
    )

    fig1 = px.bar(
        plot_df,
        x="Sector",
        y="Percentage",
        color="Metric",
        barmode="group",
        text_auto=".2f",
        color_discrete_sequence=["#1f77b4", "#ff7f0e"],
        title="📊 Budget Allocation Change (Feb 2023 → Feb 2024) vs Sector Performance (Jan–Jun 2024)"
    )
    fig1.update_traces(textposition="outside")
    st.plotly_chart(fig1, use_container_width=True)

    # --- Chart 2: Stock Market Returns Only ---
    st.subheader("💹 Sector Stock Market Returns After Budget 2024 (Feb)")

    fig2 = px.bar(
        filtered,
        x="Sector",
        y="Stock_Performance_%",
        text_auto=".2f",
        color_discrete_sequence=["#00b894"],
        title="📈 Sector-wise Stock Market Returns (Jan–Jun 2024, Post Budget)"
    )
    fig2.update_traces(textposition="outside")
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
    **📘 Note:**  
    - Union Budget is presented every **February (Feb)**.  
    - This dashboard compares **Feb 2023 vs Feb 2024** allocations  
      and market reactions from **Jan–Jun 2024**.  
    """)

    # --- Explanation Box ---
    st.markdown("### 💡 Why does a small % change look big?")
    with st.expander("Click to understand how % growth works 👇"):
        st.markdown("""
        Take the **Auto sector** 👇  
        - In **Budget 2023 (Feb)**, it got **0.9%** of the total budget  
        - In **Budget 2024 (Feb)**, it got **1.1%**  
        - The increase is only **0.2%**, but...

        When compared **to the old value (0.9%)**,  
        it shows a **22.22% growth** — that’s how percentage math works!

        ---
        💬 *Tip:* Always check both — **actual allocation (₹)** and **% growth**  
        to see which sectors truly received the biggest push.
        """)

    # --- Footer ---
    st.markdown("""
    ---
    **📚 Data Sources:**  
    - [Union Budget Portal (Feb Budgets)](https://www.indiabudget.gov.in) *(Simulated data)*  
    - [Yahoo Finance (NSE Sector Indices)](https://finance.yahoo.com)  
    - Prototype by **Mrityunjoy Sarmah** *(MBA Finance, IMT Ghaziabad)*  
    """)

    st.success("✅ Dashboard loaded successfully!")
