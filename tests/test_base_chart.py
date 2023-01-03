from io import StringIO
import json

import pytest
import yaml

from pytrevl.charts import BaseChart, Dashboard
from pytrevl import CubeQuery

@pytest.fixture
def query():
    return CubeQuery('cube', ['measure'])

@pytest.fixture
def simple_chart(query):
    return BaseChart(query, 'id-simple', x=query['measure'], y=query['measure'], title='chart title')

@pytest.fixture
def expected():
    return {
        'id': 'id-simple',
        'type': 'chart',
        'display': {
            'chart': {
                'type': 'line',
                },
            'title': {
                'text': 'chart title',
                },
            'series': [{
                'x': '$cube.measure',
                'y': '$cube.measure',
                }],
            },
        'queries': [{
            'measures': ['cube.measure'],
            }],
        }


def test_simple_serialization(simple_chart, expected):
    assert simple_chart.serialize() == expected

def test_json_serialization(simple_chart, expected):
    assert json.loads(simple_chart.as_json()) == expected

    buf = StringIO()
    simple_chart.as_json(buf=buf)
    buf.seek(0)
    assert json.load(buf) == expected

def test_yaml_serialization(simple_chart, expected):
    assert yaml.safe_load(simple_chart.as_yaml()) == expected

    buf = StringIO()
    simple_chart.as_yaml(buf=buf)
    buf.seek(0)
    assert yaml.safe_load(stream=buf) == expected


def test_component_arithmetics(simple_chart, expected):
    assert type(simple_chart + simple_chart) == Dashboard
    assert type(Dashboard() + simple_chart) == Dashboard
    assert type(simple_chart + Dashboard()) == Dashboard

    dashboard = Dashboard()
    id_orig = id(dashboard)
    dashboard += simple_chart
    assert len(dashboard.components) == 1
    assert id(dashboard) == id_orig

    assert 'desc1' == (Dashboard('desc1') + Dashboard('desc2')).description


def test_subclass_merging(query):
    class TestSub(BaseChart):
        _default = {
            # This should be merged with the original chart
            'chart': {
                'new': 'value',
            },
            # This should be added to the original data
            'nested': {
                'test': ['value'],
            },
        }
        # This should overwrite the original 'x' mapping
        _kw_paths = {
            'x': 'a.new.0.path',
        }

    sub = TestSub(query, id='id-sub', x=query['measure'], y=query['measure'], title='chart title')
    expected = {
        'id': 'id-sub',
        'type': 'chart',
        'display': {
            'chart': {
                'new': 'value',
                'type': 'line',
            },
            'title': {
                'text': 'chart title',
            },
            'series': [{
                'y': '$cube.measure',
            }],
            'a': {
                'new': [{
                    'path': '$cube.measure',
                }],
            },
            'nested': {
                'test': ['value'],
            },
        },
        'queries': [{
            'measures': ['cube.measure'],
        }],
    }

    assert sub.serialize() == expected
