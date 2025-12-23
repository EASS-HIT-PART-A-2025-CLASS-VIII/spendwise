import streamlit as st
import time
from ..core.client import create_transaction, delete_transaction
from ..core.shared import get_transactions_df, load_css


def main():
    load_css()
    _, center_col, _ = st.columns([1, 6, 1])

    with center_col:
        st.title("Transaction Management")
        tab1, tab2 = st.tabs(["Add Entry", "Delete Record"])

        with tab1:
            st.write("")

            # 3 Identical Text Inputs
            amount_str = st.text_input("Amount", value="20.0", placeholder="0.00")
            category = st.text_input("Category", placeholder="e.g. Food, Rent, Tech")
            description = st.text_input("Description", placeholder="What was this for?")

            st.write("")

            if st.button("Save Transaction", use_container_width=True, type="primary"):
                # Basic validation
                try:
                    amount_val = float(amount_str)
                    if not category:
                        st.error("Please enter a category.")
                    else:
                        create_transaction(amount_val, category, description)
                        st.toast(f"✅ Saved ${amount_val:.2f} to {category}")
                        time.sleep(1.2)
                        st.rerun()
                except ValueError:
                    st.error("Please enter a valid number for the amount.")

        with tab2:
            st.write("")
            df = get_transactions_df()
            if not df.empty:
                # Custom selection box for deletion
                records = {
                    f"{r.category} - ${r.amount} ({r.description})": r.id
                    for r in df.itertuples()
                }
                target = st.selectbox("Select record to remove", list(records.keys()))

                if st.button(
                    "Delete Permanently", type="primary", use_container_width=True
                ):
                    delete_transaction(records[target])
                    st.toast("🗑️ Record removed.")
                    time.sleep(1.2)
                    st.rerun()
            else:
                st.info("No records to delete.")
