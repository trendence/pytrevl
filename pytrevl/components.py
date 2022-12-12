'''
Components module handling Charts and Chart-Visualization

This code defines a Components module, which provides classes
for creating different types of charts. The PieChart, DonutChart,
BarChart, and LineChart classes all inherit from the Chart parent
class, which is defined in the Chart_Parent_Class module. Each of
these classes provides a constructor for creating a chart with specific
properties, such as the chart title, the data cube to use, the measure
and dimension to plot, and any filters to apply. Each class also
specifies the type of chart to be generated, such as a pie chart, donut chart, bar chart, or line chart.
'''
from typing import List

from pytrevl.chart_parent_class import Chart
from pytrevl.cube import Cube
from pytrevl.filter import Filter
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