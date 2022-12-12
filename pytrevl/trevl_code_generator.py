from pytrevl.component import Component
from typing import List

class TrevlCodeGenerator:
    def __init__(self, component: Component):
        self.component = component

    def get_trevl(self) -> dict:
        yaml = {
            'description': 'Placeholder',
            'parameters': [],
            'components': [
                {
                    'id': self.component.id,
                    'type': 'chart',
                    'queries': self._create_queries(),
                    'display': self._create_display()
                }
            ]
        }
        return yaml

    def _create_queries(self) -> List[dict]:
        queries = [{
            'measures': [self.component.cube.name + "." + self.component.measure],
            'dimensions': [self.component.cube.name + "." + self.component.dimension],
            'filters': self._create_filters()
        }]
        return queries

    def _create_filters(self) -> List[dict]:
        filters = []
        for filter in self.component.filters:
            filters.append({
                'member': self.component.cube.name + "." + filter.variable,
                'operator': filter.operator,
                'values': [filter.value]
            })
        return filters

    def _create_display(self) -> dict:
        display = {
            'chart': {'type': self.component.type},
            'title': {'text': self.component.style.title},
            'series': [{
                'name': "$" + self.component.cube.name + "." + self.component.dimension,
                'x': "$" + self.component.cube.name + "." + self.component.dimension,
                'y': "$" + self.component.cube.name + "." + self.component.measure
            }]
        }
        if self.component.__class__.__name__ == 'DonutChart':
            del display['series'][0]['x']
            display['series'][0]['innerSize'] = self.component.style.innerSize

        return display