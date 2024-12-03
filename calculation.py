
def calculate_metrics(current_volume, market_order_percentage, limit_order_percentage, market_order_fee_rate,
                      limit_order_fee_rate, circulating_supply, staker_apr, staker_share):
    # Calculate trading volumes
    market_volume = current_volume * (market_order_percentage / 100.0)  # Market orders volume
    limit_volume = current_volume * (limit_order_percentage / 100.0)  # Limit orders volume

    # Calculate fees
    market_fees = market_volume * (market_order_fee_rate / 100.0)
    limit_fees = limit_volume * (limit_order_fee_rate / 100.0)
    total_fees_daily = market_fees + limit_fees  # Total daily fees

    # Yearly fees
    yearly_fees = total_fees_daily * 365

    # Staker rewards
    staker_rewards_yearly = yearly_fees * (staker_share / 100)

    # Fair FDV calculation
    circulating_market_cap = staker_rewards_yearly / (staker_apr / 100)
    fair_fdv_target = circulating_market_cap / (circulating_supply / 100)

    # Fair APR Calculation
    fair_apr = (staker_rewards_yearly / (fair_fdv_target * (circulating_supply / 100))) * 100  # Should match staker_apr

    # % Fee of Stakers
    percent_fee_of_stakers = (staker_rewards_yearly / yearly_fees) * 100  # Should match staker_share

    return (market_volume, limit_volume, market_fees, limit_fees, yearly_fees, staker_rewards_yearly,
            fair_fdv_target, fair_apr, percent_fee_of_stakers, total_fees_daily)

