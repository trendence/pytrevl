'''
Components module handling Charts and Chart-Visualization
'''

from highcharts import Highchart
from pytrevl.chart_parent_class import Chart

from pytrevl.api.x_middle import X_Middle
from pytrevl.trevl_code_generator import Trevl_Code_Generator

class PieChart(Chart):
    '''
    PieChart component
    '''
    def __init__(self, id: str, cube: str, title: str, measure: list, dimension: list, filters: dict = {}):
        self.id = id
        self.title = title
        self.cube = cube
        self.measure = measure
        self.dimension = dimension
        self.name = measure
        self.filters = filters
        self.type = "pie"

class BarChart(Chart):
    '''
    BarChart component
    '''
    def __init__(self, id: str, cube: str, title: str, measure: list, dimension: list, filters: dict = {}, orientation: str = "h"):
        self.id = id
        self.title = title
        self.cube = cube
        self.measure = measure
        self.dimension = dimension
        self.name = measure
        self.filters = filters
        self.orientation = orientation
        self.type = "column"

class LineChart(Chart):
    '''
    LineChart component
    '''
    def __init__(self, id: str, cube: str, title: str, measure: list, dimension: list, filters: dict = {}):
        self.id = id
        self.title = title
        self.cube = cube
        self.measure = measure
        self.dimension = dimension
        self.name = measure
        self.filters = filters
        self.type = "line"