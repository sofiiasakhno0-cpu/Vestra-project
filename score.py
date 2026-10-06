def calculate_vestra_score(market: dict, fundamentals: dict) -> float:
    """
    Transparent, non-predictive information score.
    Missing inputs do not receive an invented value; the score is normalized
    over available components.
    """
    components = []

    change = market.get("change_pct")
    if change is not None:
        components.append(max(0, min(100, 50 + change * 5)))

    revenue = fundamentals.get("revenue")
    net_income = fundamentals.get("net_income")
    if revenue is not None and revenue > 0:
        components.append(60)
    if net_income is not None:
        components.append(70 if net_income >= 0 else 30)

    return sum(components) / len(components) if components else 0.0
