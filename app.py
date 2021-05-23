# Libraries
from components.WorldMap import WorldMap
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

# Classes

# Barplots
from components.AppData import AppData
from components.barplots.BarPlot import BarPlot
from components.barplots.CategoryBar import CategoryBar

from components.list import List
from components.year_slider import YearSlider
from components.WorldMap import WorldMap

# Dropdowns
from components.dropdowns.Category import Category
from components.dropdowns.LandslideSize import LandslideSize
from components.dropdowns.Country import Country
from components.dropdowns.SortCountryList import SortCountryList

external_stylesheets = [
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css',
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    dbc.themes.BOOTSTRAP
]

app = dash.Dash(__name__)
app = dash.Dash(external_stylesheets=external_stylesheets)

"""
Title of the App.
"""
app.title = 'Global Landslide Data'


"""
Use this when a component does not exist in the initial state 
(it is generated afterwards) to avoid any errors.
It is required as I was working on multipage application and loading components dynamically.
"""
app.config['suppress_callback_exceptions'] = True

content = html.Div(
    id="app-layout", children=[]
)

app.layout = html.Div([
    dcc.Location(id="url"),
    content
])


@app.callback(
    Output("app-layout", "children"),
    [Input("url", "pathname")]
)
def render_layout(pathname):
    if pathname == "/":
        return [
            html.Div([
                html.Div(id='card-1', children=[
                    dbc.Row(children=country.get_country()),
                    dbc.Row(children=category.get_category_dropdown()),
                    dbc.Row(children=land_slide_size.get_dropdown()),
                    dbc.Row(children=year_slider.get_slider()),
                    dbc.Row(children=[
                        dbc.Col(children=[
                            html.Div([
                                html.Label('Monthly Fatality Count'),
                                dcc.Graph(id='months-filter-fatality', figure=barplot.per_months_fatality_bar_plot(),
                                          style={'marginLeft': '10px'},
                                          config={
                                    'displayModeBar': False
                                })
                            ])
                        ])
                    ]),
                    dbc.Row(children=[
                        dbc.Col(children=[
                            html.Div([
                                html.Label('Monthly Injury Count'),
                                dcc.Graph(id='months-filter-injury', figure=barplot.per_months_injury_bar_plot(),
                                          style={'marginLeft': '10px'},
                                          config={
                                    'displayModeBar': False
                                })
                            ])
                        ])
                    ]),
                    dbc.Row(children=[
                        dbc.Col(children=[
                            html.Div([
                                html.Label('Category'),
                                dcc.Graph(id='category-graph', figure=category_bar.category_bar_plot([]),
                                          style={'marginLeft': '10px'},
                                          config={
                                    'displayModeBar': False
                                })
                            ])
                        ])
                    ])
                ], className="card scrollable", style={'grid-area': 'section1'}),
                html.Div(id='card-2', children=[
                    html.Div([
                        dcc.Checklist(
                            id="map_preference",
                            options=[
                                {'label': ' Toggle Map', 'value': 'wmap'}
                            ],
                            value=['wmap']
                        ),
                        dbc.Button("Reset Map",id="reset-map", className="btn btn-primary"),
                    ], style={'display':'flex', 'justify-content': 'space-between'}),
                    dcc.Graph(
                        id='the_graph', figure=world_map.world_map([], "world", ['wmap']),
                        style={'width': '100%', 'height': '100%'}
                    )
                ], className="card",  style={'grid-area': 'section2'}),
                html.Div(id='card-3', children=[
                    dbc.Row(
                        id='country_sort_list',
                        children=sort_country.get_sorting_options_dropdown('fatality_count'), style={
                            'margin-bottom': '5px'
                        }),
                    html.Div(id="list-component", children=[
                        list.generate_list('country_name'),
                    ], className="scrollable")
                ], className="card",  style={'grid-area': 'section3'}),
                html.Div(id='card-4', children=[
                    dcc.Graph(id='yearly_bar', figure=barplot.per_year_fatality_injury_bar_plot(),
                              style={'width': '100%', 'height': '100%'})
                ], className="card",  style={'grid-area': 'section4'})
            ], className="wrapper")
        ]

    if (pathname and pathname.startswith("/event/")):
        country_name = pathname.split('/')[-1]
        app_data.setCountry(country_name)
        world_map.detail_country_map(0, country_name)
        return [
            html.Div([
                html.Div([
                     dcc.Graph(
                         id='the_scatter_map', figure={},
                         style={'width': '100%', 'height': '100%'}
                     )
                ], style={'display': 'flex', 'justifyContent': 'center'})
            ]),
            html.Div(id='detail-page-list-items', children=[],
                     className="container"),
            html.Div(children=[
                dbc.Row(children=[
                    dbc.Col(children=[
                        dbc.Button("Load more", id="load-more", className="btn-primary", n_clicks=0)
                    ], width=12, style={'text-align': 'center'}),
                ], style={'margin-bottom': '10px'})
            ], className="container")
        ]

