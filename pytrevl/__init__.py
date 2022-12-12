'''
Import modules to shorten import path to use i.e.:

pytrevl.Dashboard()

instead of

pytrevl.dashboard.Dashboard()
'''

from .dashboard import Dashboard
from .components import PieChart, BarChart, LineChart, DonutChart
from .cube import Cube
from .filter import Filter
from .style import Style


# Version and Author

__version__ = '0.0.2'
__author__ = 'Trendence Institut'