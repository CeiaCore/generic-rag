from abc import ABC, abstractmethod


class InputFileInterface(ABC):

    @abstractmethod
    def validate(self, file_content: str = None):
        raise NotImplementedError