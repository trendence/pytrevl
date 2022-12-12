
from typing import List

from pytrevl.chart_parent_class import Chart
from pytrevl.cube import Cube
from pytrevl.style import Style

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