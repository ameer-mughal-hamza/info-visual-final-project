import re
from dash_html_components.Span import Span
import pandas as pd
import json
from urllib.request import urlopen
import numpy as np
import json

from plotly.express import data
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import datetime

# reading countries json file.
with open('assets/data/countries.json', 'r') as f:
    countries = json.load(f)

# reading countries json file.
with open('assets/data/countries_continent.json', 'r') as f:
    countries_continent = json.load(f)

# reading countries json file.
with open('assets/data/countries_latlon.json', 'r') as f:
    countries_latlon = json.load(f)


class AppData():

    __instance = None
    __country = None

    def getInstance():
        if AppData.__instance == None:
            AppData()
        return AppData.__instance

    def __init__(self):

        if AppData.__instance != None:
            raise Exception("Multiple instance of Main class not allowed.")
        else:
            AppData.__instance = self

        self.df = pd.DataFrame()
        self.read_file = pd.read_excel("./assets/data/glc.xlsx", sheet_name="glc_new_columns")
        self.original_dataframe = self.df.append(self.read_file, ignore_index=True)

        self.dataframe_copy = self.original_dataframe

        self.total_deaths_per_country = self.dataframe_copy.groupby(
            ['country_name'])['fatality_count'].sum()
        self.total_deaths = self.dataframe_copy['fatality_count'].sum()

        """
        Loads countries json file to get ISO_ALPHA 3 code and any other country information from there
        """
        with open('assets/data/countries.json', 'r') as f:
            self.countries_json = json.load(f)

    def setCountry(self, country):
        self.__country = country

    def getCountry(self):
        return self.__country

    def get_category(self):
        """
            Filter records with these two values: ['nan']
        """
        self.filtered_df = self.dataframe_copy.loc[
            (~self.dataframe_copy['landslide_trigger2'].isnull())
        ]
        self.filtered_df = self.filtered_df.sort_values(
            by=['landslide_trigger2'], ascending=True)
        return dict(
            zip(
                self.filtered_df['landslide_trigger'].unique(),
                self.filtered_df['landslide_trigger2'].unique()
            )
        )

    def get_landslide_size(self):
        """
            Filter records with these two values: ['Unknown', 'nan']
        """
        self.filtered_df = self.dataframe_copy.loc[
            (~self.dataframe_copy['landslide_size'].isnull())
        ]
        self.filtered_df = self.filtered_df.sort_values(
            by=['landslide_size'], ascending=True)
        return dict(
            zip(
                self.filtered_df['landslide_size'].unique(),
                self.filtered_df['landslide_size2'].unique()
            )
        )

    def getISO3Code(self, name):
        for keyval in countries:
            if name.lower() == keyval['alpha-3'].lower():
                return keyval['alpha-2']

    def getRegionInfoWithCountryName(self, name):
        for keyval in countries_continent:
            if name.lower() == keyval['Three_Letter_Country_Code'].lower():
                return keyval['Continent_Name']

    def get_country_latlon(self, name):
        for keyval in countries_latlon:
            if name.lower() == keyval['country_code'].lower():
                return keyval['latlng']

    def get_monthly_fatality_count(self):
        return self.filter_accident_df.groupby(['month'])['fatality_count'].sum()

    def get_country_list_for_dropdown(self):
        self.dataframe_copy = self.dataframe_copy[~self.dataframe_copy['country_name'].isnull(
        )]
        self.dataframe_copy = self.dataframe_copy.sort_values(
            by=['country_name'], ascending=True)
        return dict(
            zip(
                self.dataframe_copy['country_name'].unique(),
                self.dataframe_copy['iso_alpha'].unique()
            )
        )

    def load_more_events(self, no_of_clicks, country):
        list = []
        for _, item in self.getCountrySpecificEvents(no_of_clicks, country).iterrows():
            list.append(
                html.Div([
                    dbc.Row(children=[
                        html.Div(children=[
                            html.Div(children=[
                                html.Div(children=[
                                    html.Div(children=[
                                        html.H6([
                                            html.I(className="fa fa-link",
                                                   style={'color': 'lightblue'}),
                                            html.A(
                                                item['event_title'],
                                                href=item['source_link'],
                                                target="_blank",
                                                style={'text-decoration': 'none'}, className="mb-0")
                                        ]),
                                        html.Span(item['created_date'].strftime(
                                            "%b %d, %Y"), style={'font-size': '10px'})
                                    ], className="ms-2 c-details")
                                ], className="d-flex flex-row align-items-center")
                            ], className="d-flex justify-content-between")
                        ], className="detail-page-card mb-2"),
                    ]),
                    dbc.Row([
                        html.Div(children=[
                            html.P(
                                html.U(
                                    html.B(
                                        'Description'
                                    )
                                )
                            ),
                            html.P(item['event_description'])
                        ])
                    ]),
                    dbc.Row([
                        dbc.Col([
                            html.P(
                                html.B("Landslide Category")
                            ),
                            html.Span(item['landslide_category2'])
                        ], width={"size": 3}, style={'border': '1px solid', 'border-radius': '15px', 'padding': '17px'}),
                        dbc.Col([
                            html.P(
                                html.B("Landslide Trigger")
                            ),
                            html.Span(item['landslide_trigger2'])
                        ], width="2", style={'border': '1px solid', 'border-radius': '15px', 'padding': '17px'}),
                        dbc.Col([
                            html.P(
                                html.B("Landslide Size")
                            ),
                            html.Span(item['landslide_size2'])
                        ], width="2", style={'border': '1px solid', 'border-radius': '15px', 'padding': '17px'}),
                        dbc.Col([
                            html.P(
                                html.B("Fatality Count")
                            ),
                            html.Span(item['fatality_count'])
                        ], width="2", style={'border': '1px solid', 'border-radius': '15px', 'padding': '17px'}),
                        dbc.Col([
                            html.P(
                                html.B("Injury Count")
                            ),
                            html.Span(item['injury_count'] if (
                                item['injury_count'] > 1) else 0)
                        ], width={"size": 2}, style={'border': '1px solid', 'border-radius': '15px', 'padding': '17px'})
                    ], style={'text-align': 'center', 'display': 'flex', 'justify-content': 'space-around'}),
                    dbc.Row([
                        dbc.Col([
                            html.P(
                                html.B("Admin Division Name")
                            ),
                            html.Span(item['admin_division_name'])
                        ], width={"size": 4}, style={'border': '1px solid', 'border-radius': '15px', 'padding': '17px'}),
                        dbc.Col([
                            html.P(
                                html.B("Admin Division Population")
                            ),
                            html.Span(item['admin_division_population'])
                        ], width={"size": 4}, style={'border': '1px solid', 'border-radius': '15px', 'padding': '17px'}),
                    ], style={'text-align': 'center', 'margin-top': '30px', 'display': 'flex', 'justify-content': 'space-around', 'margin-bottom': '20px'})
                ], className="detail-section-item")
            )

        return html.Div(children=list)

    def getCountrySpecificEvents(self, clicks, country):
        skip = clicks * 10
        take = skip + 10
        __df = pd.read_excel(
            "./assets/data/glc.xlsx", "glc_new_columns")
        __temp_df = __df.loc[(__df['iso_alpha'] == country.upper()) & (
            __df['year'] >= 2007)]
        __countries_index = __temp_df.index.tolist()
        indexes = __countries_index[skip:take]
        df = __temp_df[__temp_df.index.isin(indexes)]
        print(df)
        return df

    def get_incident_data_by_country(self, sort_country_list_value):
        record = pd.DataFrame()
        countries = self.dataframe_copy.groupby(
            ['country_name', 'iso_alpha'])
        record['FatalityCount'] = countries['fatality_count'].sum()
        record['InjuriesCount'] = countries['injury_count'].sum()
        record.reset_index(inplace=True)

        if sort_country_list_value == 'fatality_count':
            return record.sort_values(by=['FatalityCount'], ascending=False)

        if sort_country_list_value == 'injury_count':
            return record.sort_values(by=['InjuriesCount'], ascending=False)
        return record

    def filter_data(self, years, categories, landslide_size, selected_countries):
        self.dataframe_copy = self.original_dataframe.loc[(
            self.original_dataframe['year'].isin(
                list(
                    range(years[0], years[1] + 1)
                )
            )
        )]

        if categories is not None and len(categories) != 0:
            self.dataframe_copy = self.dataframe_copy.loc[(
                self.dataframe_copy['landslide_trigger'].isin(categories))]

        if landslide_size is not None and len(landslide_size) != 0:
            self.dataframe_copy = self.dataframe_copy.loc[(
                self.dataframe_copy['landslide_size'].isin(landslide_size))]

        if selected_countries is not None and len(selected_countries) != 0:
            self.dataframe_copy = self.dataframe_copy.loc[(
                self.dataframe_copy['iso_alpha'].isin(selected_countries))]

    def get_states_data(self):
        deaths = self.dataframe_copy.groupby(
            ['country_name'])['fatality_count'].sum()
        countries_df = pd.concat(deaths, axis=1)
        return countries_df

    def get_years_timeline(self):
        """
        returning accident and fatals years timeline.
        """
        timeline_df = pd.DataFrame()
        timeline_df['Total_Events_Occured'] = self.dataframe_copy['year'].value_counts()
        timeline_df['Deaths'] = self.dataframe_copy.groupby(['year'])[
            'fatality_count'].sum()
        timeline_df['Injuries'] = self.dataframe_copy.groupby('year')[
            'injury_count'].sum()
        return timeline_df

    @staticmethod
    def read_data(file, extension, sheet_name=0):
        a_df = pd.DataFrame()
        path = "./assets/data/" + file + extension
        temp_df = pd.read_excel(path, sheet_name=sheet_name)
        a_df = a_df.append(temp_df, ignore_index=True)
        return a_df
