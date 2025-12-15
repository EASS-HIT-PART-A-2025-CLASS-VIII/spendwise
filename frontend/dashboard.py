import streamlit as st
from app.views import overview, manage, exports


PAGES = {
    "Overview": overview,
    "Manage Movies": manage,
    "Exports": exports,
}


def main():
    st.set_page_config(
        page_title="🎬 FastAPI Movie Dashboard",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.sidebar.markdown("### 🎬 FastAPI Movies")

    selection = st.sidebar.radio(
        "Navigation",
        list(PAGES.keys()),
        index=list(PAGES.keys()).index(st.session_state.get("page", "Overview")),
    )

    PAGES[selection].main()


if __name__ == "__main__":
    main()
