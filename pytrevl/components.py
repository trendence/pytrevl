from typing import Optional, TYPE_CHECKING

from .dashboard import QueryingKwargsComponent
from .utils import MergeWithBase

if TYPE_CHECKING:
    from .cube import BaseCubeQuery


class ScoreComponent(QueryingKwargsComponent):
    type = 'score'
    _default: dict = {}
    _kw_paths: dict = {
        'column': 'column',
        'digits': 'digits',
        'text': 'text',
        'unit': 'unit',
    }

    def __init__(self,
                 query: 'BaseCubeQuery', 
                 id: Optional[str]=None,
                 column: Optional[str]=None,
                 digits: Optional[int]=None,
                 text: Optional[str]=None,
                 unit: Optional[str]=None,
                 **kwargs,
             ):
        if column is None:
            column = query[query.measures[0]]

        super().__init__(
            **self._filter_locals(locals()),
            **kwargs,
        )
