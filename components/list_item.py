import dash_html_components as html
import dash_bootstrap_components as dbc


class ListItem:
    def __init__(self, data_processing):
        self.data = data_processing

    def generateItems(self, sort_country_list_value):
        self.list = []

        for _, item in self.data.get_incident_data_by_country(sort_country_list_value).iterrows():
            flag_code = self.data.getISO3Code(item['iso_alpha'])
            if flag_code is not None:
                self.list.append(
                    html.Div([
                        dbc.Row([
                            html.Div([
                                html.Img(src="./assets/flags/" + flag_code + ".svg", width="35", title=item['country_name'], style={
                                    'align-self': 'flex-start',
                                    'margin-top': '4px'
                                }),
                                html.H6(item['country_name'], style={
                                    'font-size': '12px', 'margin-left': '7px', 'font-weight': '700'})
                            ], className="d-flex"),
                        ]),
                        dbc.Row([
                            dbc.Col([
                                html.Img(src="./assets/icons/death.png",
                                        width="35", title="Total Fatalities"),
                                html.P(item['FatalityCount'],
                                    style={'font-size': '14px'})
                            ], className="text-center"),
                            dbc.Col([
                                html.Img(src="./assets/icons/patient.svg",
                                        width="35", title="Total Injuries"),
                                html.P(item['InjuriesCount'],
                                    style={'font-size': '14px'})
                            ], className="text-center")
                            ], justify="center"
                        ),
                        dbc.Row([
                            html.A("Show Details", target="_blank", href="/event/" + item['iso_alpha'], className="btn btn-lg btn-primary btn-block",
                                style={'text-decoration': 'none'})
                        ], justify="center")
                    ], style={'border-top': '1px solid black', 'margin-bottom': '10px'})
                )
        return self.list
