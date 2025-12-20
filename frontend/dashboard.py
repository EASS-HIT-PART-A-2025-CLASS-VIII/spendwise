import streamlit as st
from app.views import overview, manage, exports
from app.core.client import login, register

PAGES = {
    "Overview": overview,
    "Manage Transactions": manage,
    "Exports": exports,
}


def main():
    st.set_page_config(
        page_title="💰 SpendWise Dashboard",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    if "token" not in st.session_state:
        st.session_state.token = None

    if not st.session_state.token:
        st.title("💰 SpendWise")
        tab1, tab2 = st.tabs(["Login", "Register"])
        with tab1:
            u = st.text_input("Username", key="login_u")
            p = st.text_input("Password", type="password", key="login_p")
            if st.button("Sign In"):
                try:
                    data = login(u, p)
                    st.session_state.token = data["access_token"]
                    st.rerun()
                except Exception:
                    st.error("Invalid credentials")
        with tab2:
            ru = st.text_input("Username", key="reg_u")
            rp = st.text_input("Password", type="password", key="reg_p")
            if st.button("Create Account"):
                register(ru, rp)
                st.success("User created! Please login.")
        return

    st.sidebar.markdown("### 💰 SpendWise")
    if st.sidebar.button("Logout"):
        st.session_state.token = None
        st.rerun()

    selection = st.sidebar.radio(
        "Navigation",
        list(PAGES.keys()),
    )

    PAGES[selection].main()


if __name__ == "__main__":
    main()
