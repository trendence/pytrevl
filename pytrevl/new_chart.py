from copy import deepcopy
from dataclasses import dataclass, field
from itertools import zip_longest
import json
from os import environ
from posixpath import join as url_join
from typing import Optional, Union
from uuid import uuid4

import requests
import yaml

# Helpers
def merge(a, b):
    """Recursively merge 2 data structures.

    ``b`` takes precedence over ``a``.

    Returns
    -------
    merged
        ``a`` recursively merged with ``b``
    """
    if type(a) != type(b):
        raise ValueError(f'Can only merge same typed objects. Got: {type(a)} and {type(b)}')
    if isinstance(a, dict):
        out = {}
        for k in set(a) | set(b):
            if k in a and k in b:
                out[k] = merge(a[k], b[k])
            elif k in a:
                out[k] = deepcopy(a[k])
            else:
                out[k] = deepcopy(b[k])

    elif isinstance(a, list):
        out = []
        for ai, bi in zip_longest(a, b):
            if ai is not None and bi is not None:
                out.append(merge(ai, bi))
            elif ai is not None:
                out.append(deepcopy(ai))
            else:
                out.append(deepcopy(bi))
    else:
        out = b

    return out


def insert(value, path: Union[str, list[str]], container: Optional[Union[dict, list]]=None):
    """Insert ``value`` at ``path`` into ``container``.

    ``container`` is changed **in-place**!

    Paramters
    ---------
    value
        The value to insert.
    path
        The path where to insert ``value``. If a ``str``, it must be
        dot-separated. Numeric strings are interpreted as list-index.
    container
        The container to insert into. If missing or ``None``, a new
        container object is created according to the first part of ``path``:
        If it's a numeric string a `list` is used, otherwise a ``dict``.

    Returns
    -------
    container_or_value
        The updated ``container`` or ``value`` if ``path`` is empty (i.e. at
        the end of recursion).
    """
    if not path:
        return value

    if isinstance(path, str):
        path = path.split('.')

    head, *tail = path
    if head.isdigit():
        if container is None:
            container = []
        if not isinstance(container, list):
            raise ValueError(f'Cannot insert {head!r} into {type(container)}')
        i = int(head)
        if i < len(container):
            container[i] = insert(value, tail, container[i])
        else:
            container.append(insert(value, tail))
    else:
        if container is None:
            container = {}
        if not isinstance(container, dict):
            raise ValueError(f'Cannot insert {head!r} into {type(container)}')
        container[head] = insert(value, tail, container.get(head))
    return container


class MergeWithBase(type):
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



@dataclass
class CubeQuery:
    cube: str
    measures: list[str]
    dimensions: list[str] = field(default_factory=list)
    filters: list = field(default_factory=list)
    computed: list = field(default_factory=list)

    def __getitem__(self, field):
        """Get a reference for `field` in this query."""
        if field in self.measures or field in self.dimensions:
            return f"${self.cube}.{field}"
        if field in {c['name'] for c in self.computed}:
            return f'${field}'
        raise ValueError(f'Field {field!r} not found in query for cube {self.cube}')

    def _prepend_cube(self, fields: list[str]) -> list[str]:
        return [f'{self.cube}.{f}' for f in fields]

    def _serialize_filter(self, f: dict) -> dict:
        ret = deepcopy(f)
        ret['members'] = self._prepend_cube(ret['members'])
        return ret

    def _serialize_computed(self, c: dict) -> dict:
        ret = deepcopy(c)
        ret['arguments'] = {
            dst: f'${self.cube}.{src}'
            for dst, src in ret['arguments'].items()
        }
        return ret

    def serialize(self):
        ret = {
            'measures': self._prepend_cube(self.measures),
        }

        if self.dimensions:
            ret['dimensions'] = self._prepend_cube(self.measures)

        if self.filters:
            ret['filters'] = [self._serialize_filter(f) for f in self.filters]

        if self.computed:
            ret['computed'] = [self._serialize_computed(c) for c in self.computed]
        return ret


query = CubeQuery('cubeName', ['meas1', 'meas2'], ['dim1', 'dim2'])


_xmiddle = None

def xmiddle(*args, **kwargs):
    if not _xmiddle:
        _xmiddle = XMiddleService.from_env(*args, **kwargs)
    return _xmiddle


