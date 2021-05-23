import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


class YearSlider:
    def __init__(self, data_processing):
        self.data = data_processing

    def get_slider(self):
        return [
            dbc.Col(children=[
                html.Label('Filter landslides by years'),
                dcc.RangeSlider(
                    id='my-slider',
                    min=self.data.original_dataframe['year'].min(),
                    max=self.data.original_dataframe['year'].max(),
                    step=None,
                    value=[self.data.original_dataframe['year'].min(
                    ), self.data.original_dataframe['year'].max()],
                    marks={
                        str(year): str(year)
                        for year in self.data.original_dataframe['year'].unique()
                    }
                )
            ], width="12")
        ]
