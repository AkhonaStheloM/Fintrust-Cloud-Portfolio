def calculate_savings_plan_savings(hourly_commitment_usd, term_years=3,
                                     discount_pct=0.66):
    """
    Compute total savings vs On-Demand for a Compute Savings Plan.
    hourly_commitment_usd: the $/hr commitment you make
    discount_pct: Compute SP gives up to 66% off On-Demand
    """
    # What you would pay on-demand for the same compute
    effective_ondemand_hourly = hourly_commitment_usd / (1 - discount_pct)

    hours_in_period = term_years * 365 * 24

    total_ondemand_cost = effective_ondemand_hourly * hours_in_period
    total_sp_cost       = hourly_commitment_usd      * hours_in_period
    total_savings       = total_ondemand_cost - total_sp_cost

    return {
        'commitment_per_hour':       hourly_commitment_usd,
        'effective_ondemand_hourly': round(effective_ondemand_hourly, 4),
        'total_ondemand_cost':       round(total_ondemand_cost, 2),
        'total_sp_cost':             round(total_sp_cost, 2),
        'total_savings_usd':         round(total_savings, 2),
        'savings_pct':               round(discount_pct * 100, 1)
    }

# FinTrust scenario: $32.47/hr commitment across 14 accounts
result = calculate_savings_plan_savings(
    hourly_commitment_usd=32.47,
    term_years=3,
    discount_pct=0.66
)
for k, v in result.items():
    print(f'{k}: {v}')