import streamlit as st
from ..core.client import get_ai_advice
from ..core.shared import load_css


def main():
    load_css()
    _, center_col, _ = st.columns([1, 3, 1])

    with center_col:
        st.title("🤖 AI Financial Advisor")
        st.write(
            "Ask questions about your spending habits and get personalized advice."
        )

        query = st.text_area(
            "What would you like to know?",
            placeholder="Am I spending too much on Food?",
        )

        if st.button("Ask Advisor", use_container_width=True, type="primary"):
            with st.spinner("Analyzing your transactions..."):
                try:
                    res = get_ai_advice(query)
                    st.markdown("### Advice:")
                    st.info(res["advice"])
                except Exception:
                    st.error("AI service is currently unavailable.")
