"""Utility functions."""
from copy import deepcopy
from itertools import zip_longest
import json
from typing import Optional, Union

import yaml


class NoAliasDumper(yaml.SafeDumper):
    """Stop PyYAML from using anchors and aliases during dump operation.
    """
    def ignore_aliases(self, data):
        return True


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
            yaml.dump(data, Dumper=NoAliasDumper, stream=buf, **dump_kw)
            return buf
        return yaml.dump(data, Dumper=NoAliasDumper, **dump_kw)


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
