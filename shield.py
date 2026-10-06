def simulate_shield(investment: float, reference_price: float, current_price: float, shield_level: int) -> dict:
    """
    Scenario calculator only.
    shield_level is the percentage of the simulated LOSS that is hypothetically covered.
    It does not model an actual option price, collateral, counterparty, taxes, fees,
    volatility, strike, maturity, or execution.
    """
    if reference_price <= 0 or current_price <= 0:
        raise ValueError("Prices must be positive.")

    unprotected_value = investment * (current_price / reference_price)
    loss = max(0.0, investment - unprotected_value)
    protection = loss * (shield_level / 100.0)
    protected_value = unprotected_value + protection

    return {
        "unprotected_value": unprotected_value,
        "loss": loss,
        "protection": protection,
        "protected_value": protected_value,
    }
