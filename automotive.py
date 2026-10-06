import io
import requests
import pandas as pd
import streamlit as st

OWID_BATTERY_URL = "https://ourworldindata.org/grapher/price-of-lithium-ion-battery-cells.csv?v=1&csvType=full&useColumnShortNames=false"

# Latest company-reported operating figures available for the MVP.
# Values are deliberately stored with source/date metadata so the UI does not present
# them as live market data.
COMPANY_REPORTS = {
    "TSLA": {
        "period": "Q2 2026",
        "sales": 480126,
        "deliveries": 480126,
        "production": 451758,
        "ev_share": "100% of vehicle deliveries",
        "market_share": "Company-specific global share not disclosed in the release",
        "dealer_inventory": "Tesla does not report dealer inventory; direct-sales model",
        "incentives": "Company-specific figure not disclosed in the release",
        "recalls": "See NHTSA / Tesla recall notices",
        "production_guidance": "2026 company outlook in shareholder materials",
        "source": "Tesla Q2 2026 Production, Deliveries & Deployments",
        "source_url": "https://ir.tesla.com/press-release/tesla-second-quarter-2026-production-deliveries-and-deployments",
    },
    "F": {
        "period": "H1 2026",
        "sales": 1006515,
        "deliveries": 1006515,
        "production": "See Ford production disclosures",
        "ev_share": "Company-specific EV share requires Ford sales breakdown",
        "market_share": "12.3% estimated June U.S. retail share",
        "dealer_inventory": "Not included in the cited sales release",
        "incentives": "Not disclosed as one consolidated figure in the cited release",
        "recalls": "See Ford recall notices / NHTSA",
        "production_guidance": "2026 guidance in Q2 financial results",
        "source": "Ford H1/Q2 2026 Sales Results",
        "source_url": "https://www.fromtheroad.ford.com/us/en/articles/2026/ford-2026-second-quarter-sales-results?pubDate=20260711",
    },
    "GM": {
        "period": "Q2 2026",
        "sales": 714896,
        "deliveries": 714896,
        "production": "See GM quarterly operating materials",
        "ev_share": "GM reported it remained #2 U.S. EV seller; exact share varies by scope",
        "market_share": "U.S. Q2 sales: 714,896 vehicles; company reported #1 U.S. automaker by sales",
        "dealer_inventory": "Some inventory constraints reported in Q2 release",
        "incentives": "Company discussed pricing/incentive discipline; no single consolidated figure in release",
        "recalls": "See GM recall notices / NHTSA",
        "production_guidance": "2026 guidance raised with Q2 results",
        "source": "GM Q2 2026 Sales / Earnings Release",
        "source_url": "https://investor.gm.com/news-releases/news-release-details/gm-releases-2026-second-quarter-results",
    },
    "RIVN": {
        "period": "Latest company quarterly release",
        "sales": "See latest Rivian production/delivery release",
        "deliveries": "See latest Rivian production/delivery release",
        "production": "See latest Rivian production/delivery release",
        "ev_share": "Rivian is an EV-only manufacturer",
        "market_share": "Company-specific global share is not reported as one consolidated live metric",
        "dealer_inventory": "Rivian primarily uses a direct-sales model; dealer inventory is not applicable",
        "incentives": "Company-specific consolidated figure not reported",
        "recalls": "See NHTSA / Rivian recall notices",
        "production_guidance": "See latest Rivian shareholder letter",
        "source": "Rivian Investor Relations",
        "source_url": "https://rivian.com/investors",
    },
    "TM": {
        "period": "Latest Toyota IR disclosures",
        "sales": "See Toyota latest financial/sales release",
        "deliveries": "See Toyota latest financial/sales release",
        "production": "See Toyota latest production release",
        "ev_share": "See Toyota electrified-vehicle disclosures",
        "market_share": "See Toyota market disclosures by region",
        "dealer_inventory": "See Toyota regional disclosures",
        "incentives": "See Toyota regional disclosures",
        "recalls": "See Toyota recall notices",
        "production_guidance": "See Toyota latest IR guidance",
        "source": "Toyota Investor Relations",
        "source_url": "https://global.toyota/en/ir/",
    },
}

@st.cache_data(ttl=86400, show_spinner=False)
def get_battery_price() -> dict:
    try:
        df = pd.read_csv(OWID_BATTERY_URL)
        # OWID may expose the indicator under a long translated column name.
        value_col = [c for c in df.columns if c not in {"Entity", "Code", "Year"}][0]
        df = df.dropna(subset=[value_col]).sort_values("Year")
        row = df.iloc[-1]
        return {
            "value": float(row[value_col]),
            "year": int(row["Year"]),
            "unit": "USD/kWh (constant 2024 USD)",
            "source": "Our World in Data / Rupert Way",
            "url": "https://ourworldindata.org/grapher/price-of-lithium-ion-battery-cells",
        }
    except Exception as exc:
        return {"value": None, "year": None, "unit": "USD/kWh", "source": f"Battery dataset unavailable: {exc}", "url": "https://ourworldindata.org/grapher/price-of-lithium-ion-battery-cells"}


def get_automotive_metrics(symbol: str, fundamentals: dict) -> dict:
    r = COMPANY_REPORTS.get(symbol, {})
    battery = get_battery_price()
    capex = fundamentals.get("capex")
    cfo = fundamentals.get("operating_cash_flow")
    cash_burn = None
    if cfo is not None and cfo < 0:
        cash_burn = abs(cfo)
    elif cfo is not None:
        cash_burn = 0.0

    return {
        "vehicle_sales": r.get("sales", "Unavailable"),
        "deliveries": r.get("deliveries", "Unavailable"),
        "registrations": "Use regional registration feed; company releases do not standardize this metric",
        "market_share": r.get("market_share", "Unavailable"),
        "ev_penetration": r.get("ev_share", "Unavailable"),
        "dealer_inventory": r.get("dealer_inventory", "Unavailable"),
        "incentives": r.get("incentives", "Unavailable"),
        "recalls": r.get("recalls", "Unavailable"),
        "battery_prices": f"${battery['value']:.1f}/kWh ({battery['year']})" if battery.get("value") is not None else "Unavailable",
        "production_guidance": r.get("production_guidance", "Unavailable"),
        "margins": fundamentals.get("operating_margin", "Calculated from reported financials where available"),
        "capex": capex if capex is not None else "Calculated from SEC/financial statements when available",
        "cash_burn": cash_burn if cash_burn is not None else "Positive operating cash flow / no burn in latest reported period",
        "period": r.get("period", "Latest available"),
        "source": r.get("source", "Company investor relations"),
        "source_url": r.get("source_url", ""),
        "battery_source": battery.get("source"),
        "battery_url": battery.get("url"),
    }
