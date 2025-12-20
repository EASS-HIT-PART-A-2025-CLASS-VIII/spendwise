import streamlit as st
from app.core.client import create_transaction, delete_transaction
from app.core.shared import get_transactions_df


def main():
    st.title("💸 Manage Transactions")
    add_tab, del_tab = st.tabs(["➕ Add Expense", "🗑️ Delete"])

    with add_tab:
        with st.form("tx_form", clear_on_submit=True):
            amount = st.number_input("Amount", min_value=0.01)
            category = st.selectbox(
                "Category", ["Food", "Transport", "Rent", "Tech", "Other"]
            )
            desc = st.text_input("Description")
            if st.form_submit_button("Add Transaction"):
                create_transaction(amount, category, desc)
                st.success("Transaction added!")
                st.rerun()

    with del_tab:
        df = get_transactions_df()
        if not df.empty:
            # Dropdown with ID and Description for deletion
            options = {
                f"{row.id}: {row.description} (${row.amount})": row.id
                for row in df.itertuples()
            }
            to_delete = st.selectbox("Select to remove", list(options.keys()))
            if st.button("Confirm Delete"):
                delete_transaction(options[to_delete])
                st.rerun()
