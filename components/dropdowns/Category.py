import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

class Category:
    def __init__(self, data_processing):
        self.data = data_processing

    def get_category_dropdown(self):
        return [
            dbc.Col(children=[
                html.Label('Filter landslides by category'),
                dcc.Dropdown(
                    id='filter-data-category',
                    options=[
                        ({'label': str(v), 'value': str(k)})
                        for k, v in self.data.get_category().items()
                    ],
                    placeholder="Select a category...",
                    searchable=True,
                    clearable=True,
                    multi=True,
                    style={
                        'fontSize': '14px',
                        'width': '-webkit-fill-available'
                    }
                ),
            ], width="12")
        ]
