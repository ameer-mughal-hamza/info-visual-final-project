import plotly.graph_objects as go

class CategoryBar:
    def __init__(self, data_processing):
        self.data = data_processing

    def category_bar_plot(self, selected_categories):
        grouped_data = self.data.dataframe_copy.groupby(['landslide_trigger'])[
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
                height=160,
                xaxis=dict(
                    tickmode='array',
                    tickvals=grouped_data.index,
                    ticktext=selected_categories
                )
        )
        )
        fig.update_traces(
            marker_line_color='rgb(87, 48, 48)',
            marker_line_width=1
        )
        return fig