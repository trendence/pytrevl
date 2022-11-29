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
    
    def trevl(self) -> str:
        trevl_code = "" #show trevl code for dashboard
        return trevl_code

    