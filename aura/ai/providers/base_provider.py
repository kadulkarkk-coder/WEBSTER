from abc import ABC, abstractmethod


class BaseProvider(ABC):

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_status(self) -> str:
        pass