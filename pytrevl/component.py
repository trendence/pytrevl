from typing import Protocol

class Component(Protocol):
    '''
    Protocol base class for components
    '''
    def show(self) -> None:
        ...

    def get_data(self) -> None:
        ...