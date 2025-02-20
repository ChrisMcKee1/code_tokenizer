"""Core tokenizer functionality for code processing."""

from typing import List, Optional, Tuple

import tiktoken

from ..exceptions import EncodingNotSupportedError, ModelNotSupportedError
from ..models.model_config import get_model_encoding, get_model_token_limit


def get_encoding(encoding_name: str) -> tiktoken.Encoding:
    """Get a tiktoken encoding by name.

    Args:
        encoding_name: Name of the encoding to get

    Returns:
        tiktoken.Encoding: The requested encoding

    Raises:
        EncodingNotSupportedError: If the encoding is not supported
    """
    try:
        return tiktoken.get_encoding(encoding_name)
    except KeyError:
        raise EncodingNotSupportedError(f"Encoding not supported: {encoding_name}")


class CodeTokenizer:
    """A class for tokenizing code using tiktoken."""

    def __init__(self, model_name: str = "gpt-4o", max_tokens: Optional[int] = None):
        """Initialize the CodeTokenizer.

        Args:
            model_name: Name of the model to use for tokenization
            max_tokens: Maximum number of tokens per file (defaults to model's limit)

        Raises:
            ModelNotSupportedError: If the model is not supported
            EncodingNotSupportedError: If the encoding is not supported
        """
        try:
            self.model_name = model_name
            self.encoding_name = get_model_encoding(model_name)
            self.encoding = get_encoding(self.encoding_name)
            self.max_tokens = max_tokens or get_model_token_limit(model_name)
        except ValueError as e:
            raise ModelNotSupportedError(str(e))
        except EncodingNotSupportedError as e:
            raise e

    def count_tokens(self, text: str) -> int:
        """Count the number of tokens in a text.

        Args:
            text: Text to count tokens for

        Returns:
            Number of tokens in the text
        """
        if not text:
            return 0

        # Process text in chunks to avoid stack overflow
        chunk_size = 100000  # Process 100KB at a time
        total_tokens = 0

        for i in range(0, len(text), chunk_size):
            chunk = text[i : i + chunk_size]
            total_tokens += len(self.encoding.encode(chunk))

        return total_tokens

    def encode(self, text: str) -> Tuple[List[int], List[str]]:
        """Encode text into tokens.

        Args:
            text: Text to encode

        Returns:
            Tuple containing:
            - List of token IDs
            - List of token strings
        """
        if not text:
            return [], []

        token_ids = []
        token_strings = []

        # Process text in chunks
        chunk_size = 100000
        for i in range(0, len(text), chunk_size):
            chunk = text[i : i + chunk_size]
            chunk_ids = self.encoding.encode(chunk)
            chunk_strings = [self.encoding.decode([id]) for id in chunk_ids]

            token_ids.extend(chunk_ids)
            token_strings.extend(chunk_strings)

        return token_ids, token_strings

    def decode(self, token_ids: List[int]) -> str:
        """Decode token IDs back into text.

        Args:
            token_ids: List of token IDs to decode

        Returns:
            Decoded text
        """
        if not token_ids:
            return ""
        return self.encoding.decode(token_ids)

    def truncate_to_token_limit(self, text: str, max_tokens: Optional[int] = None) -> str:
        """Truncate text to a maximum number of tokens.

        Args:
            text: Text to truncate
            max_tokens: Maximum number of tokens (defaults to self.max_tokens)

        Returns:
            Truncated text
        """
        if not text:
            return text

        limit = max_tokens or self.max_tokens
        token_ids, _ = self.encode(text)

        if len(token_ids) <= limit:
            return text

        return self.decode(token_ids[:limit])

    def truncate_text(self, text: str, model_name: str, max_tokens: int) -> Tuple[str, int]:
        """Truncate text to fit within token limit.

        Args:
            text: Text to truncate
            model_name: Model to use for tokenization
            max_tokens: Maximum number of tokens allowed

        Returns:
            Tuple[str, int]: Truncated text and token count

        Raises:
            ModelNotSupportedError: If model is not supported
        """
        return truncate_text(text, max_tokens, model_name)


def count_tokens(text: str, model_name: str) -> int:
    """Count the number of tokens in a text using tiktoken.

    Args:
        text: Text to count tokens for
        model_name: Name of the model to use for tokenization

    Returns:
        int: Number of tokens in the text

    Raises:
        ModelNotSupportedError: If model is not supported
        EncodingNotSupportedError: If encoding is not supported
    """
    tokenizer = CodeTokenizer(model_name=model_name)
    return tokenizer.count_tokens(text)


def truncate_text(text: str, max_tokens: int, model_name: str) -> Tuple[str, int]:
    """Truncate text to a maximum number of tokens.

    Args:
        text: Text to truncate
        max_tokens: Maximum number of tokens to keep
        model_name: Name of the model to use for tokenization

    Returns:
        Tuple[str, int]: (truncated_text, token_count)

    Raises:
        ModelNotSupportedError: If model is not supported
        EncodingNotSupportedError: If encoding is not supported
    """
    tokenizer = CodeTokenizer(model_name=model_name, max_tokens=max_tokens)
    truncated = tokenizer.truncate_to_token_limit(text, max_tokens)
    return truncated, tokenizer.count_tokens(truncated)
