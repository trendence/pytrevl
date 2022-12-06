'''
Handling X-Middle connections
'''

import requests
from highcharts import Highchart
import yaml
import os
import pandas as pd

from pytrevl.component import Component
from pytrevl.trevl_code_generator import Trevl_Code_Generator

class X_Middle:
    '''
    X-Middle api
    '''
    def __init__(self, component: Component):
        self.component = component
    
    def get_chart(self) -> Highchart:
        # Create HTTP Authentification with X-Middle API
        http_auth = self.authenticate()

        # Create a YAML Object from TREVL Code
        yaml_object = self.get_yaml_object_without_trevl()

        # Post and receive request to X-Middle API
        x_middle_response = self.post_request(yaml_object=yaml_object, http_auth=http_auth)
        
        # Extract JSON information from post request response
        self.highcharts_json = x_middle_response.json()["components"][0]

        # Create Highchart object
        self.highchart = Highchart()

        # Extracts x, y and name data from json and writes it to highchart object
        self.define_x_and_y_data()

        # Set title of highchart object
        self.highchart.set_options("title", {'text': self.component.title})

        return self.highchart

    def get_data(self) -> list:
        # Create HTTP Authentification with X-Middle API
        http_auth = self.authenticate()

        # Create a YAML Object from TREVL Code
        yaml_object = self.get_yaml_object_without_trevl()

        # Post and receive request to X-Middle API
        x_middle_response = self.post_request(yaml_object=yaml_object, http_auth=http_auth)
        
        # Extract JSON information from post request response
        self.highcharts_json = x_middle_response.json()["components"][0]

        # Create Highchart object
        self.highchart = Highchart()

        # Extracts x, y and name data from json and writes it to highchart object
        data = self.define_x_and_y_data()

        df = pd.DataFrame(data, columns=["X", "Y"])
        df = df.set_index("X")

        return df

    def authenticate(self):
        x_username = os.getenv("X_MIDDLE_USERNAME")
        x_password = os.getenv("X_MIDDLE_PASSWORD")
        http_auth = requests.auth.HTTPBasicAuth(x_username, x_password)
        return http_auth

    def get_yaml_object(self):
        travel_code_generator = Trevl_Code_Generator(self.component)
        trevl_code = travel_code_generator.create_trevl()
        yaml_code = yaml.safe_load(trevl_code)
        return yaml_code

    def get_yaml_object_without_trevl(self):
        travel_code_generator = Trevl_Code_Generator(self.component)
        yaml_code = travel_code_generator.create_yaml()
        return yaml_code

    def post_request(self, yaml_object, http_auth):
        base_url = os.getenv("X_MIDDLE_BASEURL")
        req = {"abstractConfig": yaml_object,}
        response = requests.post(f'{base_url}/dashboards', auth=http_auth, json=req)
        
        if "error" in response.json():
            raise Exception("X-MIDDLE API ERROR RESPONSE: " + response.json()["error"] + "  REQUEST: " + str(req))
        
        return response

    def define_x_and_y_data(self):

        # Create lists for data and category names
        data = []
        category_names = []

        if self.component.type == "pie":
            '''
            If component type is 'pie' then x value will be called 'name' upon return from X-Middle
            '''
            for data_points in self.highcharts_json["series"][0]["data"]:
                data.append([data_points["name"], data_points["y"]])

        elif self.component.type == "column":
            '''
            If component type is 'column' then x value is the names of options/catagories
            '''
            category_names = self.highcharts_json["xAxis"]["categories"]

            for counter, value in enumerate(self.highcharts_json["series"][0]["data"]):
                data.append([category_names[counter],value[1]])

            self.highchart.set_options("xAxis", {'categories': category_names})

        elif self.component.type == "line":

            for data_points in self.highcharts_json["series"][0]["data"]:
                data.append([data_points[0], data_points[1]])

        else:
            raise Exception(f"Component type {self.component.type} is not defined.")

        # Add data to highcharts object
        self.highchart.add_data_set(data, self.component.type)

        return data