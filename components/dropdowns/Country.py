import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

class Country:
    def __init__(self, data_processing):
        self.data = data_processing

    def get_country(self):
        return [
            dbc.Col(children=[
                html.Label('Filter landslides by country'),
                dcc.Dropdown(
                    id='filter-data-country',
                    options=[
                        ({'label': str(k), 'value': str(v)})
                        for k, v in self.data.get_country_list_for_dropdown().items()
                    ],
                    placeholder="Select a country...",
                    searchable=True,
                    clearable=True,
                    multi=True,
                    style={
                        'fontSize': '14px',
                        'width': '-webkit-fill-available'
                    }
                ),
                # html.Div([
                #     dbc.Button("Reset Map", id="reset-map", className="btn-block mt-1")
                # ])
            ], width="12"
            ),
        ]
