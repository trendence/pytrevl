'''
Import modules to shorten import path to use i.e.:

pytrevl.Dashboard()

instead of

pytrevl.dashboard.Dashboard()
'''

from .dashboard import Dashboard
from .components import PieChart, BarChart, LineChart, DonutChart, CustomChart
from .cube import Cube
from .filter import Filter
from .style import Style
from .api.cube_query import CubeQuery


# Version and Author

__version__ = '0.2.1'
__author__ = 'Trendence Institut'