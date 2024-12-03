from abc import ABC, abstractmethod
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from typing import List
from plots import create_pie_chart, display_valuation_metrics, display_pie_chart_simulation, display_fair_valuation_simulation, display_fdv_vs_volume_simulation
from calculation import calculate_metrics  

# Abstract base class for simulators
class Simulator(ABC):
    @abstractmethod
    def calculate(self):
        pass

    @abstractmethod
    def visualize(self):
        pass


# Pie Chart Simulator Implementation
def get_sidebar_inputs():
    st.sidebar.title("Input Parameters")

    # Trading Volume and Fees
    st.sidebar.header("Trading Volume and Fees")
    current_volume = st.sidebar.number_input("Current Trading Volume ($M)", value=1000.0, step=100.0)

    # Volume percentages
    market_order_percentage = st.sidebar.slider("Market Order Volume (%)", 0.0, 100.0, 75.0, step=1.0)  # Default 75%
    limit_order_percentage = 100.0 - market_order_percentage  # Remaining percentage

    # Fee rates
    market_order_fee_rate = st.sidebar.number_input("Market Order Fee Rate (%)", value=0.024, step=0.001, format="%.3f")  # Default 0.024%
    limit_order_fee_rate = st.sidebar.number_input("Limit Order Fee Rate (%)", value=-0.002, step=0.001, format="%.3f")  # Default -0.002%

    # Tokenomics
    st.sidebar.header("Tokenomics")
    circulating_supply = st.sidebar.number_input("Circulating Supply (%)", value=40.0, step=1.0)  # Default 40%
    staker_apr = st.sidebar.slider("Fair APR (%)", 5.0, 15.0, 10.0, step=0.1)  # Default 10%

    # Fee Allocation
    st.sidebar.header("Fee Allocation")
    staker_share = st.sidebar.slider("Stakers' Share of Fees (%)", 50.0, 100.0, 75.0, step=1.0)  # Default 75%

    # Pie Chart Input
    st.sidebar.header("Pie Chart Input")
    st.sidebar.write("Enter the values for each category. The sum should be 100.")

    # Labels are constant
    pie_labels = ["Airdrop", "Team", "Block Rewards"]

    # Values are entered separately
    airdrop_value = st.sidebar.number_input("Airdrop (%)", min_value=0.0, max_value=100.0, value=25.0, step=0.1)
    team_value = st.sidebar.number_input("Team (%)", min_value=0.0, max_value=100.0, value=35.0, step=0.1)
    block_rewards_value = st.sidebar.number_input("Block Rewards (%)", min_value=0.0, max_value=100.0, value=40.0, step=0.1)

    # Ensure the sum of values is 100
    total_value = airdrop_value + team_value + block_rewards_value
    if total_value != 100:
        st.sidebar.error(f"The total percentage must be 100. Current total: {total_value:.1f}%")

    pie_values = [airdrop_value, team_value, block_rewards_value]

    return (current_volume, market_order_percentage, limit_order_percentage, market_order_fee_rate,
            limit_order_fee_rate, circulating_supply, staker_apr, staker_share, pie_labels, pie_values)

# Main application logic
def main():
    # Title
    st.title("Hyperliquid Metrics, Valuation, and Simulations")

    # Tabs for different sections
    tab1, tab2, tab3 = st.tabs(["Valuation Metrics", "Pie Chart Simulation", "Fair Valuation Simulation"])

    # Sidebar Inputs
    (current_volume, market_order_percentage, limit_order_percentage, market_order_fee_rate,
     limit_order_fee_rate, circulating_supply, staker_apr, staker_share, pie_labels, pie_values) = get_sidebar_inputs()

    # Calculations shared across tabs
    (market_volume, limit_volume, market_fees, limit_fees, yearly_fees, staker_rewards_yearly,
     fair_fdv_target, fair_apr, percent_fee_of_stakers, total_fees_daily) = calculate_metrics(
        current_volume, market_order_percentage, limit_order_percentage, market_order_fee_rate,
        limit_order_fee_rate, circulating_supply, staker_apr, staker_share
    )

    # Display each tab
    display_valuation_metrics(tab1, current_volume, market_volume, limit_volume, market_fees, limit_fees, total_fees_daily,
                              yearly_fees, fair_apr, circulating_supply, percent_fee_of_stakers, fair_fdv_target)
    display_pie_chart_simulation(tab2, pie_labels, pie_values, fair_fdv_target)
    display_fair_valuation_simulation(tab3, staker_rewards_yearly, yearly_fees)


if __name__ == "__main__":
    main()
