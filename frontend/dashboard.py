import streamlit as st
from app.views import overview, manage, reports, ai_advisor
from app.core.client import login, register
from app.core.shared import load_css

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
        _, center_col, _ = st.columns([1, 2, 1])
        with center_col:
            st.markdown("<h1 style='font-size: 60px;'>💰</h1>", unsafe_allow_html=True)
            st.title("SpendWise")

            tab1, tab2 = st.tabs(["Login", "Register"])

            with tab1:
                with st.form("login_form"):
                    u = st.text_input("Username")
                    p = st.text_input("Password", type="password")
                    if st.form_submit_button("Sign In", use_container_width=True):
                        try:
                            data = login(u, p)
                            st.session_state.token = data["access_token"]
                            st.rerun()
                        except Exception:
                            st.error("Invalid credentials")

            with tab2:
                with st.form("reg_form"):
                    ru = st.text_input("New Username")
                    rp = st.text_input("New Password", type="password")
                    if st.form_submit_button(
                        "Create Account", use_container_width=True
                    ):
                        try:
                            register(ru, rp)
                            st.success("Account created! You can now log in.")
                        except Exception:
                            st.error("Registration failed.")
        return

    from app.core.shared import render_sidebar_nav

    selection = render_sidebar_nav()
    PAGES[selection].main()


if __name__ == "__main__":
    main()
