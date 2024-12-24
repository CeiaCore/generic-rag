

from abc import ABC, abstractmethod


class TokenizerInterface(ABC):
    
    @abstractmethod
    def count_tokens(self, value) -> int:
        raise NotImplementedError