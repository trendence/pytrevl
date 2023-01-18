from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING
from uuid import uuid4

from .api import xmiddle
from .notebook import render_component
from .utils import insert, merge, AsSomethingMixin, MergeWithBase

if TYPE_CHECKING:
    from .api import XMiddleService
    from .cube import BaseCubeQuery


class BaseComponent(AsSomethingMixin):
    """Base class for all components

    This class provides that 
    - instances have an ``id`` attribute.
    - can be serialized to JSON and YAML (:method:`serialize()` must be
      implemented in sub-classes).
    - can be composed into dashboards.
    """
    id: str
    def __init__(self, id: Optional[str]=None):
        self.id = id or f'{type(self).__name__}-{uuid4().hex}'

    def __str__(self):
        return f'<{type(self).__name__} id:{self.id}>'

    def __add__(self, other):
        if isinstance(other, BaseComponent):
            return Dashboard(components=[self, other])
        return NotImplemented

class QueryingKwargsComponent(BaseComponent, metaclass=MergeWithBase):
    """Base class for creating component from kwargs with easy composition of sub-classes.

    This base class can be used for all TREVL-components that have the following structure::

        id: "component-id"
        type: "component-type"
        queries:
          - <cube-query-1>
          # ...
        display:
          # ...
    """
    type: str
    _default: dict ={}
    _kw_paths: dict[str, str] = {}

    def __init__(self, query: 'BaseCubeQuery', id: Optional[str]=None, **kwargs):
        super().__init__(id)
        self.query = query
        self.kwargs = kwargs
        self.custom = {}

    def _filter_locals(self, l, filtered=None):
        """Internal helper to be used to update ``self.kwargs``.

        Should be used in sub-classes' ``__init__()`` like so::

            class SubComponent(QueryingKwargsComponent):
                def __init__(self, a, b=None, **kwargs):
                    if b is None:
                        # initialize b
                    super().__init__(
                    **self._filter_locals(locals()),
                    **kwargs,
                )
        """
        filtered = filtered or {'kwargs', 'self', '__class__'}
        return {
            k: v for k, v in l.items() if k not in filtered and v is not None
        }

    def __setitem__(self, path, value):
        self.custom = insert(value, path, self.custom)

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
            'type': self.type,
            'id': self.id,
            'display': display,
            'queries': queries,
        }

    def show(self, *args, **kwargs):
        return Dashboard(components=[self]).show(*args, **kwargs)

    def render(self, *args, **kwargs):
        resp = Dashboard(components=[self]).render(*args, **kwargs)
        return resp["components"][0]


@dataclass
class Dashboard(AsSomethingMixin):
    description: str = ""
    components: list = field(default_factory=list)

    def serialize(self):
        data = {}
        # Add description before components to have them at the top of the
        # serialized object.
        if self.description:
            data['description'] = self.description

        data['components'] = [c.serialize() for c in self.components]

        return data

    def __add__(self, other):
        if isinstance(other, Dashboard):
            return Dashboard(self.description, self.components + other.components)
        elif isinstance(other, BaseComponent):
            return Dashboard(self.description, self.components + [other])

    def __radd__(self, other):
        if isinstance(other, Dashboard):
            return Dashboard(self.description, other.components + self.components)
        elif isinstance(other, BaseComponent):
            return Dashboard(self.description, [other] + self.components)

    def __iadd__(self, other):
        if isinstance(other, Dashboard):
            self.components.extend(other.components)
            return self
        elif isinstance(other, BaseComponent):
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

        iframes = [render_component(comp) for comp in body['components']]
        return HTML('\n'.join(iframes))
