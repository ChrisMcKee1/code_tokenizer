"""Core tokenizer functionality for code processing."""

from typing import Tuple

import tiktoken

from ..models.model_config import MODEL_ENCODINGS, get_model_encoding, get_model_token_limit


def count_tokens(text: str, model_name: str) -> int:
    """
    Count the number of tokens in a text using tiktoken.

    Args:
        text: Text to count tokens for
        model_name: Name of the model to use for tokenization

    Returns:
        int: Number of tokens in the text

    Raises:
        ValueError: If model is not supported
    """
    try:
        encoding = tiktoken.get_encoding(get_model_encoding(model_name))
        return len(encoding.encode(text))
    except KeyError:
        raise ValueError(
            f"Model {model_name} not supported. Supported models: {list(MODEL_ENCODINGS.keys())}"
        )


def truncate_text(text: str, max_tokens: int, model_name: str) -> Tuple[str, int]:
    """
    Truncate text to a maximum number of tokens.

    Args:
        text: Text to truncate
        max_tokens: Maximum number of tokens to keep
        model_name: Name of the model to use for tokenization

    Returns:
        Tuple[str, int]: (truncated_text, token_count)

    Raises:
        ValueError: If model is not supported
    """
    try:
        encoding = tiktoken.get_encoding(get_model_encoding(model_name))
        tokens = encoding.encode(text)

        if len(tokens) <= max_tokens:
            return text, len(tokens)

        truncated_tokens = tokens[:max_tokens]
        return encoding.decode(truncated_tokens), len(truncated_tokens)
    except KeyError:
        raise ValueError(
            f"Model {model_name} not supported. Supported models: {list(MODEL_ENCODINGS.keys())}"
        )


class CodeTokenizer:
    """Handles code tokenization using tiktoken."""
    
    def __init__(self, model_name: str) -> None:
        """
        Initialize the tokenizer.
        
        Args:
            model_name: Name of the LLM model to use for tokenization
        """
        self.model_name = model_name
        self.encoding = tiktoken.encoding_for_model(model_name)
        self.max_tokens = get_model_token_limit(model_name)
        
    def count_tokens(self, text: str) -> int:
        """
        Count the number of tokens in a text.
        
        Args:
            text: Text to count tokens for
            
        Returns:
            int: Number of tokens
        """
        return len(self.encoding.encode(text))
        
    def truncate_to_token_limit(self, text: str, max_tokens: int) -> str:
        """
        Truncate text to stay within token limit.
        
        Args:
            text: Text to truncate
            max_tokens: Maximum number of tokens allowed
            
        Returns:
            str: Truncated text
        """
        tokens = self.encoding.encode(text)
        if len(tokens) <= max_tokens:
            return text
            
        truncated_tokens = tokens[:max_tokens]
        return self.encoding.decode(truncated_tokens)
