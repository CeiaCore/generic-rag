

from abc import ABC, abstractmethod


class InputFileKnowledgeInterface(ABC):

    @abstractmethod
    def extract(self, file_content: str = None):
        raise NotImplementedError