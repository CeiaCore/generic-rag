

from abc import ABC, abstractmethod
from typing import List


class RetrievalInterface(ABC):

    @abstractmethod
    def retriever(self, query_embedding: List[float]):
        raise NotImplementedError