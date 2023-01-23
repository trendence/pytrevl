import pytest

from pytrevl.cube import Computed, CubeQuery, MultiCubeQuery

@pytest.fixture
def query():
    return CubeQuery(
        'cube-name',
        ['m-1', 'm-2'],
        ['d-1', 'd-2'],
        computed=[
            Computed('c-1', 'code-1'),
            Computed('c-2', 'code-2'),
        ],
    )


def test_using_measures(query):
    # Known measures can be referenced
    assert '$cube-name.m-1' == query['m-1']
    assert '$cube-name.m-2' == query['m-2']

    # Unknown measures throw an error
    with pytest.raises(KeyError):
        query['m-3']

def test_using_dimensions(query):
    # Known dimensions can be referenced
    assert '$cube-name.d-1' == query['d-1']
    assert '$cube-name.d-2' == query['d-2']

    # Unknown dimensions throw an error
    with pytest.raises(KeyError):
        query['d-3']

def test_using_computed(query):
    # Known computed fields can be referenced
    assert '$c-1' == query['c-1']
    assert '$c-2' == query['c-2']

    # Unknown computed fields throw an error
    with pytest.raises(KeyError):
        query['c-3']


def test_multicube_query():
    query = MultiCubeQuery(['cubeA.meas1', 'cubeB.meas2'], ['cubeA.dim1', 'cubeB.dim2'])
    assert query.serialize() == {
        'measures': ['cubeA.meas1', 'cubeB.meas2'],
        'dimensions': ['cubeA.dim1', 'cubeB.dim2'],
    }

    assert query['cubeA.meas1'] == '$cubeA.meas1'
    assert query['cubeA.meas1'] == '$cubeA.meas1'
