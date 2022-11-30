from typing import Protocol
import pandas as pd

class Component(Protocol):
    '''
    Protocol base class for components
    '''
    def show(self) -> None:
        ...

    def get_data(self) -> pd.DataFrame:
        ...