import yfinance as yf
import pandas as pd
import streamlit as st

@st.cache_data(ttl=60, show_spinner=False)
def get_market_snapshot(symbol: str) -> dict:
    ticker = yf.Ticker(symbol)
    info = {}
    try:
        info = ticker.fast_info
    except Exception:
        info = {}

    history = ticker.history(period="5d", interval="1d", auto_adjust=False)
    if history.empty:
        raise RuntimeError(f"No market data returned for {symbol}.")

    closes = history["Close"].dropna()
    price = float(closes.iloc[-1])
    previous = float(closes.iloc[-2]) if len(closes) > 1 else None
    change = ((price - previous) / previous * 100) if previous else None

    market_cap = None
    try:
        market_cap = float(info.get("marketCap")) if info.get("marketCap") is not None else None
    except Exception:
        pass

    currency = "USD"
    try:
        currency = str(ticker.get_fast_info().get("currency") or "USD").upper()
    except Exception:
        pass

    return {
        "price": price,
        "previous_close": previous,
        "change_pct": change,
        "market_cap": market_cap,
        "currency": currency,
    }

@st.cache_data(ttl=300, show_spinner=False)
def get_price_history(symbol: str, period: str) -> pd.DataFrame:
    df = yf.Ticker(symbol).history(period=period, interval="1d", auto_adjust=False)
    if df.empty:
        return pd.DataFrame()
    df.index = pd.to_datetime(df.index).tz_localize(None)
    return df
