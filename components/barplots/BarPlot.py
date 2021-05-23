import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import plotly.express as px


class BarPlot:
    def __init__(self, data_processing):
        self.data = data_processing

    def per_months_fatality_bar_plot(self):
        grouped_data = self.data.dataframe_copy.groupby(['month'])[
            'fatality_count'].sum()
        fig = go.Figure(data=[
            go.Bar(
                x=grouped_data.index,
                y=grouped_data,
                marker_color='rgb(239,84,59)',
                marker={
                    'color': grouped_data,
                    'colorscale': 'reds'
                }
            )],
            layout=go.Layout(
                coloraxis_showscale=False,
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color="#67748E"),
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(t=10, b=0, r=30, l=30),
                height=120,
                xaxis=dict(
                    tickmode='array',
                    tickvals=grouped_data.index,
                    ticktext=[
                        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
                    ]
                )
        )
        )
        fig.update_traces(
            marker_line_color='rgb(87, 48, 48)',
            marker_line_width=1
        )
        return fig

    def per_months_injury_bar_plot(self):
        grouped_data = self.data.dataframe_copy.groupby(['month'])[
            'injury_count'].sum()
        fig = go.Figure(data=[
            go.Bar(
                x=grouped_data.index,
                y=grouped_data,
                marker_color='rgb(239,84,59)',
                marker={
                    'color': grouped_data,
                    'colorscale': 'reds'
                }
            )],
            layout=go.Layout(
                coloraxis_showscale=False,
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color="#67748E"),
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(t=10, b=0, r=30, l=30),
                height=120,
                xaxis=dict(
                    tickmode='array',
                    tickvals=grouped_data.index,
                    ticktext=[
                        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
                    ]
                )
        )
        )
        fig.update_traces(
            marker_line_color='rgb(87, 48, 48)',
            marker_line_width=1
        )
        return fig

    def per_year_fatality_injury_bar_plot(self):
        timeline_df = self.data.get_years_timeline()
        fig = go.Figure(
            data=[
                go.Bar(name='Total Events Occured', x=timeline_df.index,
                       y=timeline_df['Total_Events_Occured'], marker_color='rgb(239,84,59)'),
                go.Bar(name='Deaths', x=timeline_df.index,
                       y=timeline_df['Deaths'], marker_color='rgb(98,109,250)'),
                go.Bar(name='Injuries', x=timeline_df.index,
                       y=timeline_df['Injuries'], marker_color='rgb(5,204,150)'),
            ],
            layout=go.Layout(
                margin=dict(t=20, b=20, r=20, l=20), paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#67748E"
                                                        )
            ))

        return fig
