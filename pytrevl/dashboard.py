import yaml

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
            display(component.show()) # Render Charts in Jupyter
    
    def get_json(self) -> dict:
        dashboard_json = {'description': self.description, 'parameters': [], 'components': []}
        for component in self.components.values():
            json = component.get_json()
            dashboard_json["components"].append(json["components"][0])
        return dashboard_json

    def get_yaml(self) -> str:
        dashboard_json = self.get_json()
        dashboard_yaml = yaml.safe_dump(dashboard_json)
        print(dashboard_yaml)