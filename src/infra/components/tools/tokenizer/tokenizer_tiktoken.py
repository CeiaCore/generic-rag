
import tiktoken

from src.core.components.tools.token.tokenizer_interface import TokenizerInterface


class TokenizerTikToken(TokenizerInterface):

    def __init__(self, model: str = "o200k_base") -> None:
        self.model = model
        
        
    def count_tokens(self, value) -> int:
        
        tokenizer = tiktoken.get_encoding(self.model)
        tokens = tokenizer.encode(value)
        len_tokens = len(tokens)
        return len_tokens