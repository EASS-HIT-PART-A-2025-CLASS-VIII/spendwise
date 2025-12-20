import pandas as pd
import streamlit as st
from app.core.client import list_transactions


def get_transactions_df() -> pd.DataFrame:
    try:
        data = list_transactions()
        if not data:
            return pd.DataFrame(
                columns=["id", "amount", "category", "description", "date"]
            )
        df = pd.DataFrame(data)
        df["date"] = pd.to_datetime(df["date"])
        return df
    except Exception as e:
        st.error(f"❌ Failed to fetch transactions: {e}")
        return pd.DataFrame()


def render_sidebar_nav():
    st.sidebar.title("💰 SpendWise")
    if st.sidebar.button("Log Out"):
        st.session_state.token = None
        st.rerun()
    return st.sidebar.radio(
        "Navigation", ["Dashboard", "Transactions", "AI Advisor", "Reports"]
    )
