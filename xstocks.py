import requests
import streamlit as st

BASE = "https://api.xstocks.fi"

@st.cache_data(ttl=30, show_spinner=False)
def get_xstock_price(symbol: str) -> dict:
    if not symbol or symbol.startswith("Not "):
        return {"price": None, "currency": "USD", "status": "No tokenized representation configured"}
    url = f"{BASE}/public/assets/{symbol}/price-data"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        price = data.get("price") or data.get("data", {}).get("price")
        return {"price": float(price) if price is not None else None, "currency": "USD", "status": "Live xStocks public price"}
    except Exception as exc:
        return {"price": None, "currency": "USD", "status": f"xStocks price unavailable: {exc}"}


def prepare_investment(symbol: str, quantity: float, wallet: str = "") -> dict:
    quote = get_xstock_price(symbol)
    if quote.get("price") is None:
        raise RuntimeError("A live token price is unavailable, so an order cannot be prepared safely.")
    return {
        "token": symbol,
        "quantity": quantity,
        "estimated_price": quote["price"],
        "estimated_notional": quote["price"] * quantity,
        "network": "Solana",
        "wallet": wallet or "Wallet not connected",
        "status": "Order prepared — user signature/execution required",
    }
