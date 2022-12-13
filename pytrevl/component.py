from typing import Protocol

class Component(Protocol):
    '''
    Protocol base class for components
    '''
    def show(self) -> None:
        ...
