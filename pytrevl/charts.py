from dataclasses import dataclass, field
from typing import Optional,TYPE_CHECKING
from uuid import uuid4

from .api import xmiddle
from .notebook import chart_iframe
from .utils import insert, merge, AsSomethingMixin

if TYPE_CHECKING:
    from .api import XMiddleService
    from .cube import CubeQuery

class _MergeWithBase(type):
    """Helper to merge ``_kw_paths`` and ``_default`` of all parent classes
    into ``kw_paths`` and ``default``, respectively.
    """
    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Merge the kw_paths mapping
        cls.kw_paths = {}
        for c in reversed(cls.mro()):
            cls.kw_paths.update(getattr(c, '_kw_paths', {}))

        # Merge the default config
        cls.default = {}
        for c in reversed(cls.mro()):
            cls.default = merge(cls.default, getattr(c, '_default', {}))


class BaseChart(AsSomethingMixin, metaclass=_MergeWithBase):
    """Base class for TREVL charts.

    This class helps building the ``display`` part of a TREVL chart. It
    requires a :class:`CubeQuery` instance and accepts optional keyword
    arguments. The mapping between keyword arguments and the attributes in
    the ``display`` part of the TREVL chart is defined in :attr:`_kw_paths`.
    The default ``display`` document is denfined in :attr:`_default`.

    The ``display`` properties can be controlled via

    1. keyword arguments of the constructor, e.g.::

        >>> # query = ...
        >>> chart = BaseClass(query, title="Chart title", x=query['dimension'], y=query['measure'])

    2. Setting "custom" attributes, e.g. setting the ``color`` attribute::

        >>> chart['series.0.color'] = '#ff0000'

    Subclasses can override settings made in the base class's
    :attr:`_default` and :attr:`_kw_paths`.  The results are assigned to
    :attr:`default` and :attr:`kw_paths` via the meta-class
    :class:`MergeWithBase`.
    """

    _default: dict = {
        'chart': {
            'type': 'line',
        },
    }
    _kw_paths: dict[str, str] = {
        'title': 'title.text',
        # Series definition
        'color': 'series.0.color',
        'name': 'series.0.name',
        'x': 'series.0.x',
        'y': 'series.0.y',
        'z': 'series.0.z',
    }

    def __init__(self, query: 'CubeQuery', id: Optional[str]=None, **kwargs):
        self.query = query
        self.id = id or f'{type(self).__name__}-{uuid4().hex}'
        self.kwargs = kwargs
        self.custom = {}

    def __str__(self):
        return f'<{type(self).__name__} id:{self.id}>'

    def __add__(self, other):
        if isinstance(other, BaseChart):
            return Dashboard(components=[self, other])
        return NotImplemented

    def __setitem__(self, path, value):
        self.custom = insert(path, value)

    def _filter_locals(self, l, filtered=None):
        filtered = filtered or {'kwargs', 'self', '__class__'}
        return {
            k: v for k, v in l.items() if k not in filtered
            }

    def serialize(self):
        dynamic = {}
        for name, value in self.kwargs.items():
            if name not in self.kw_paths:
                raise ValueError(f'{type(self).__name__} received unknown keyword argument {name!r}. Supported arguments are: {", ".join(sorted(self.kw_paths))}')
            dest = self.kw_paths[name]
            dynamic = insert(value, dest, dynamic)

        display = self.default
        display = merge(display, dynamic)
        display = merge(display, self.custom)

        queries = [self.query.serialize()]
        return {
            'type': 'chart',
            'id': self.id,
            'display': display,
            'queries': queries,
        }

    def show(self, *args, **kwargs):
        return Dashboard(components=[self]).show(*args, **kwargs)

    def render(self, *args, **kwargs):
        return Dashboard(components=[self]).render(*args, **kwargs)


class ColumnChart(BaseChart):
    _default = {
        'chart': {
            'type': 'column',
        },
    }
    _kw_paths = {
        'category': 'series.0.x',
        'height': 'series.0.y',
        }
    def __init__(self, query, category=None, height=None, **kwargs):
        if category is None:
            category = query[query.dimensions[0]]
        if height is None:
            height = query[query.measures[0]]

        super().__init__(
            **self._filter_locals(locals()),
            **kwargs,
        )


class PieChart(BaseChart):
    _default = {
        'chart': {
            'type': 'pie',
        },
    }
    def __init__(self, query, name, y, **kwargs):
        super().__init__(
            **self._filter_locals(locals()),
            **kwargs,
        )


class DonutChart(PieChart):
    _kw_paths = {
        'inner': 'series.0.innerSize',
        'outer': 'series.0.size',
    }

    def __init__(self, query, y, name, inner='30%', outer='60%', **kwargs):
        super().__init__(
            **self._filter_locals(locals()),
            **kwargs,
        )


@dataclass
class Dashboard(AsSomethingMixin):
    description: str = ""
    components: list = field(default_factory=list)

    def serialize(self):
        data = {
            'parameters': [],
        }
        # Add description before components to have them at the top of the
        # serialized object.
        if self.description:
            data['description'] = self.description

        data['components'] = [c.serialize() for c in self.components]

        return data

    def __add__(self, other):
        if isinstance(other, Dashboard):
            return Dashboard(self.description, self.components + other.components)
        elif isinstance(other, BaseChart):
            return Dashboard(self.description, self.components + [other])

    def __radd__(self, other):
        if isinstance(other, Dashboard):
            return Dashboard(self.description, other.components + self.components)
        elif isinstance(other, BaseChart):
            return Dashboard(self.description, [other] + self.components)

    def __iadd__(self, other):
        if isinstance(other, Dashboard):
            self.components.extend(other.components)
            return self
        elif isinstance(other, BaseChart):
            self.components.append(other)
            return self
        return NotImplemented

    def render(self, api_client: 'XMiddleService'=None, **kwargs):
        if api_client is None:
            api_client = xmiddle()

        return api_client(self, **kwargs)

    def show(self, *args, **kwargs):
        from IPython.display import HTML
        body = self.render(*args, **kwargs)

        iframes = [chart_iframe(comp) for comp in body['components']]
        return HTML('\n'.join(iframes))
