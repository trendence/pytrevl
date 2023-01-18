'''
Import modules to shorten import path to use i.e.:

pytrevl.Dashboard()

instead of

pytrevl.dashboard.Dashboard()
'''
# Version and Author

__version__ = '0.2.1'
__author__ = 'Trendence Institut'

from .charts import (
    ColumnChart,
    DonutChart,
    LineChart,
    PieChart,
    BarChart,
    StackedBarChart,
    CustomChart
)
from .components import (
    ScoreComponent,
)
from .cube import CubeQuery, Computed, Filter
from .dashboard import Dashboard
