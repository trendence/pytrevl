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
    BarChart,
    ColumnChart,
    CustomChart,
    DonutChart,
    LineChart,
    PieChart,
    StackedBarChart,
)
from .components import (
    ScoreComponent,
)
from .cube import (
    Computed,
    CubeQuery,
    Filter,
    MultiCubeQuery,
    SqlQuery,
)
from .dashboard import Dashboard
