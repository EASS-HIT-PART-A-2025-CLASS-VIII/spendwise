import streamlit as st
from ..core.client import trigger_report
from ..core.shared import load_css


def main():
    load_css()
    _, center_col, _ = st.columns([1, 2, 1])

    with center_col:
        st.markdown(
            """
            <div class="report-card">
                <h1 style="color: white; text-align: center;">📑 Financial Reports</h1>
                <p style="color: #8b949e; text-align: center;">Click below to trigger a background process that generates a complete PDF summary of your finances.</p>
            </div>
        """,
            unsafe_allow_html=True,
        )

        st.write("")
        if st.button(
            "🚀 Generate PDF Report", use_container_width=True, type="primary"
        ):
            try:
                trigger_report()
                st.balloons()
                st.success(
                    "Request sent! The worker (Redis + ARQ) is generating your file. It will be available in the data logs in 5 seconds."
                )
            except Exception:
                st.error("The reporting service is currently offline.")
