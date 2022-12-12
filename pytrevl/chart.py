import yaml

from typing import List

from pytrevl.api.x_middle import X_Middle
from pytrevl.trevl_code_generator import TrevlCodeGenerator
from pytrevl.render import IpythonHC


class Chart:
    '''
    Chart parent class
    '''
        
    def get_json(self) -> dict:
        trevl_code_generator = TrevlCodeGenerator(self)
        yaml_code = trevl_code_generator.get_trevl()
        return yaml_code
    
    def get_yaml(self) -> str:
        trevl_code_generator = TrevlCodeGenerator(self)
        trevl_code = trevl_code_generator.get_trevl()
        yaml_code = yaml.safe_dump(trevl_code)
        print(yaml_code)

    def show(self):
        x_middle_api = X_Middle(self)
        chart = x_middle_api.get_chart()
        render = IpythonHC(chart)
        return render

    def get_data(self) -> list:
        x_middle_api = X_Middle(self)
        data = x_middle_api.get_data()
        return data
