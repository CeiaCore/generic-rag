

from abc import ABC, abstractmethod


class InputInterface(ABC):

    @abstractmethod
    def validate(self, query: str, file_content: str = None):
        raise NotImplementedError