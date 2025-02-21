"""Model configuration and encoding mappings."""

import dataclasses
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set, Union

# Default model configuration values
DEFAULT_MODEL = "gpt-4o"
DEFAULT_MAX_TOKENS = 200000
DEFAULT_OUTPUT_FORMAT = "markdown"


@dataclass
class TokenizerConfig:
    """Configuration for the tokenizer service."""

    model_name: str = DEFAULT_MODEL
    max_tokens: Optional[int] = None
    bypass_gitignore: bool = False
    base_dir: Optional[str] = None
    output_format: str = "markdown"
    output_dir: Optional[str] = None
    include_metadata: bool = True
    file_extensions: Optional[Set[str]] = None
    skip_extensions: Optional[Set[str]] = None
    show_progress: bool = True
    # Add new sanitization options
    preserve_comments: bool = True
    aggressive_whitespace: bool = False
    sanitize_content: bool = True

    def __init__(self, config: Optional[Union[Dict[str, Any], "TokenizerConfig"]] = None) -> None:
        """Initialize configuration from dictionary or another config.

        Args:
            config: Configuration dictionary or TokenizerConfig instance
        """
        if config is None:
            config = {}
        elif isinstance(config, TokenizerConfig):
            # Copy from another config
            for field in dataclasses.fields(self):
                setattr(self, field.name, getattr(config, field.name))
            return

        # Set defaults first
        self.model_name = DEFAULT_MODEL
        self.max_tokens = None
        self.bypass_gitignore = False
        self.base_dir = None
        self.output_format = "markdown"
        self.output_dir = None
        self.include_metadata = True
        self.file_extensions = None
        self.skip_extensions = None
        self.show_progress = True
        self.preserve_comments = True
        self.aggressive_whitespace = False
        self.sanitize_content = True

        # Update from config dict
        if isinstance(config, dict):
            for key, value in config.items():
                if hasattr(self, key):
                    setattr(self, key, value)

        # Post-initialization validation
        self.validate()

    def validate(self):
        """Validate configuration values."""
        if self.model_name not in MODEL_ENCODINGS:
            raise ValueError(f"Model {self.model_name} not supported")

        if self.max_tokens is None:
            self.max_tokens = get_model_token_limit(self.model_name)

        if self.output_format not in ["markdown", "json", "yaml", "text"]:
            raise ValueError(f"Output format {self.output_format} not supported")

        # Convert file extensions to sets if provided as lists
        if self.file_extensions and not isinstance(self.file_extensions, set):
            self.file_extensions = set(self.file_extensions)
        if self.skip_extensions and not isinstance(self.skip_extensions, set):
            self.skip_extensions = set(self.skip_extensions)

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary.

        Returns:
            Dict[str, Any]: Configuration as dictionary
        """
        return {
            field.name: getattr(self, field.name)
            for field in dataclasses.fields(self)
        }


# Encoding formats
class Encoding:
    GPT2 = "gpt2"
    R50K_BASE = "r50k_base"
    P50K_BASE = "p50k_base"
    P50K_EDIT = "p50k_edit"
    CL100K_BASE = "cl100k_base"
    O200K_BASE = "o200k_base"


# Mapping of model names to their tiktoken encoding names
MODEL_ENCODINGS: Dict[str, str] = {
    # O-series models
    "o1-preview": Encoding.O200K_BASE,
    "o1-mini": Encoding.O200K_BASE,
    "gpt-4o": Encoding.O200K_BASE,
    "chatgpt-4o": Encoding.O200K_BASE,
    # GPT-4 and GPT-3.5 models
    "gpt-4": Encoding.CL100K_BASE,
    "gpt-3.5-turbo": Encoding.CL100K_BASE,
    "gpt-3.5": Encoding.CL100K_BASE,
    "ft:gpt-4": Encoding.CL100K_BASE,
    "ft:gpt-3.5-turbo": Encoding.CL100K_BASE,
    "ft:davinci-002": Encoding.CL100K_BASE,
    "ft:babbage-002": Encoding.CL100K_BASE,
    # Text embedding models
    "text-embedding-ada-002": Encoding.CL100K_BASE,
    # P50K_BASE models
    "text-davinci-003": Encoding.P50K_BASE,
    "text-davinci-002": Encoding.P50K_BASE,
    "code-davinci-002": Encoding.P50K_BASE,
    "code-davinci-001": Encoding.P50K_BASE,
    "code-cushman-002": Encoding.P50K_BASE,
    "code-cushman-001": Encoding.P50K_BASE,
    "davinci-codex": Encoding.P50K_BASE,
    "cushman-codex": Encoding.P50K_BASE,
    # R50K_BASE models
    "text-davinci-001": Encoding.R50K_BASE,
    "text-curie-001": Encoding.R50K_BASE,
    "text-babbage-001": Encoding.R50K_BASE,
    "text-ada-001": Encoding.R50K_BASE,
    "davinci": Encoding.R50K_BASE,
    "curie": Encoding.R50K_BASE,
    "babbage": Encoding.R50K_BASE,
    "ada": Encoding.R50K_BASE,
    "text-similarity-davinci-001": Encoding.R50K_BASE,
    "text-similarity-curie-001": Encoding.R50K_BASE,
    "text-similarity-babbage-001": Encoding.R50K_BASE,
    "text-similarity-ada-001": Encoding.R50K_BASE,
    "text-search-davinci-doc-001": Encoding.R50K_BASE,
    "text-search-curie-doc-001": Encoding.R50K_BASE,
    "text-search-ada-doc-001": Encoding.R50K_BASE,
    "text-search-babbage-doc-001": Encoding.R50K_BASE,
    "code-search-babbage-code-001": Encoding.R50K_BASE,
    "code-search-ada-code-001": Encoding.R50K_BASE,
    # P50K_EDIT models
    "text-davinci-edit-001": Encoding.P50K_EDIT,
    "code-davinci-edit-001": Encoding.P50K_EDIT,
    # GPT2 models
    "gpt2": Encoding.GPT2,
}

# Model token limits
MODEL_TOKEN_LIMITS = {
    # O-series models
    "o1-preview": 200000,
    "o1-mini": 100000,
    "gpt-4o": 8192,
    "chatgpt-4o": 8192,
    # GPT-4 and GPT-3.5 models
    "gpt-4": 8192,
    "gpt-3.5-turbo": 4096,
    "gpt-3.5": 4096,
    # Text embedding models
    "text-embedding-ada-002": 8191,
    # P50K_BASE models
    "text-davinci-003": 4097,
    "text-davinci-002": 4097,
    "code-davinci-002": 8001,
    "code-davinci-001": 8001,
    "code-cushman-002": 2048,
    "code-cushman-001": 2048,
    # R50K_BASE models
    "text-davinci-001": 2048,
    "text-curie-001": 2048,
    "text-babbage-001": 2048,
    "text-ada-001": 2048,
    "davinci": 2048,
    "curie": 2048,
    "babbage": 2048,
    "ada": 2048,
    # P50K_EDIT models
    "text-davinci-edit-001": 4097,
    "code-davinci-edit-001": 4097,
}

# Default model to use if none specified
DEFAULT_MODEL = "gpt-4o"


def get_model_encoding(model_name: str) -> str:
    """Get the tiktoken encoding name for a given model.

    Args:
        model_name: Name of the model

    Returns:
        str: Encoding name for the model

    Raises:
        ValueError: If model is not supported
    """
    # Check for exact model match
    if model_name in MODEL_ENCODINGS:
        return MODEL_ENCODINGS[model_name]

    # Check for model prefix matches
    model_prefixes = {
        "o1-": Encoding.O200K_BASE,
        "chatgpt-4o-": Encoding.O200K_BASE,
        "gpt-4o-": Encoding.O200K_BASE,
        "gpt-4-": Encoding.CL100K_BASE,
        "gpt-3.5-turbo-": Encoding.CL100K_BASE,
        "gpt-35-turbo-": Encoding.CL100K_BASE,
        "ft:gpt-4": Encoding.CL100K_BASE,
        "ft:gpt-3.5-turbo": Encoding.CL100K_BASE,
    }

    for prefix, encoding in model_prefixes.items():
        if model_name.startswith(prefix):
            return encoding

    raise ValueError(f"Unsupported model: {model_name}")


def get_model_token_limit(model_name: str) -> int:
    """Get the token limit for a given model.

    Args:
        model_name: Name of the model

    Returns:
        int: Token limit for the model

    Raises:
        ValueError: If model is not supported
    """
    if model_name not in MODEL_TOKEN_LIMITS:
        raise ValueError(f"Unsupported model: {model_name}")
    return MODEL_TOKEN_LIMITS[model_name]
