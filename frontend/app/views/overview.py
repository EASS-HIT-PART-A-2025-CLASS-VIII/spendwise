import streamlit as st
import plotly.express as px
from ..core.shared import get_transactions_df, load_css


def main():
    load_css()
    df = get_transactions_df()

    st.title("Financial Overview")

    if df.empty:
        st.info("No data recorded yet. Go to the Manage tab to add your first expense.")
        return

    # Wide Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Spending", f"${df['amount'].sum():,.2f}")
    m2.metric("Average Entry", f"${df['amount'].mean():,.2f}")
    m3.metric("Top Category", df.groupby("category")["amount"].sum().idxmax())
    m4.metric("Entries", len(df))

    st.write("")

    # Side-by-Side: Graph and Table
    col_chart, col_table = st.columns([1, 1.2])

    with col_chart:
        fig = px.pie(
            df,
            values="amount",
            names="category",
            hole=0.5,
            template="plotly_dark",
            title="Spending Mix",
        )
        fig.update_layout(margin=dict(t=50, b=0, l=0, r=0), showlegend=True)
        st.plotly_chart(fig, use_container_width=True)

    with col_table:
        st.subheader("Recent Activity")
        # Clean history table
        st.dataframe(
            df.sort_values("date", ascending=False),
            use_container_width=True,
            hide_index=True,
            column_config={
                "amount": st.column_config.NumberColumn("Amount", format="$%.2f"),
                "date": st.column_config.DatetimeColumn("Date", format="D MMM, HH:mm"),
                "category": "Category",
                "description": "Details",
            },
        )
