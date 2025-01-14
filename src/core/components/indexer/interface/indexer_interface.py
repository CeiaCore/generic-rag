
from abc import ABC, abstractmethod


class IIndexer(ABC):
    @abstractmethod
    def indexer(self, input):
        raise NotImplementedError