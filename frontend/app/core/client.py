import httpx
import streamlit as st
from typing import Any
from datetime import datetime
import os

API_URL = os.getenv("API_URL", "http://backend:8000")


def get_client():
    headers = {}
    if "token" in st.session_state and st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"
    return httpx.Client(base_url=API_URL, headers=headers, timeout=10.0)


def login(username, password):
    res = get_client().post(
        "/auth/token", data={"username": username, "password": password}
    )
    res.raise_for_status()
    return res.json()


def register(username, password):
    res = get_client().post(
        "/auth/register", json={"username": username, "password": password}
    )
    res.raise_for_status()
    return res.json()


def list_transactions() -> list[dict[str, Any]]:
    try:
        res = get_client().get("/transactions")
        res.raise_for_status()
        return res.json()
    except Exception:
        return []


def create_transaction(amount: float, category: str, description: str):
    payload = {
        "amount": amount,
        "category": category,
        "description": description,
        "date": datetime.now().isoformat(),
    }
    res = get_client().post("/transactions", json=payload)
    res.raise_for_status()
    return res.json()


def delete_transaction(tx_id: int):
    res = get_client().delete(f"/transactions/{tx_id}")
    res.raise_for_status()


def get_ai_advice(query: str):
    res = get_client().get("/ai/advice", params={"query": query})
    res.raise_for_status()
    return res.json()


def trigger_report():
    res = get_client().post("/transactions/report")
    res.raise_for_status()