@app.callback(
    [
        Output('the_graph', 'figure'),
        Output('yearly_bar', 'figure'),
        Output('country_sort_list', 'children'),
        Output('list-component', 'children'),
        Output('category-graph', 'figure')
    ],
    [
        Input('my-slider', 'value'),
        Input('filter-data-country', 'value'),
        Input('filter-data-category', 'value'),
        Input('filter-data-landslide-size', 'value'),
        Input('filter-country-sort-list', 'value'),
        Input('map_preference', 'value'),
        Input('the_graph', 'clickData')
    ]
)
def main(years, selected_countries, categories, landslide_size, sort_country_list_value, map_preference,click_data):

    country_iso_code = 'world'
    if len(map_preference) != 0 and map_preference[0] == 'wmap' and click_data is not None:
        country_iso_code = click_data['points'][0]['location']

    if (selected_countries is not None) and len(selected_countries) != 0:
        country_iso_code = 'world'

    app_data.filter_data(years, categories, landslide_size, selected_countries)
    
    return [
        world_map.world_map(selected_countries, country_iso_code, map_preference),
        barplot.per_year_fatality_injury_bar_plot(),
        sort_country.get_sorting_options_dropdown(sort_country_list_value),
        list.generate_list(sort_country_list_value),
        category_bar.category_bar_plot(categories)
    ]


"""
    To reset map again to show all countries.
    By clicking this button continent view will be changed to world view again.
"""
@app.callback(
    Output('the_graph', 'clickData'),
    [Input('reset-map', 'n_clicks')]
)
def reset_world_map(n_clicks):
    return None


"""
                        *Load more*
    Loads events for a country and append dynamically.
    In this way it is possible to load thousands of events 
    without crashing the system
"""


@app.callback(
    [Output('detail-page-list-items', 'children'),
    Output('the_scatter_map', 'figure')],
    [
        Input('load-more', 'n_clicks'),
        Input("url", "pathname")
    ],
    [State('detail-page-list-items', 'children')]
)
def load_more(n_clicks, pathname, children):
    country = pathname.split('/')[-1]
    app_data.setCountry(country)
    new_events = app_data.load_more_events(n_clicks, country)
    children.append(new_events)
    detail_page_map = world_map.detail_country_map(n_clicks, country)
    return [children, detail_page_map]


if __name__ == '__main__':

    app_data = AppData()
    barplot = BarPlot(app_data)
    world_map = WorldMap(app_data)
    list = List(app_data)
    year_slider = YearSlider(app_data)
    country = Country(app_data)
    category_bar = CategoryBar(app_data)
    land_slide_size = LandslideSize(app_data)
    sort_country = SortCountryList(app_data)
    category = Category(app_data)

    app.run_server(debug=True, dev_tools_hot_reload=False, port="4200")
