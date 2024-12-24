

from src.core.components.input.interface.InputInterface import InputInterface
from src.core.components.tools.token.tokenizer_interface import  TokenizerInterface




class BasicInput(InputInterface):

    def __init__(self, MAX_TOKENS: int, tokenizer: TokenizerInterface):
        self.MAX_TOKENS = MAX_TOKENS
        self.tokenizer = tokenizer

    def validate(self, query: str, file: str = None):
        self.validate_token_limit(query=query, file_content=file)

    def validate_token_limit(self, query, file_content):
        query_tokens = self.tokenizer.count_tokens(query)
        total_tokens = query_tokens
        if file_content:
            file_tokens = self.tokenizer.count_tokens(file_content)
            total_tokens = query_tokens + file_tokens
            
        if total_tokens > self.MAX_TOKENS:
            raise ValueError(f"A entrada excede o limite de tokens.")
        return True