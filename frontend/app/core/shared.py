import pandas as pd
import streamlit as st
from .client import list_transactions


def load_css():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #0d1117 !important;
            color: #c9d1d9 !important;
        }
        /* Make all text inputs look identical and clean */
        div[data-testid="stTextInput"] input {
            background-color: #161b22 !important;
            color: #f0f6fc !important;
            border: 1px solid #30363d !important;
            border-radius: 8px !important;
            height: 45px !important;
            padding: 10px !important;
        }
        /* Remove focus border glow for a cleaner look */
        div[data-testid="stTextInput"] input:focus {
            border-color: #58a6ff !important;
            box-shadow: none !important;
        }
        /* Neutral headers */
        h1, h2, h3 {
            color: #f0f6fc !important;
            text-align: center !important;
            font-weight: 500 !important;
        }
        /* Center content */
        .block-container {
            max-width: 800px !important;
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
        "<div style='text-align: center; padding-bottom: 20px;'><span style='font-size: 50px;'>💰</span><br><b style='font-size: 20px; color: #f0f6fc;'>SpendWise</b></div>",
        unsafe_allow_html=True,
    )
    st.sidebar.divider()
    options = ["Dashboard", "Manage", "AI Advisor", "Reports"]
    selection = st.sidebar.radio(
        "Navigation", options, label_visibility="collapsed", key="nav_radio"
    )
    st.sidebar.write("")
    if st.sidebar.button("🚪 Log Out", use_container_width=True):
        st.session_state.token = None
        st.rerun()
    return selection
