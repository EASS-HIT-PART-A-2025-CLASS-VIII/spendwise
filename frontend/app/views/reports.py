import streamlit as st
import os
import time
from ..core.client import trigger_report
from ..core.shared import load_css


def main():
    load_css()
    _, center, _ = st.columns([1, 4, 1])

    with center:
        st.title("Statement Hub")
        st.write("Trigger the background worker to compile your history into a PDF.")

        if st.button(
            "🚀 Generate New Statement", use_container_width=True, type="primary"
        ):
            try:
                trigger_report()
                st.toast("Request sent to background worker...")
                time.sleep(2)
                st.rerun()
            except Exception:
                st.error("Reporting service offline.")

        st.divider()
        st.subheader("Your PDF Reports")

        # Reports live in the shared volume folder
        data_path = "/app/app/data"
        if os.path.exists(data_path):
            pdfs = [f for f in os.listdir(data_path) if f.endswith(".pdf")]
            if pdfs:
                for pdf in pdfs:
                    file_path = os.path.join(data_path, pdf)
                    with open(file_path, "rb") as f:
                        st.download_button(
                            label=f"📂 Download {pdf}",
                            data=f,
                            file_name=pdf,
                            mime="application/pdf",
                            use_container_width=True,
                        )
            else:
                st.write("No reports found. Click generate above.")
