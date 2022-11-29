from pytrevl.component import Component

class Dashboard:
    def __init__(self, description: str = ""):
        self.components: dict[str, Component] = {}
        self.description = description

    def add_component(self, component: Component) -> str:
        self.components[component.id] = component
        return component.id

    def remove_component(self, component: Component) -> str:
        self.components.pop(component.id)
        return f"{component.id} removed from dashboard"

    def get_component(self, component_id: str) -> Component:
        return self.components[component_id]

    def show(self) -> None:
        for component in self.components.values():
            component.show()

    def update(self) -> None:
        ...
    
    def show_trevl(self) -> str:
        trevl_code = f"""
            description: >-
            {self.description}
            'parameters: []"""
        for component in self.components.values():
            trevl_code += f"""
            components:
                - id: {component.id}
                    type: chart
                    queries:
                    - measures:
                        - {component.cube}.{component.y}
                    dimensions:
                        - {component.cube}.{component.x}
                    filters:"""
            for filter, value in component.filters.items():
                trevl_code += f"""
                        - member: "{component.cube}.{filter}"
                          operator: "equals"
                          values:
                            - "{value}" """
            trevl_code += f"""
                    display:
                    chart:
                        type: "{component.type}"
                    title:
                        text: "{component.title}"
                    series:
                        - name: ${component.cube}.{component.x}
                          y: ${component.cube}.{component.y}
                        """
        print (trevl_code)
