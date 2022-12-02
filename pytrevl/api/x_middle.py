'''
Handling X-Middle connections
'''

import requests
from highcharts import Highchart
import yaml

from pytrevl.component import Component
from pytrevl.trevl_code_generator import Trevl_Code_Generator

# Get global env variables for SQL - connection


class X_Middle:
    '''
    Cube api
    '''
    def __init__(self, component: Component):
        self.component = component
    
    def get_chart(self) -> Highchart:
        base_url = "https://x-middle.herokuapp.com/api"
        basic = requests.auth.HTTPBasicAuth('x', 'awesomev1z')
        tcg = Trevl_Code_Generator(self.component)
        trevl_code = tcg.create_trevl()
        yaml_code = yaml.safe_load(trevl_code)
        req = {"abstractConfig": yaml_code,}
        response = requests.post(f'{base_url}/dashboards', auth=basic, json=req)
        
        if "Error" in str(response.content):
            raise Exception(response.content)

        options = response.json()["components"][0]

        highchart = Highchart()

        data = []
        category_names = []
        if self.component.type == "pie":
            for x in options["series"][0]["data"]:
                data.append([x["name"], x["y"]])
        else:
            category_names = options["xAxis"]["categories"]
            for counter, value in enumerate(options["series"][0]["data"]):
                data.append([category_names[counter],value[1]])
            highchart.set_options("xAxis", {'categories': category_names})
    
        
        highchart.add_data_set(data, self.component.type) 
        highchart.set_options("title", {'text': self.component.title})
        return highchart