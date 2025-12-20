import streamlit as st
from ..core.client import create_transaction, delete_transaction
from ..core.shared import get_transactions_df, load_css


def main():
    load_css()
    _, center_col, _ = st.columns([1, 2, 1])

    with center_col:
        st.title("💸 Manage Finances")
        t1, t2 = st.tabs(["➕ Add Entry", "🗑️ Remove Entry"])

        with t1:
            with st.form("entry_form", clear_on_submit=True):
                amount = st.number_input("Amount ($)", min_value=0.01, step=0.5)

                cat_col1, cat_col2 = st.columns(2)
                with cat_col1:
                    choice = st.selectbox(
                        "Category", ["Food", "Rent", "Transport", "Tech", "Other"]
                    )
                with cat_col2:
                    custom = st.text_input("Or Custom Name")

                desc = st.text_input("Description (optional)")

                final_cat = custom if custom else choice

                if st.form_submit_button("Save Transaction", use_container_width=True):
                    create_transaction(amount, final_cat, desc)
                    st.success(f"Added ${amount} to {final_cat}")
                    st.rerun()

        with t2:
            df = get_transactions_df()
            if not df.empty:
                mapping = {
                    f"{r.category}: {r.description} (${r.amount})": r.id
                    for r in df.itertuples()
                }
                target = st.selectbox("Select to delete", list(mapping.keys()))
                if st.button(
                    "Delete Permanently", type="primary", use_container_width=True
                ):
                    delete_transaction(mapping[target])
                    st.rerun()
            else:
                st.write("No transactions to delete.")
