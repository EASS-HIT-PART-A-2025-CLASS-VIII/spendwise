import pandas as pd
import streamlit as st
from .client import list_transactions


def load_css():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #0e1117;
            color: #fafafa;
        }
        [data-testid="stHeader"] {
            background-color: rgba(0,0,0,0);
        }
        [data-testid="stSidebar"] {
            background-color: #161b22;
            border-right: 1px solid #30363d;
        }
        div[data-testid="stMetric"] {
            background-color: #1c2128;
            border: 1px solid #30363d;
            padding: 15px;
            border-radius: 10px;
        }
        [data-testid="stForm"] {
            background-color: #1c2128;
            border: 1px solid #30363d;
            border-radius: 15px;
            padding: 30px;
        }
        .report-card {
            background-color: #1c2128;
            border: 1px solid #30363d;
            padding: 40px;
            border-radius: 20px;
            text-align: center;
        }
        h1, h2, h3 {
            text-align: center;
            color: #4CAF50;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 24px;
            justify-content: center;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )


def get_transactions_df() -> pd.DataFrame:
    data = list_transactions()
    if not data:
        return pd.DataFrame(columns=["id", "amount", "category", "description", "date"])
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    return df


def render_sidebar_nav():
    st.sidebar.markdown(
        "<h1 style='font-size: 80px; margin: 0;'>💰</h1>", unsafe_allow_html=True
    )
    st.sidebar.markdown(
        "<h2 style='text-align: center; margin-top: 0; color: white;'>SpendWise</h2>",
        unsafe_allow_html=True,
    )
    st.sidebar.divider()

    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.token = None
        st.rerun()

    st.sidebar.write("")
    return st.sidebar.radio(
        "Navigation", ["Dashboard", "Manage", "AI Advisor", "Reports"]
    )
