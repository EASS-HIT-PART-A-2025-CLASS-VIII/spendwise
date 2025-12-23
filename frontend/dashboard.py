import streamlit as st
from app.views import overview, manage, reports, ai_advisor
from app.core.client import login, register
from app.core.shared import load_css, render_sidebar_nav

PAGES = {
    "Dashboard": overview,
    "Manage": manage,
    "AI Advisor": ai_advisor,
    "Reports": reports,
}


def main():
    st.set_page_config(page_title="SpendWise", layout="wide", page_icon="💰")
    load_css()

    if "token" not in st.session_state:
        st.session_state.token = None

    if not st.session_state.token:
        _, col, _ = st.columns([1, 2, 1])
        with col:
            st.markdown(
                "<h1 style='text-align: center !important;'>💰 SpendWise</h1>",
                unsafe_allow_html=True,
            )
            tabs = st.tabs(["Login", "Register"])

            with tabs[0]:
                if st.button("Sign In", use_container_width=True, type="primary"):
                    try:
                        data = login(
                            st.session_state.login_user, st.session_state.login_pass
                        )
                        st.session_state.token = data["access_token"]
                        st.rerun()
                    except Exception:
                        st.error("Incorrect credentials")

            with tabs[1]:
                if st.button("Create Account", use_container_width=True):
                    try:
                        register(st.session_state.reg_user, st.session_state.reg_pass)
                        st.success("User created. Now Sign In.")
                    except Exception:
                        st.error("Signup failed")
        return

    # Main App Logic
    selection = render_sidebar_nav()
    page = PAGES.get(selection, overview)
    page.main()


if __name__ == "__main__":
    main()
