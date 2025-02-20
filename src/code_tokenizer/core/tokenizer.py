"""Core tokenizer functionality for code processing."""

import logging
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from typing import Any, Dict, List, Optional, Tuple

import tiktoken

from ..exceptions import EncodingNotSupportedError, ModelNotSupportedError, TokenizationError
from ..models.model_config import get_model_encoding, get_model_token_limit

# Configure logging
logger = logging.getLogger(__name__)

# Constants
CHUNK_SIZE = 100000  # Process 100KB at a time
MAX_WORKERS = 4  # Maximum number of threads for parallel processing
CACHE_SIZE = 1024  # LRU cache size for token counting


@lru_cache(maxsize=CACHE_SIZE)
def get_encoding(encoding_name: str) -> tiktoken.Encoding:
    """Get a tiktoken encoding by name with caching.

    Args:
        encoding_name: Name of the encoding to get

    Returns:
        tiktoken.Encoding: The requested encoding

    Raises:
        EncodingNotSupportedError: If the encoding is not supported
    """
    try:
        return tiktoken.get_encoding(encoding_name)
    except KeyError as e:
        logger.error(f"Encoding not supported: {encoding_name}")
        raise EncodingNotSupportedError(f"Encoding not supported: {encoding_name}") from e


class CodeTokenizer:
    """A class for tokenizing code using tiktoken with optimized performance."""

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
            self._executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)
            self._stats: Dict[str, Any] = {"total_tokens": 0, "chunks_processed": 0, "errors": 0}
        except ValueError as e:
            logger.error(f"Model not supported: {model_name}")
            raise ModelNotSupportedError(str(e))
        except EncodingNotSupportedError as e:
            logger.error(f"Encoding error: {str(e)}")
            raise e

    def _process_chunk(self, chunk: str) -> int:
        """Process a single chunk of text.

        Args:
            chunk: Text chunk to process

        Returns:
            int: Number of tokens in the chunk
        """
        try:
            tokens = self.encoding.encode(chunk)
            self._stats["chunks_processed"] += 1
            return len(tokens)
        except Exception as e:
            self._stats["errors"] += 1
            logger.warning(f"Error processing chunk: {str(e)}")
            return 0

    def count_tokens(self, text: str) -> int:
        """Count the number of tokens in a text with parallel processing.

        Args:
            text: Text to count tokens for

        Returns:
            int: Number of tokens in the text

        Raises:
            TokenizationError: If token counting fails
        """
        if not text:
            return 0

        try:
            # Split text into chunks
            chunks = [text[i : i + CHUNK_SIZE] for i in range(0, len(text), CHUNK_SIZE)]

            # Process chunks in parallel
            futures = [self._executor.submit(self._process_chunk, chunk) for chunk in chunks]
            total_tokens = sum(future.result() for future in futures)

            self._stats["total_tokens"] += total_tokens
            return total_tokens

        except Exception as e:
            logger.error(f"Token counting failed: {str(e)}")
            raise TokenizationError(f"Failed to count tokens: {str(e)}")

    def encode(self, text: str) -> Tuple[List[int], List[str]]:
        """Encode text into tokens with optimized memory usage.

        Args:
            text: Text to encode

        Returns:
            Tuple containing:
            - List of token IDs
            - List of token strings

        Raises:
            TokenizationError: If encoding fails
        """
        if not text:
            return [], []

        try:
            token_ids = []
            token_strings = []

            # Process text in chunks to manage memory
            for i in range(0, len(text), CHUNK_SIZE):
                chunk = text[i : i + CHUNK_SIZE]
                chunk_ids = self.encoding.encode(chunk)
                # Decode tokens in smaller batches
                batch_size = 1000
                for j in range(0, len(chunk_ids), batch_size):
                    batch = chunk_ids[j : j + batch_size]
                    strings = [self.encoding.decode([id]) for id in batch]
                    token_strings.extend(strings)
                token_ids.extend(chunk_ids)

            return token_ids, token_strings

        except Exception as e:
            logger.error(f"Encoding failed: {str(e)}")
            raise TokenizationError(f"Failed to encode text: {str(e)}")

    def decode(self, token_ids: List[int]) -> str:
        """Decode token IDs back into text with error handling.

        Args:
            token_ids: List of token IDs to decode

        Returns:
            str: Decoded text

        Raises:
            TokenizationError: If decoding fails
        """
        if not token_ids:
            return ""

        try:
            return self.encoding.decode(token_ids)
        except Exception as e:
            logger.error(f"Decoding failed: {str(e)}")
            raise TokenizationError(f"Failed to decode tokens: {str(e)}")

    def truncate_to_token_limit(self, text: str, max_tokens: Optional[int] = None) -> str:
        """Truncate text to a maximum number of tokens with optimization.

        Args:
            text: Text to truncate
            max_tokens: Maximum number of tokens (defaults to self.max_tokens)

        Returns:
            str: Truncated text

        Raises:
            TokenizationError: If truncation fails
        """
        if not text:
            return text

        try:
            limit = max_tokens or self.max_tokens
            token_ids, _ = self.encode(text)

            if len(token_ids) <= limit:
                return text

            # Try to find a natural break point (newline, period, etc.)
            truncated_ids = token_ids[:limit]
            truncated_text = self.decode(truncated_ids)

            # Look for last sentence or line break
            break_points = ["\n\n", ".\n", "\n", ". ", ";"]
            for point in break_points:
                last_break = truncated_text.rfind(point)
                if last_break > len(truncated_text) * 0.8:  # Only break in last 20%
                    return truncated_text[: last_break + len(point)]

            return truncated_text

        except Exception as e:
            logger.error(f"Truncation failed: {str(e)}")
            raise TokenizationError(f"Failed to truncate text: {str(e)}")

    def get_stats(self) -> Dict[str, Any]:
        """Get tokenizer statistics.

        Returns:
            Dict[str, Any]: Statistics about tokenizer usage
        """
        return self._stats.copy()

    def reset_stats(self) -> None:
        """Reset tokenizer statistics."""
        self._stats = {"total_tokens": 0, "chunks_processed": 0, "errors": 0}

    def __del__(self) -> None:
        """Cleanup resources."""
        if hasattr(self, "_executor"):
            self._executor.shutdown(wait=False)


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
        TokenizationError: If token counting fails
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
        TokenizationError: If truncation fails
    """
    tokenizer = CodeTokenizer(model_name=model_name, max_tokens=max_tokens)
    truncated = tokenizer.truncate_to_token_limit(text, max_tokens)
    return truncated, tokenizer.count_tokens(truncated)
