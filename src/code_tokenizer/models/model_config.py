"""Model configuration and encoding mappings."""

from typing import Dict

# Model context window sizes (in tokens)
MODEL_CONTEXT_SIZES: Dict[str, int] = {
    # OpenAI Models
    "gpt-4": 8192,
    "gpt-4-32k": 32768,
    "gpt-4-turbo": 128000,
    "gpt-3.5-turbo": 4096,
    "gpt-3.5-turbo-16k": 16384,
    "text-davinci-003": 4097,
    "text-davinci-002": 4097,
    "code-davinci-002": 8001,
    "code-cushman-001": 2048,
    "text-curie-001": 2049,
    "text-babbage-001": 2049,
    "text-ada-001": 2049,
    # Anthropic Models
    "claude-3-opus": 200000,
    "claude-3-sonnet": 200000,
    "claude-3-haiku": 200000,
    "claude-2": 100000,
    "claude-instant": 100000,
    # Google Models
    "gemini-2.0-flash": 1048576,
    "gemini-2.0-flash-lite-preview": 1048576,
    "gemini-1.5-pro": 2097152,
    # DeepSeek Models
    "deepseek-r1": 128000,
}

# Use the same values for token limits
MODEL_TOKEN_LIMITS = MODEL_CONTEXT_SIZES

# Mapping of model names to their tiktoken encoding names
MODEL_ENCODINGS: Dict[str, str] = {
    # Default to cl100k_base for all models
    model: "cl100k_base"
    for model in MODEL_CONTEXT_SIZES.keys()
}

# Default model to use if none specified
DEFAULT_MODEL = "claude-3-sonnet"


def get_model_encoding(model_name: str) -> str:
    """
    Get the tiktoken encoding name for a given model.

    Args:
        model_name: Name of the model

    Returns:
        str: Encoding name for the model

    Raises:
        ValueError: If model is not supported
    """
    if model_name not in MODEL_ENCODINGS:
        raise ValueError(
            f"Model {model_name} not supported. Supported models: {list(MODEL_ENCODINGS.keys())}"
        )
    return MODEL_ENCODINGS[model_name]


def get_model_token_limit(model_name: str) -> int:
    """
    Get the token limit for a given model.

    Args:
        model_name: Name of the model

    Returns:
        int: Token limit for the model

    Raises:
        ValueError: If model is not supported
    """
    if model_name not in MODEL_TOKEN_LIMITS:
        raise ValueError(
            f"Model {model_name} not supported. Supported models: {list(MODEL_TOKEN_LIMITS.keys())}"
        )
    return MODEL_TOKEN_LIMITS[model_name]
