'''
Import modules to shorten import path to use i.e.:

pytrevl.Dashboard()

instead of

pytrevl.dashboard.Dashboard()
'''

from .dashboard import Dashboard
from .components import PieChart, BarChart, LineChart


# Version and Author

__version__ = '0.0.2'
__author__ = 'Trendence Institut'