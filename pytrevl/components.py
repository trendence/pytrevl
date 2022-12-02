'''
Components module handling Charts and Chart-Visualization
'''

import plotly.express as px
import pandas as pd
from highcharts import Highchart

from pytrevl.api.cube import Cube
from pytrevl.api.x_middle import X_Middle
from pytrevl.trevl_code_generator import Trevl_Code_Generator


class PieChart():
    '''
    PieChart component
    '''
    def __init__(self, id: str, cube: str, title: str, x: list, y: list, filters: dict = {}):
        self.id = id
        self.title = title
        self.cube = cube
        self.x = x
        self.y = y
        self.name = x
        self.filters = filters
        self.type = "pie"

    def get_trevl(self) -> str:
        trevl_code_generator = Trevl_Code_Generator(self)
        trevl_code = trevl_code_generator.create_trevl()
        return trevl_code

    def show(self) -> Highchart:
        x_middle_api = X_Middle(self)
        chart = x_middle_api.get_chart()
        return chart
            

'''
    #Old Cube integration

    def show(self) -> None:
        data = self.get_data()
        fig = px.pie(data, values=self.y, names=self.x, title=self.title)
        fig.show()

    def get_data(self) -> pd.DataFrame:
        cube = Cube(
            x = self.x,
            y = self.y,
            cube = self.cube,
            filters = self.filters)
        cube.connect()
        cube_data = cube.get_data()
        return cube_data

'''

class BarChart():
    '''
    BarChart component
    '''
    def __init__(self, id: str, cube: str, title: str, x: list, y: list, filters: dict = {}, orientation: str = "h"):
        self.id = id
        self.title = title
        self.cube = cube
        self.x = x
        self.y = y
        self.name = x
        self.filters = filters
        self.orientation = orientation
        self.type = "column"

    def get_trevl(self) -> str:
        trevl_code_generator = Trevl_Code_Generator(self)
        trevl_code = trevl_code_generator.create_trevl()
        return trevl_code

    def show(self) -> Highchart:
        x_middle_api = X_Middle(self)
        chart = x_middle_api.get_chart()
        return chart
    

'''
    # Old Cube integration

    def show(self) -> None:
        data = self.get_data()
        fig = px.bar(data, x=self.x, y=self.y, title=self.title, orientation=self.orientation)
        fig.show()

    def get_data(self) -> pd.DataFrame:
        cube = Cube(
            x = self.x,
            y = self.y,
            cube = self.cube,
            filters = self.filters)
        cube.connect()
        cube_data = cube.get_data()
        return cube_data
'''