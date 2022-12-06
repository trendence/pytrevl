from highcharts import Highchart
import yaml

from pytrevl.api.x_middle import X_Middle
from pytrevl.trevl_code_generator import Trevl_Code_Generator

class Chart:
    '''
    Chart parent class
    '''
    def get_trevl(self) -> str:
        trevl_code_generator = Trevl_Code_Generator(self)
        trevl_code = trevl_code_generator.create_trevl()
        return trevl_code
        
    def get_yaml(self) -> dict:
        trevl_code_generator = Trevl_Code_Generator(self)
        yaml_code = trevl_code_generator.create_yaml()
        return yaml_code
    
    def get_trevl(self) -> str:
        trevl_code_generator = Trevl_Code_Generator(self)
        yaml_code = trevl_code_generator.create_yaml()
        trevl_code = yaml.safe_dump(yaml_code)
        print(trevl_code)

    def show(self) -> Highchart:
        x_middle_api = X_Middle(self)
        chart = x_middle_api.get_chart()
        return chart

    def get_data(self) -> list:
        x_middle_api = X_Middle(self)
        data = x_middle_api.get_data()
        return data
