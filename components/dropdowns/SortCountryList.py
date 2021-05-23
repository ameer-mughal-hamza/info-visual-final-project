import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

class SortCountryList:
    def __init__(self, data_processing):
        self.data = data_processing

    def get_sorting_options_dropdown(self, sort_country_list_value):
        sorting_options = {
            'Country Name': 'country_name', 
            'Fatality Count': 'fatality_count', 
            'Injury Count': 'injury_count'
        }
        return [
            dbc.Col(children=[
                html.Label('Sort list by'),
                dcc.Dropdown(
                    id='filter-country-sort-list',
                    options=[
                        ({'label': str(k), 'value': str(v)})
                        for k, v in sorting_options.items()
                    ],
                    placeholder="Select sort option...",
                    searchable=True,
                    clearable=True,
                    value=sort_country_list_value,
                    style={
                        'fontSize': '14px',
                        'width': '-webkit-fill-available'
                    }
                ),
            ], width="12")
        ]
