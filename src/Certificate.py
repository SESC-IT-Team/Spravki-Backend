from abc import ABC, abstractmethod

class Certificate(ABC):

    @abstractmethod
    def render():
        pass