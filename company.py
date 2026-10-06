COMPANIES = {
    "TSLA": {
        "name": "Tesla, Inc.",
        "sector": "Automotive / Energy",
        "country": "United States",
        "description": "Electric vehicles, energy generation/storage and related technology.",
        "tokenized": "TSLAx",
        "token_route": "External tokenized representation; Vestra does not issue the security token.",
        "official_url": "https://ir.tesla.com/",
        "sec_url": "https://www.sec.gov/edgar/browse/?CIK=1318605",
        "cik": "1318605",
        "automotive_metrics": {
            "Production / deliveries": {
                "value": "Use Tesla quarterly delivery/production release",
                "period": "Official release",
                "source": "Tesla Investor Relations"
            }
        }
    },
    "F": {
        "name": "Ford Motor Company",
        "sector": "Automotive",
        "country": "United States",
        "description": "Automotive manufacturer with Ford Blue, Ford Model e and Ford Pro businesses.",
        "tokenized": "Fx",
        "token_route": "External tokenized representation; Vestra does not issue the security token.",
        "official_url": "https://shareholder.ford.com/",
        "sec_url": "https://www.sec.gov/edgar/browse/?CIK=37996",
        "cik": "37996",
        "automotive_metrics": {
            "Vehicle production / sales": {
                "value": "See Ford quarterly sales releases",
                "period": "Official release",
                "source": "Ford Investor Relations"
            }
        }
    },
    "GM": {
        "name": "General Motors Company",
        "sector": "Automotive",
        "country": "United States",
        "description": "Automotive manufacturer and mobility company.",
        "tokenized": "GMx",
        "token_route": "External tokenized representation; Vestra does not issue the security token.",
        "official_url": "https://investor.gm.com/",
        "sec_url": "https://www.sec.gov/edgar/browse/?CIK=1467858",
        "cik": "1467858",
        "automotive_metrics": {
            "Vehicle deliveries / sales": {
                "value": "See GM quarterly sales releases",
                "period": "Official release",
                "source": "GM Investor Relations"
            }
        }
    },
    "RIVN": {
        "name": "Rivian Automotive, Inc.",
        "sector": "Automotive / EV",
        "country": "United States",
        "description": "Electric vehicle manufacturer focused on consumer and commercial vehicles.",
        "tokenized": "RIVNx",
        "token_route": "External tokenized representation; Vestra does not issue the security token.",
        "official_url": "https://rivian.com/investors",
        "sec_url": "https://www.sec.gov/edgar/browse/?CIK=1874178",
        "cik": "1874178",
        "automotive_metrics": {
            "Production / deliveries": {
                "value": "See Rivian quarterly production/delivery releases",
                "period": "Official release",
                "source": "Rivian Investor Relations"
            }
        }
    },
    "TM": {
        "name": "Toyota Motor Corporation",
        "sector": "Automotive",
        "country": "Japan",
        "description": "Global automotive manufacturer with Toyota and Lexus brands and mobility businesses.",
        "tokenized": "Not hard-coded as a Vestra-issued token",
        "token_route": "External representation must be verified before use.",
        "official_url": "https://global.toyota/en/ir/",
        "sec_url": None,
        "cik": None,
        "automotive_metrics": {}
    },
}


_AUTOMOTIVE_FIELDS = {
"vehicle_sales":"Company sales disclosures / market data","deliveries":"Quarterly deliveries",
"registrations":"Registration data","market_share":"Market share by region/segment",
"ev_penetration":"EV share / penetration","dealer_inventory":"Dealer inventory / days supply",
"incentives":"Incentives and discounts","recalls":"Safety recalls / campaigns",
"battery_prices":"Battery cost / price indicators","production_guidance":"Production guidance",
"margins":"Automotive margins","capex":"CAPEX","cash_burn":"Cash burn / liquidity"}
for _t,_c in COMPANIES.items():
    _c["automotive_intelligence"]={**_AUTOMOTIVE_FIELDS,**_c.get("automotive_intelligence",{})}
