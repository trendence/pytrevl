'''
Trevl Code Generator
'''
from pytrevl.component import Component

class Trevl_Code_Generator:
    def __init__(self, component: Component):
        self.component = component

    def create_trevl(self) -> str:
        '''
        Function for creating TREVL code. Maybe there is an easy way to turn YAML into TREVL?
        '''

        if self.component.type == "pie":
          trevl_code = f"""
          description: >-
            Placeholder
          parameters: []
          components:
              - id: {self.component.id}
                type: chart
                queries:
                - measures:
                    - {self.component.cube}.{self.component.y}
                  dimensions:
                    - {self.component.cube}.{self.component.x}
                  filters:"""
          for filter, value in self.component.filters.items():
              trevl_code += f"""
                    - member: "{self.component.cube}.{filter}"
                      operator: "equals"
                      values:
                        - "{value}" """
          trevl_code += f"""
                display:
                  chart:
                    type: "{self.component.type}"
                  title:
                    text: "{self.component.title}"
                  series:
                    - name: ${self.component.cube}.{self.component.x}
                      x: ${self.component.cube}.{self.component.x}
                      y: ${self.component.cube}.{self.component.y}
          """

        else:
          trevl_code = f"""
          description: >-
            Placeholder
          parameters: []
          components:
              - id: {self.component.id}
                type: chart
                queries:
                - measures:
                    - {self.component.cube}.{self.component.x}
                  dimensions:
                    - {self.component.cube}.{self.component.y}
                  filters:
                  - """
          for filter, value in self.component.filters.items():
              trevl_code += f"""
                      member: "{self.component.cube}.{filter}"
                      operator: "equals"
                      values:
                        - "{value}" """
          trevl_code += f"""
                display:
                  chart:
                    type: "{self.component.type}"
                  title:
                    text: "{self.component.title}"
                  series:
                    - name: "{self.component.title}"
                      x: ${self.component.cube}.{self.component.y}
                      y: ${self.component.cube}.{self.component.x}
          """
        return trevl_code

'''
# Not useful at the moment

    def create_yaml(self) -> dict:
        yaml = {
            'description': 'Placeholder',
            'parameters': [],
            'components': [
                {
                    'id': self.component.id,
                    'type': 'chart',
                    'queries': [{
                        'measures': [self.component.cube + "." + self.component.y],
                        'dimensions': [self.component.cube + "." + self.component.x],
                        'filters': []
                        }],
                    'display': {
                        'chart': {'type': self.component.type},
                        'title': {'text': self.component.title},
                        'series': [{
                            'name': self.component.cube + "." + self.component.x,
                            'x': self.component.cube + "." + self.component.x,
                            'y': self.component.cube + "." + self.component.y}
                            ]}
                }]}
        for filter, value in self.component.filters.items():
            yaml["components"][0]["queries"][0]["filters"].append({
                'member': self.component.cube + "." + filter,
                'operator': "equals",
                'values': [value]})
        return yaml
'''



