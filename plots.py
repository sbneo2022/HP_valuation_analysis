import plotly.graph_objects as go
import pandas as pd
import streamlit as st
from calculation import calculate_metrics
from simulators import PieChartSimulator

# Professional financial color palette
FINANCIAL_COLORS = [
    '#003f5c',  # Dark blue
    '#58508d',  # Purple
    '#bc5090',  # Pink
    '#ff6361',  # Coral
    '#ffa600',  # Orange
    '#374c80',  # Navy
    '#7a5195',  # Violet
    '#bc5090',  # Magenta
]

def create_pie_chart(labels, values):
    # Prepare data
    total = sum(values)
    percentages = [f"{(value/total*100):.1f}%" for value in values]

    # Create solid pie chart
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.0,  # Set hole to 0 for a solid pie chart
        textinfo='label+text',
        textposition='inside',
        text=percentages,
        texttemplate="%{label}<br>%{text}",
        textfont=dict(
            size=12,
            color='white',
            family="Arial"
        ),
        marker=dict(
            colors=FINANCIAL_COLORS,
            line=dict(color='white', width=2)
        ),
        hovertemplate="<b>%{label}</b><br>" +
                      "Amount: %{value:,.0f}<br>" +
                      "Share: %{text}<br>" +
                      "<extra></extra>",
        rotation=90,
        insidetextorientation='horizontal'
    )])

    # Update layout without center text
    fig.update_layout(
        title=dict(
            text="Pie Chart Visualization",
            y=0.95,
            x=0.5,
            xanchor='center',
            yanchor='top',
            font=dict(
                size=24,
                color='#2E4053',
                family="Arial Black"
            )
        ),
        height=500,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.1,
            xanchor="center",
            x=0.5,
            font=dict(
                size=12,
                family="Arial"
            ),
            bgcolor='rgba(255, 255, 255, 0.9)',
            bordercolor='rgba(0,0,0,0.1)',
            borderwidth=1
        ),
        margin=dict(t=80, b=80, l=20, r=20),
        paper_bgcolor='white',
        plot_bgcolor='white',
        uniformtext=dict(
            minsize=10,
            mode='hide'
        )
    )

    return fig


def display_valuation_metrics(tab, current_volume, market_volume, limit_volume, market_fees, limit_fees, total_fees_daily,
                              yearly_fees, fair_apr, circulating_supply, percent_fee_of_stakers, fair_fdv_target):
    with tab:
        st.subheader("Valuation Metrics")

        # Construct DataFrame for display
        data = {
            "Metric": [
                "Daily Volume ($M)",
                "Market Order ($M)",
                "Limit Order ($M)",
                "Market Fees ($M)",
                "Limit Fees ($M)",
                "Total Daily Fees ($M)",
                "Yearly Fees ($M)",
                "Fair APR (%)",
                "% Circulating Supply",
                "% Fee to Stakers",
                "Fair FDV ($M)",
            ],
            "Value": [
                current_volume,
                market_volume,
                limit_volume,
                market_fees,
                limit_fees,
                total_fees_daily,
                yearly_fees,
                fair_apr,
                circulating_supply,
                percent_fee_of_stakers,
                fair_fdv_target
            ]
        }

        df = pd.DataFrame(data)
        st.table(df)


def display_pie_chart_simulation(tab, pie_labels, pie_values, fair_fdv_target):
    with tab:
        st.subheader("Pie Chart Simulation: Distribution Overview")
        # Use fair_fdv_target to calculate the values
        pie_values = [fair_fdv_target * (value / 100) for value in pie_values]
        pie_simulator = PieChartSimulator(pie_labels, pie_values)
        pie_simulator.calculate()
        fig1 = pie_simulator.visualize()
        st.plotly_chart(fig1)


def display_fair_valuation_simulation(tab, staker_rewards_yearly, yearly_fees):
    with tab:
        st.subheader("Fair Valuation Simulation: Financial Breakdown")

        # Use yearly_fees to calculate the values
        labels = ['Rewards to Stakers', 'Other Fees']
        values = [staker_rewards_yearly, yearly_fees - staker_rewards_yearly]

        # Create pie chart
        fig2 = create_pie_chart(labels, values)

        st.plotly_chart(fig2)


def display_fdv_vs_volume_simulation(tab, market_order_percentage, limit_order_percentage, market_order_fee_rate,
                                     limit_order_fee_rate, circulating_supply, staker_apr, staker_share):
    with tab:
        st.subheader("FDV vs Daily Trading Volume")
        volumes = list(range(100, 5100, 100))
        fdv_values = []

        for volume in volumes:
            _, _, _, _, _, _, fair_fdv, _, _, _ = calculate_metrics(
                volume, market_order_percentage, limit_order_percentage, market_order_fee_rate,
                limit_order_fee_rate, circulating_supply, staker_apr, staker_share
            )
            fdv_values.append(fair_fdv)

        # Create the plot
        fig3 = go.Figure(data=go.Scatter(
            x=volumes,
            y=fdv_values,
            mode='lines+markers',
            line=dict(
                width=3,
                color='#1f77b4',  # Use a consistent color
                shape='spline'  # Smooth the line
            ),
            marker=dict(
                size=8,
                color='#ff7f0e',  # Marker color
                line=dict(width=1, color='DarkSlateGrey')
            ),
            hovertemplate="<b>Volume: %{x}</b><br>FDV: %{y:,.0f}<extra></extra>"
        ))

        # Update layout with improved styling
        fig3.update_layout(
            title={
                'text': "Fair FDV vs Daily Trading Volume",
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': dict(
                    size=24,
                    family="Arial Black",
                    color="#2E4053"
                )
            },
            xaxis_title=dict(
                text="Daily Trading Volume ($M)",
                font=dict(size=16, family="Arial")
            ),
            yaxis_title=dict(
                text="Fair FDV ($M)",
                font=dict(size=16, family="Arial")
            ),
            height=500,
            hovermode='x unified',
            showlegend=False,
            plot_bgcolor='rgba(240,240,240,0.3)',
            paper_bgcolor='white',
            font=dict(size=14, family="Arial"),
            dragmode='zoom',
            modebar=dict(
                bgcolor='rgba(255,255,255,0.7)',
                color='#2E4053',
                activecolor='#1f77b4'
            ),
        )

        # Enhanced grid lines and axes
        fig3.update_xaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(128,128,128,0.2)',
            showline=True,
            linewidth=2,
            linecolor='rgba(0,0,0,0.3)',
            mirror=True
        )

        fig3.update_yaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(128,128,128,0.2)',
            showline=True,
            linewidth=2,
            linecolor='rgba(0,0,0,0.3)',
            mirror=True,
            tickformat=','
        )

        st.plotly_chart(fig3, use_container_width=True)
