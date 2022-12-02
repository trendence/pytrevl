'''
API Protocol class
'''

from typing import Protocol

class Api(Protocol):
    '''
    Protocol class for api modules
    '''
    def connect(self) -> None:
        ...