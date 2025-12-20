import streamlit as st
import plotly.express as px
from ..core.shared import get_transactions_df, load_css


def main():
    load_css()
    df = get_transactions_df()

    _, center_col, _ = st.columns([1, 4, 1])

    with center_col:
        st.title("📊 Financial Insights")

        if df.empty:
            st.info("No transactions found. Go to 'Manage' to add your first expense.")
            return

        m1, m2, m3 = st.columns(3)
        m1.metric("Total Spent", f"${df['amount'].sum():,.2f}")
        m2.metric("Monthly Avg", f"${df['amount'].mean():,.2f}")
        m3.metric("Record Count", len(df))

        st.write("")

        c1, c2 = st.columns(2)
        with c1:
            fig_pie = px.pie(
                df,
                values="amount",
                names="category",
                hole=0.5,
                template="plotly_dark",
                title="Spending Mix",
            )
            fig_pie.update_layout(margin=dict(t=40, b=0, l=0, r=0))
            st.plotly_chart(fig_pie, use_container_width=True)
        with c2:
            cat_df = df.groupby("category")["amount"].sum().reset_index()
            fig_bar = px.bar(
                cat_df,
                x="category",
                y="amount",
                color="category",
                template="plotly_dark",
                title="Category Totals",
            )
            fig_bar.update_layout(showlegend=False, margin=dict(t=40, b=0, l=0, r=0))
            st.plotly_chart(fig_bar, use_container_width=True)

        st.subheader("Latest Transactions")
        st.dataframe(
            df.sort_values("date", ascending=False),
            use_container_width=True,
            hide_index=True,
        )
