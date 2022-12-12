def test_get_yaml(self):
    # Test that the get_yaml() method returns the correct YAML representation of the chart
    chart = Chart()
    chart.id = "chart_id"
    chart.title = "Test Chart"
    chart.cube = "test_cube"
    chart.measure = "test_measure"
    chart.dimension = "test_dimension"
    chart.filters = [
        ["filter1", "=", "value1"],
        ["filter2", "=", "value2"]
    ]

    expected_yaml = {
        'description': 'Placeholder',
        'parameters': [],
        'components': [
            {
                'id': "chart_id",
                'type': 'chart',
                'queries': [
                    {
                        'measures': ["test_cube.test_measure"],
                        'dimensions': ["test_cube.test_dimension"],
                        'filters': [
                            {
                                'member': "test_cube.filter1",
                                'operator': "=",
                                'values': ["value1"]
                            },
                            {
                                'member': "test_cube.filter2",
                                'operator': "=",
                                'values': ["value2"]
                            }
                        ]
                    }
                ],
                'display': {
                    'chart': {'type': 'column'},
                    'title': {'text': 'Test Chart'},
                    'series': [
                        {
                            'name': "$test_cube.test_dimension",
                            'y': "$test_cube.test_measure"
                        }
                    ]
                }
            }
        ]
    }
    yaml = chart.get_yaml()
    assert yaml == expected_yaml

def test_get_trevl(self):
    # Test that the get_trevl() method prints the correct TREVL representation of the chart
    chart = Chart()
    chart.id = "chart_id"
    chart.title = "Test Chart"
    chart.cube = "test_cube"
    chart.measure = "test_measure"
    chart.dimension = "test_dimension"
    chart.filters = [
        ["filter1", "=", "value1"],
        ["filter2", "=", "value2"]
    ]

    expected_trevl = '''description: Placeholder
parameters: []
components:
- id: chart_id
  type: chart
  queries:
  - measures:
    - test_cube.test_measure
    dimensions:
    - test_cube.test_dimension
    filters:
    - member: test_cube.filter1
      operator: =
      values:
      - value1
    - member: test_cube.filter2
      operator: =
      values:
      - value2
  display:
    chart:
      type: column
    title:
      text: Test Chart
    series:
    - name: $test_cube.test_dimension
      y: $test_cube.test_measure
'''

