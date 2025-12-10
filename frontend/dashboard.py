# Add project root to sys.path so `import app` works with Streamlit
import sys
from pathlib import Path

current = Path(__file__).resolve()
app_dir = current.parent
frontend_dir = app_dir.parent

if str(frontend_dir) not in sys.path:
    sys.path.insert(0, str(frontend_dir))
if str(app_dir) not in sys.path:
    sys.path.insert(0, str(app_dir))

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
        index=list(PAGES.keys()).index(st.session_state.get("page", "Overview"))
    )

    st.session_state["page"] = selection

    PAGES[selection].main()


if __name__ == "__main__":
    main()
