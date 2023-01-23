import pytest

from pytrevl.components import ScoreComponent
from pytrevl import CubeQuery

@pytest.fixture
def query():
    return CubeQuery('cube', ['1st-measure', '2nd-measure'])

@pytest.fixture
def simple_score_component(query):
    return ScoreComponent(query, id='component-id')


def test_uses_1st_measure():
    query = CubeQuery('cube', ['1st-measure'])
    component = ScoreComponent(query, id='component-id')
    expected = {
        'id': 'component-id',
        'type': 'score',
        'queries': [{
            'measures': [
                'cube.1st-measure',
            ],
        }],
        'display': {
            'column': '$cube.1st-measure',
        },
    }

    assert component.serialize() == expected
