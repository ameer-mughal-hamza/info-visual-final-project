import dash_html_components as html
import dash_core_components as dcc
from components.list_item import ListItem

class List:
    def __init__(self, data_processing):
        self.listItem = ListItem(data_processing)

    def generate_list(self, sort_country_list_value):
        listItems = self.listItem.generateItems(sort_country_list_value)
        return html.Div(listItems, style={'padding': '0 20px 0 20px'})
