# frontend/app/main.py (Refactored)
import streamlit as st
from app.core.client import login
from app.core.shared import render_sidebar_nav
from app.views import overview, manage


def main():
    if "token" not in st.session_state:
        st.session_state.token = None

    if not st.session_state.token:
        st.title("💰 SpendWise Login")
        tab1, tab2 = st.tabs(["Login", "Register"])

        with tab1:
            u = st.text_input("Username", key="l_u")
            p = st.text_input("Password", type="password", key="l_p")
            if st.button("Sign In"):
                data = login(u, p)
                st.session_state.token = data["access_token"]
                st.rerun()
        return

    page = render_sidebar_nav()
    if page == "Dashboard":
        overview.main()
    elif page == "Transactions":
        manage.main()


if __name__ == "__main__":
    main()
