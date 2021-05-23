from datetime import timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import plotly.express as px


class WorldMap:
    def __init__(self, data_processing):
        self.data = data_processing

    def world_map(self, selected_countries, country_iso_code, show_map):
        if len(show_map) != 0 and show_map[0] == 'wmap':
            print('If')
            scope = 'world'
            if (country_iso_code is not None) and (country_iso_code != 'world'):
                continent = self.data.getRegionInfoWithCountryName(
                    country_iso_code)
                scope = 'world'
                if continent.lower() in ['usa', 'europe', 'asia', 'africa', 'north america', 'south america']:
                    scope = continent.lower()

            df = self.data.dataframe_copy
            __temp_df = pd.DataFrame()
            df_after_groupby = df.groupby(['iso_alpha', 'country_name'])
            __temp_df['FatalityCount'] = df_after_groupby['fatality_count'].sum()
            __temp_df['InjuryCount'] = df_after_groupby['injury_count'].sum()
            __temp_df['TotalEvents'] = df_after_groupby.size()

            if selected_countries is not None and len(selected_countries) != 0:
                df_after_groupby = df[df['iso_alpha'].isin(selected_countries)].groupby([
                    'iso_alpha', 'country_name'])
                __temp_df['FatalityCount'] = df_after_groupby['fatality_count'].sum()
                __temp_df['InjuryCount'] = df_after_groupby['injury_count'].sum()
                __temp_df['TotalEvents'] = df_after_groupby.size()

            yourdata = __temp_df.reset_index()

            print(yourdata)

            fig = px.choropleth(yourdata, locations="iso_alpha",
                                color="FatalityCount",
                                hover_name="country_name",
                                hover_data=['TotalEvents',
                                            'FatalityCount', 'InjuryCount'],
                                color_continuous_scale=[
                                    "#6B8E23",
                                    "#556B2F",
                                    "#9ACD32",
                                    "#FFFF00",
                                    "#FF8C00",
                                    "#FA8072",
                                    "#E9967A",
                                    "#F08080",
                                    "#CD5C5C",
                                    "#FF7F50",
                                    "#FF6347",
                                    "#FF0000",
                                    "#DC143C",
                                    "#B22222",
                                    "#A52A2A",
                                    "#8B0000",
                                ],
                                scope=scope)


            fig.update_layout(
                margin={'r': 0, 't': 0, 'l': 0, 'b': 0},
                coloraxis_colorbar={
                    'title': 'Fatality Count',
                    'tickvals': [0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000]
                }
            )

            fig.update_layout(
                mapbox_style="open-street-map",
                hoverlabel=dict(
                    bgcolor="white",
                    font_size=16,
                    font_family="Rockwell"
                )
            )

            return fig
        else:
            print('else')
            first_df = self.data.dataframe_copy
            
            fig = px.scatter_mapbox(
                first_df,
                lat="latitude",
                lon="longitude",
                hover_name="country_name",
                hover_data={"fatality_count", "injury_count", "event_title","landslide_trigger2", "landslide_category2"},
                color_discrete_sequence=["fuchsia"],
                zoom=0
            )

            fig.update_traces(
                marker=dict(size=7, color="#DC143C"),
                selector=dict(mode='markers')
            )

            fig.update_layout(
                mapbox_style="open-street-map",
                hoverlabel=dict(
                    bgcolor="white",
                    font_size=16,
                    font_family="Rockwell"
                )
            )

            fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

            return fig

    def valid_latlon(s):
        return (s <= 90) or (s >= -90)

    def detail_country_map(self, clicks, country):
        dataframe = self.data.getCountrySpecificEvents(clicks, country)
        
        fig = px.scatter_mapbox(
            dataframe,
            lat="latitude",
            lon="longitude",
            hover_name="country_name",
            hover_data={"event_title", "fatality_count", "injury_count"},
            color_discrete_sequence=["fuchsia"],
            zoom=3,
            height=450
        )

        fig.update_traces(
            marker=dict(size=20, color="#DC143C"),
            selector=dict(mode='markers')
        )

        fig.update_layout(
            mapbox_style="open-street-map",
            hoverlabel=dict(
                bgcolor="white",
                font_size=16,
                font_family="Rockwell"
            )
        )
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

        return fig
