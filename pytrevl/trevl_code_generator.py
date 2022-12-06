'''
Trevl Code Generator
'''
from pytrevl.component import Component

class Trevl_Code_Generator:
    def __init__(self, component: Component):
        self.component = component

    def create_yaml(self) -> dict:
        yaml = {
            'description': 'Placeholder',
            'parameters': [],
            'components': [
                {
                    'id': self.component.id,
                    'type': 'chart',
                    'queries': [{
                        'measures': [self.component.cube + "." + self.component.measure],
                        'dimensions': [self.component.cube + "." + self.component.dimension],
                        'filters': []
                        }],
                    'display': {
                        'chart': {'type': self.component.type},
                        'title': {'text': self.component.title},
                        'series': [{
                            'name': "$" + self.component.cube + "." + self.component.dimension,
                            'x': "$" + self.component.cube + "." + self.component.dimension,
                            'y': "$" + self.component.cube + "." + self.component.measure}
                            ]}
                }]}
        for filter in self.component.filters:
            yaml["components"][0]["queries"][0]["filters"].append({
                'member': self.component.cube + "." + filter[0],
                'operator': filter[1],
                'values': [filter[2]]})
        return yaml

'''
    Deprecated function for creating TREVL code. 

    def create_trevl(self) -> str:
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
                  - {self.component.cube}.{self.component.x}"""
        if self.component.filters:
          trevl_code += """
                filters:"""
          for filter in self.component.filters:
              trevl_code += f"""
                - member: "{self.component.cube}.{filter[0]}"
                  operator: "{filter[1]}"
                  values:
                    - "{filter[2]}" """
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
                  - {self.component.cube}.{self.component.y}"""
        if self.component.filters:
          trevl_code += """
                filters:"""
          for filter in self.component.filters:
              trevl_code += f"""
                - member: "{self.component.cube}.{filter[0]}"
                  operator: "{filter[1]}"
                  values:
                    - "{filter[2]}" """
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