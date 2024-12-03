from abc import ABC, abstractmethod
from typing import List
import plotly.graph_objects as go

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

# Abstract base class for simulators
class Simulator(ABC):
    @abstractmethod
    def calculate(self):
        pass

    @abstractmethod
    def visualize(self):
        pass

# Pie Chart Simulator Implementation
class PieChartSimulator(Simulator):
    def __init__(self, labels: List[str], values: List[float]):
        self.labels = labels
        self.values = values

    def calculate(self):
        self.total = sum(self.values)
        self.percentages = [value / self.total * 100 for value in self.values]

    def visualize(self):
        # Prepare data
        values = self.values
        labels = self.labels
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