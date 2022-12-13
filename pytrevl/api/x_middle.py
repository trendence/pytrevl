import requests
import os
import pandas as pd

from pytrevl.component import Component
from pytrevl.trevl_code_generator import TrevlCodeGenerator

class X_Middle:
    '''
    X-Middle api
    '''
    def __init__(self, component: Component):
        self.component = component
        self.http_auth = self.authenticate()

    def authenticate(self):
        x_username = os.getenv("X_MIDDLE_USERNAME")
        x_password = os.getenv("X_MIDDLE_PASSWORD")
        http_auth = requests.auth.HTTPBasicAuth(x_username, x_password)
        return http_auth

    def post_request(self, chart_json):
        base_url = os.getenv("X_MIDDLE_BASEURL")
        req = {"abstractConfig": chart_json,}
        response = requests.post(f'{base_url}/dashboards', auth=self.http_auth, json=req)
        
        if "error" in response.json():
            raise Exception("X-MIDDLE API ERROR RESPONSE: " + response.json()["error"] + "  REQUEST: " + str(req))
        
        return response
    
    def get_chart(self, json: dict = None) -> dict:
        # Create a YAML object from the TREVL code
        if not json:
            chart_json = self.get_trevl()
        else:
            chart_json = json
        # Post a request to the X-Middle API and receive a response
        x_middle_response = self.post_request(chart_json=chart_json)
        
        # Extract the JSON information from the response
        highcharts_json = x_middle_response.json()["components"][0]

        return highcharts_json

    def get_trevl(self):
        travel_code_generator = TrevlCodeGenerator(self.component)
        trevl_code = travel_code_generator.get_trevl()
        return trevl_code

    def get_data(self, json: dict = None):
        # Get Chart JSON from X-Middle
        if not json:
            highcharts_json = self.get_chart()
        else:
            highcharts_json = self.get_chart(json)
            self.component.type = json["components"][0]['display']['chart']['type']
        
        # Create lists for data and category names
        data = []
        category_names = []

        if self.component.type == "pie":
            '''
            If component type is 'pie' then x value will be called 'name' upon return from X-Middle
            '''
            for data_points in highcharts_json["series"][0]["data"]:
                data.append([data_points["name"], data_points["y"]])

        elif self.component.type == "column":
            '''
            If component type is 'column' then x value is the names of options/catagories
            '''
            category_names = highcharts_json["xAxis"]["categories"]

            for counter, value in enumerate(highcharts_json["series"][0]["data"]):
                data.append([category_names[counter],value[1]])

        elif self.component.type == "line":
            '''
            If component type is 'line' then x value is 1st and y ist 2nd in list of data_points
            '''
            for data_points in highcharts_json["series"][0]["data"]:
                data.append([data_points[0], data_points[1]])

        else:
            raise Exception(f"Component type {self.component.type} is not defined.")
       
        # Create DataFrame
        df = pd.DataFrame(data, columns=["X", "Y"])
        df = df.set_index("X")

        return df