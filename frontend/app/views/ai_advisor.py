import streamlit as st
from ..core.client import get_ai_advice
from ..core.shared import load_css


def main():
    load_css()
    _, center, _ = st.columns([1, 5, 1])

    with center:
        st.title("AI Advisor")
        query = st.text_area(
            "Question", placeholder="E.g., How can I reduce my tech spending?"
        )

        if st.button("Generate Insight", use_container_width=True, type="primary"):
            if query:
                with st.spinner("Analyzing your habits..."):
                    try:
                        res = get_ai_advice(query)
                        st.markdown(
                            f"""
                            <div style="background-color: #1c2128; border-left: 5px solid #4CAF50; padding: 30px; border-radius: 0 12px 12px 0; margin-top: 30px;">
                                <span style="color: #8b949e; text-transform: uppercase; letter-spacing: 1.5px; font-size: 0.8rem;">Intelligence Output</span>
                                <p style="font-size: 1.15rem; line-height: 1.7; color: #f0f6fc; margin-top: 10px;">{res["advice"]}</p>
                            </div>
                        """,
                            unsafe_allow_html=True,
                        )
                    except Exception:
                        st.error("AI service temporarily unavailable.")
