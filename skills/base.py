from abc import ABC, abstractmethod

class Skill(ABC):

    @abstractmethod
    def can_handle(self, query: str) -> bool:
        pass

    @abstractmethod
    def execute(self, query: str):
        pass
