'''
Components module handling Charts and Chart-Visualization
'''

from pytrevl.chart_parent_class import Chart

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