import os
import requests
import pandas as pd
import streamlit as st
from data.company import COMPANIES

SEC_HEADERS = {
    "User-Agent": os.getenv("SEC_USER_AGENT", "Vestra research contact@example.com"),
    "Accept-Encoding": "gzip, deflate",
}

def _latest_fact(facts, concept_names):
    units = facts.get("units", {})
    for unit_name, points in units.items():
        if not points:
            continue
        df = pd.DataFrame(points)
        if "fy" in df.columns:
            annual = df[df["fy"].notna()].copy()
        else:
            annual = df.copy()
        if annual.empty:
            continue
        annual["filed"] = pd.to_datetime(annual["filed"], errors="coerce")
        annual = annual.sort_values("filed")
        return float(annual.iloc[-1]["val"])
    return None

@st.cache_data(ttl=3600, show_spinner=False)
def get_sec_fundamentals(cik: str) -> dict:
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{int(cik):010d}.json"
    r = requests.get(url, headers=SEC_HEADERS, timeout=20)
    r.raise_for_status()
    data = r.json()
    facts = data.get("facts", {}).get("us-gaap", {})

    mapping = {
        "revenue": ["RevenueFromContractWithCustomerExcludingAssessedTax", "SalesRevenueNet"],
        "net_income": ["NetIncomeLoss"],
        "operating_cash_flow": ["NetCashProvidedByUsedInOperatingActivities"],
        "free_cash_flow": [],
        "capex": ["PaymentsToAcquirePropertyPlantAndEquipment"],
    }

    out = {}
    for key, concepts in mapping.items():
        value = None
        for concept in concepts:
            if concept in facts:
                value = _latest_fact(facts[concept])
                if value is not None:
                    break
        out[key] = value

    # FCF = CFO - CapEx when both are available.
    capex = out.get("capex")
    if out.get("operating_cash_flow") is not None and capex is not None:
        out["free_cash_flow"] = out["operating_cash_flow"] - abs(capex)
    revenue = out.get("revenue")
    net_income = out.get("net_income")
    if revenue and net_income is not None:
        out["operating_margin"] = net_income / revenue * 100
    return out

@st.cache_data(ttl=3600, show_spinner=False)
def get_fundamentals(symbol: str) -> dict:
    company = COMPANIES[symbol]
    cik = company.get("cik")
    if cik:
        try:
            result = get_sec_fundamentals(cik)
            result["source"] = "SEC EDGAR Company Facts"
            return result
        except Exception as exc:
            # Do not invent values. Return unavailable values and surface the source issue.
            return {
                "revenue": None,
                "net_income": None,
                "operating_cash_flow": None,
                "free_cash_flow": None,
                "capex": None,
                "operating_margin": None,
                "source": f"SEC unavailable: {exc}",
            }

    # For non-US companies in this MVP, use the market provider only for fields it actually exposes.
    # We deliberately do not label those values as SEC data.
    import yfinance as yf
    t = yf.Ticker(symbol)
    fin = t.financials
    out = {"revenue": None, "net_income": None, "operating_cash_flow": None, "free_cash_flow": None, "capex": None, "operating_margin": None,
           "source": "Yahoo Finance company financials"}
    if fin is not None and not fin.empty:
        def latest_row(names):
            for n in names:
                if n in fin.index:
                    vals = fin.loc[n].dropna()
                    if len(vals):
                        return float(vals.iloc[0])
            return None
        out["revenue"] = latest_row(["Total Revenue"])
        out["net_income"] = latest_row(["Net Income"])
        out["operating_margin"] = (out["net_income"] / out["revenue"] * 100) if out["revenue"] else None
    return out
