
from typing import List
import yaml

from pytrevl.chart import Chart
from pytrevl.cube import Cube
from pytrevl.style import Style

from pytrevl.api.x_middle import X_Middle
from pytrevl.render import IpythonHC

class PieChart(Chart):
    '''
    PieChart component
    '''
    def __init__(self, id: str, cube: Cube, measure: str, dimension: str, filters: List, style: Style):
        self.id = id
        self.cube = cube
        self.measure = measure
        self.dimension = dimension
        self.filters = filters
        self.style = style
        self.type = "pie"

class DonutChart(Chart):
    '''
    DonutChart component
    '''
    def __init__(self, id: str, cube: Cube, measure: str, dimension: str, filters: List, style: Style):
        self.id = id
        self.cube = cube
        self.measure = measure
        self.dimension = dimension
        self.filters = filters
        self.style = style
        self.type = "pie"

class BarChart(Chart):
    '''
    BarChart component
    '''
    def __init__(self, id: str, cube: Cube, measure: str, dimension: str, filters: List, style: Style):
        self.id = id
        self.cube = cube
        self.measure = measure
        self.dimension = dimension
        self.filters = filters
        self.style = style
        self.type = "column"

class LineChart(Chart):
    '''
    LineChart component
    '''
    def __init__(self, id: str, cube: Cube, measure: str, dimension: str, filters: List, style: Style):
        self.id = id
        self.cube = cube
        self.measure = measure
        self.dimension = dimension
        self.filters = filters
        self.style = style
        self.type = "line"

class CustomChart:
    def __init__(self, json: dict):
        self.json = json
        self.type = ""

    def get_json(self) -> dict:
        return self.json
    
    def get_yaml(self) -> str:
        yaml_code = yaml.safe_dump(self.json)
        print(yaml_code)

    def show(self):
        x_middle_api = X_Middle(self)
        chart = x_middle_api.get_chart(json=self.json)
        render = IpythonHC(chart)
        return render

    def get_data(self) -> list:
        x_middle_api = X_Middle(self)
        data = x_middle_api.get_data(json=self.json)
        return data