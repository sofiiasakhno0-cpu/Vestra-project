# Vestra — Automotive Investment Intelligence

A working Streamlit MVP based on the Vestra brief.

## What is live and real

- Market prices/history are fetched at runtime through `yfinance` (Yahoo Finance data).
- US-company financial facts are fetched directly from the SEC EDGAR Company Facts API.
- Company/investor-relations URLs are first-party links.
- No market price, revenue, profit, production or protection payout is hard-coded as a fake live value.
- When a requested company metric is not available from the selected source, the UI says "Unavailable" instead of inventing a number.

## Companies

The MVP includes the four assets recommended in the brief:
- Tesla (TSLA)
- Ford (F)
- General Motors (GM)
- Rivian (RIVN)

Toyota (TM) is also included as an additional automotive company. Because Toyota is not a US SEC registrant in the same way as the four US companies, its financial section uses the market-data provider rather than pretending it is SEC data.

## Vestra Shield

The Shield module is intentionally a **scenario calculator**, not an executed hedge.

It calculates:

loss = max(0, investment - simulated_position_value)

protection = loss × shield_level

protected_value = simulated_position_value + protection

The real brief identifies options hedging, a protection pool, and mixed safe-asset/equity structures as possible mechanisms. An actual financial product would require regulated counterparties, legal documentation, pricing, collateral, risk limits and an actual execution/settlement layer. This demo does not claim to provide those.

## Run

1. Install Python 3.10–3.14.
2. Open this folder in VS Code.
3. Create a virtual environment:

   Windows:
   `python -m venv .venv`
   `.venv\Scripts\activate`

4. Install:
   `pip install -r requirements.txt`

5. Copy `.env.example` to `.env` and replace the SEC user-agent email.

6. Run:
   `streamlit run app.py`

The browser should open the local Vestra dashboard.

## Data-source note

The SEC EDGAR APIs are public and do not require an API key. Yahoo Finance/yfinance is used for market prices because it is convenient for an MVP; it should not be described as an official company source or as guaranteed real-time exchange data.

For production, replace/augment the market-data adapter with a licensed market-data feed and build a dedicated automotive-data adapter for verified production, deliveries, registrations, market share, recalls, incentives, battery prices and guidance.


## Reworked UI
Black-only theme; removed top/right method areas; Financial Intelligence moved directly under Market Intelligence; added local prototype account registration/login and Automotive Intelligence fields: sales, deliveries, registrations, market share, EV penetration, dealer inventory, incentives, recalls, battery prices, production guidance, margins, CAPEX and cash burn.
