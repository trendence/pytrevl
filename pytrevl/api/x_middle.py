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

    def authenticate(self):
        x_username = os.getenv("X_MIDDLE_USERNAME")
        x_password = os.getenv("X_MIDDLE_PASSWORD")
        http_auth = requests.auth.HTTPBasicAuth(x_username, x_password)
        return http_auth

    def post_request(self, yaml_object, http_auth):
        base_url = os.getenv("X_MIDDLE_BASEURL")
        req = {"abstractConfig": yaml_object,}
        response = requests.post(f'{base_url}/dashboards', auth=http_auth, json=req)
        
        if "error" in response.json():
            raise Exception("X-MIDDLE API ERROR RESPONSE: " + response.json()["error"] + "  REQUEST: " + str(req))
        
        return response
    
    def get_chart(self) -> dict:
        # Authenticate with the X-Middle API
        http_auth = self.authenticate()

        # Create a YAML object from the TREVL code
        yaml_object = self.get_trevl()

        # Post a request to the X-Middle API and receive a response
        x_middle_response = self.post_request(yaml_object=yaml_object, http_auth=http_auth)
        
        # Extract the JSON information from the response
        self.highcharts_json = x_middle_response.json()["components"][0]

        return self.highcharts_json

    def get_trevl(self):
        travel_code_generator = TrevlCodeGenerator(self.component)
        trevl_code = travel_code_generator.get_trevl()
        return trevl_code

    def get_data(self):
        # Authenticate with the X-Middle API
        http_auth = self.authenticate()

        # Create a YAML object from the TREVL code
        yaml_object = self.get_trevl()

        # Post a request to the X-Middle API and receive a response
        x_middle_response = self.post_request(yaml_object=yaml_object, http_auth=http_auth)
        
        # Extract JSON information from post request response
        self.highcharts_json = x_middle_response.json()["components"][0]

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

        elif self.component.type == "line":

            for data_points in self.highcharts_json["series"][0]["data"]:
                data.append([data_points[0], data_points[1]])

        else:
            raise Exception(f"Component type {self.component.type} is not defined.")
       
        # Create DataFrame
        df = pd.DataFrame(data, columns=["X", "Y"])
        df = df.set_index("X")

        return df