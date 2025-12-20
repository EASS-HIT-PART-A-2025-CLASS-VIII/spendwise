import streamlit as st
import plotly.express as px
from app.core.shared import get_transactions_df


def main():
    st.title("📊 Financial Overview")
    df = get_transactions_df()

    if df.empty:
        st.info("No transactions yet. Add some in the Transactions tab!")
        return

    # Metrics
    total_spent = df["amount"].sum()
    avg_tx = df["amount"].mean()
    top_cat = df.groupby("category")["amount"].sum().idxmax()

    m1, m2, m3 = st.columns(3)
    m1.metric("Total Spent", f"${total_spent:,.2f}")
    m2.metric("Avg. Transaction", f"${avg_tx:,.2f}")
    m3.metric("Top Category", top_cat)

    # Charts
    c1, c2 = st.columns(2)
    with c1:
        fig_pie = px.pie(
            df, values="amount", names="category", title="Spending by Category"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    with c2:
        df_daily = df.set_index("date").resample("D")["amount"].sum().reset_index()
        fig_line = px.line(df_daily, x="date", y="amount", title="Daily Spending Trend")
        st.plotly_chart(fig_line, use_container_width=True)
