"""Core tokenizer functionality for code processing."""

from typing import Tuple
import tiktoken
from ..models.model_config import MODEL_ENCODINGS, get_model_encoding


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
