"""Containers for Cube.js based queries in TREVL."""
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Filter:
    """Container around TREVL filters."""
    # The column name without the cube name
    member: str
    operator: str
    values: Optional[list[str]] = None
    parameter: Optional[str] = None

    def __post_init__(self):
        if self.values is None and self.parameter is None:
            raise ValueError('Filter must have either values or parameter')


@dataclass
class Computed:
    """Container for computed field in TREVL queries."""
    name: str
    code: str
    arguments: Optional[dict[str, str]] = field(default_factory=dict)



@dataclass
class CubeQuery:
    """Wrapper for Cube.js-based TREVL queries.

    The query must reference a single Cube.js schema.

    To reference a column for a chart component, use ``query['...']``.

    Note
    ----
    When creating a query, the columns (e.g. measures, dimensions, filter
    members) **must not** have the cube name as prefix!

    Parameters
    ----------
    cube
        The cube name.
    measures
        The measures to query.
    dimensions
        The dimensions to query.
    filters
        The filters to apply. See :class:`Filter`.
    computed
        Definitions for computed fields

    """
    cube: str
    measures: list[str] = field(default_factory=list)
    dimensions: list[str] = field(default_factory=list)
    filters: list[Filter] = field(default_factory=list)
    computed: list[Computed] = field(default_factory=list)

    def __post_init__(self):
        if not self.measures and not self.dimensions:
            raise ValueError('CubeQuery must have at at least one measure or one dimension!')

    def __getitem__(self, field):
        """Get a reference for `field` in this query."""
        if field in self.measures or field in self.dimensions:
            return f"${self.cube}.{field}"
        if field in {c.name for c in self.computed}:
            return f'${field}'
        raise KeyError(
            f'Field {field!r} not found in query for cube {self.cube}. Available fields: '
            ', '.join(sorted((*self.measures, *self.dimensions, *(c.name for c in self.computed))))
            )

    def _prepend_cube(self, fields: list[str]) -> list[str]:
        return [f'{self.cube}.{f}' for f in fields]

    def _serialize_filter(self, f: Filter) -> dict:
        ret = {
            'member': f'{self.cube}.{f.member}',
            'operator': f.operator,
        }
        if f.parameter:
            ret['parameter'] = f.parameter
        elif f.values:
            ret['values'] = f.values
        return ret

    def _serialize_computed(self, c: Computed) -> dict:
        ret = {
            'name': c.name,
            'code': c.code,
        }

        if c.arguments:
            ret['arguments'] = {
                dst: f'${self.cube}.{src}'
                for dst, src in c.arguments.items()
                }
        return ret

    def serialize(self) -> dict:
        ret = {}

        if self.measures:
            ret['measures'] = self._prepend_cube(self.measures)

        if self.dimensions:
            ret['dimensions'] = self._prepend_cube(self.dimensions)

        if self.filters:
            ret['filters'] = [self._serialize_filter(f) for f in self.filters]

        if self.computed:
            ret['computed'] = [self._serialize_computed(c) for c in self.computed]
        return ret