class XMiddleService:
    """Simple wrapper for x-middle API endpoints.

    Examples
    --------
    >>> # Load configuration from environment
    >>> api = XMiddleService.from_env()
    >>> dashboard = # ...
    >>> # Call API with a dashboard ("rendering")
    >>> api(dashboard)
    {
        components: [ ... ],
        events: [ ... ],
        parameters: { ... },
    }
    """
    def __init__(self, base_url: str, auth_password: Optional[str]=None, auth_username: str="pytrevl"):
        """
        Use :method:`~XMiddleService.from_env` to create an instance using
        configuration from environment variables.

        Parameters
        ----------
        base_url
            The URL of the base of dashboard-API endpoint, i.e. without the
            final ``'dashboards'``.
        auth_password
            The password for HTTP-Basic auth for the API.
        auth_username
            The username for HTTP-Basic auth for the API.
        """
        self.root = url_join(base_url, 'dashboards')
        if auth_password:
            self._session = requests.Session(
                auth=requests.auth.HTTPBasicAuth(auth_username, auth_password)
            )
        else:
            self._session = requests.Session()

    @classmethod
    def from_env(cls, base_url: str="X_MIDDLE_BASEURL", auth_password: str="X_MIDDLE_PASSWORD", **kwargs):
        base_url = environ[base_url]
        auth_password = environ[auth_password]
        return cls(base_url, auth_password, **kwargs)

    def __call__(self, dashboard: "Dashboard", event=None, parameters=None) -> dict:
        """Render a dashboard through the API."""
        body = {
            'abstractDashoboardConfig': dashboard.serialize(),
        }
        if event:
            body['event'] = event
        if parameters:
            body['parameters'] = parameters
        resp = self._session.post(self.root_url, json=body)
        return resp.json()


class AsSomethingMixin:
    """Mixin to render serialized data as JSON and YAML.

    The class must implement :meth:`serialize()` that generates a simple
    data structure that can be serialized as JSON or YAML, i.e. just
    ``list``, ``dict``, and "scalars" (i.e. ``int``, ``str``, ``float``).
    """
    def as_json(self, buf=None, indent=2, **dump_kw):
        """Serialize as JSON.

        Parameters
        ----------
        buf
            If specified, a buffer (e.g. file-like object) to write the JSON
            to.
        indent
            The indentation level, passed to :func:`json.dump`.
        **dump_kw
            Other keyword arguments are passed through to :func:`json.dump`.

        Returns
        -------
        json_or_buf
            If ``buf`` is specified, ``buf`` is returned, otherwise the
            JSON-serialized data.
        """
        data = self.serialize()
        if buf:
            json.dump(data, buf, indent=indent, **dump_kw)
            return buf
        return json.dumps(data, indent=indent, **dump_kw)

    def as_yaml(self, buf=None, **dump_kw):
        """Serialize as YAML.

        Parameters
        ----------
        buf
            If specified, a buffer (e.g. file-like object) to write the YAML
            to.
        indent
            The indentation level, passed to :func:`yaml.safe_dump`.
        **dump_kw
            Other keyword arguments are passed through to :func:`yaml.safe_dump`.

        Returns
        -------
        json_or_buf
            If ``buf`` is specified, ``buf`` is returned, otherwise the
            YAML-serialized data.
        """
        data = self.serialize()
        if buf:
            yaml.safe_dump(data, stream=buf, **dump_kw)
            return buf
        return yaml.safe_dump(data, **dump_kw)


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
        elif isinstance(other, BaseChart):
            return Dashboard(self.description, self.components + [other])

    def __radd__(self, other):
        if isinstance(other, Dashboard):
            return Dashboard(self.description, other.components + self.components)
        elif isinstance(other, BaseChart):
            return Dashboard(self.description, [other] + self.components + [other])

    def __iadd__(self, other):
        if isinstance(other, Dashboard):
            self.components.extend(other.components)
        elif isinstance(other, BaseChart):
            self.components.append(other)

    def show(self, api_client=None, **kwargs):
        if api_client is None:
            api_client = xmiddle()

        body = api_client(self.serialize(), **kwargs)
        return [IpythonHC(chart) for chart in body['components']]


class BaseChart(AsSomethingMixin, metaclass=MergeWithBase):
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

    def __init__(self, query: CubeQuery, id: Optional[str]=None, **kwargs):
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
            'id': self.id,
            'display': display,
            'queries': queries,
        }

    def show(self, *args, **kwargs):
        return Dashboard(components=[self]).show()


print(BaseChart(query, id='base-01').serialize())

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


print(PieChart(query, id='pie-01', name=query['dim1'], y=query['meas1']).serialize())
print(PieChart(query, name=query['dim1'], y=query['meas1'], title='Titlte').serialize())

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

print(DonutChart(query, name=query['dim1'], y=query['meas1']).as_yaml())

try:
    BaseChart(query, unknown_kw=1).serialize()
except ValueError as e:
    print(f"As expected: {e}")
else:
    raise RuntimeError('No ValueError raised')


print(
    BaseChart(query, id='base-01')
    + BaseChart(query, id='base-02')
)
