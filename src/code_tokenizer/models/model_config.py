"""Model configuration and encoding mappings."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set

# Default model configuration values
DEFAULT_MODEL = "gpt-4o"
DEFAULT_MAX_TOKENS = 200000
DEFAULT_OUTPUT_FORMAT = "markdown"


@dataclass
class TokenizerConfig:
    """Configuration for the tokenizer service."""

    model_name: str = DEFAULT_MODEL
    max_tokens: int = DEFAULT_MAX_TOKENS
    base_dir: Optional[str] = None
    output_dir: Optional[str] = None
    output_format: str = DEFAULT_OUTPUT_FORMAT
    bypass_gitignore: bool = False
    include_metadata: bool = True
    ignore_patterns: List[str] = field(default_factory=list)
    file_extensions: Set[str] = field(default_factory=set)
    skip_extensions: Set[str] = field(default_factory=set)
    show_progress: bool = True
    verbose: bool = False
    debug: bool = False

    def __init__(self, config_dict: Optional[Dict[str, Any]] = None) -> None:
        """Initialize the configuration.

        Args:
            config_dict: Optional dictionary with configuration values
        """
        if config_dict is None:
            config_dict = {}

        self.model_name = config_dict.get("model_name", DEFAULT_MODEL)
        self.max_tokens = config_dict.get("max_tokens", DEFAULT_MAX_TOKENS)
        self.base_dir = config_dict.get("base_dir")
        self.output_dir = config_dict.get("output_dir")
        self.output_format = config_dict.get("output_format", DEFAULT_OUTPUT_FORMAT)
        self.bypass_gitignore = config_dict.get("bypass_gitignore", False)
        self.include_metadata = config_dict.get("include_metadata", True)
        self.ignore_patterns = config_dict.get("ignore_patterns", [])
        self.show_progress = config_dict.get("show_progress", True)
        self.verbose = config_dict.get("verbose", False)
        self.debug = config_dict.get("debug", False)

        # When bypass_gitignore is True, we don't use any extension filters
        if self.bypass_gitignore:
            self.file_extensions = set()
            self.skip_extensions = set()
        else:
            # Handle file_extensions
            file_extensions = config_dict.get("file_extensions")
            if file_extensions is None:
                # Use default extensions
                file_extensions = {
                    "py",
                    "js",
                    "ts",
                    "jsx",
                    "tsx",  # Code files
                    "json",
                    "yaml",
                    "yml",  # Config files
                    "txt",
                    "md",  # Documentation
                    "html",
                    "css",
                    "scss",  # Web files
                    "sh",
                    "bash",  # Shell scripts
                    "xml",
                    "ini",
                    "conf",  # Other config files
                    "gitignore",
                    ".gitignore",  # Special files
                    "env",  # Environment files
                    "cs",
                    "java",
                    "go",
                    "rs",  # Other languages
                }
            else:
                # Convert to set and strip dots
                file_extensions = {ext.lstrip(".") for ext in file_extensions}
            self.file_extensions = file_extensions

            # Handle skip_extensions
            skip_extensions = config_dict.get("skip_extensions")
            if skip_extensions is None:
                # Use default skip_extensions
                skip_extensions = {
                    "pyc",
                    "pyo",
                    "pyd",  # Python bytecode
                    "dll",
                    "so",
                    "dylib",  # Binary libraries
                    "exe",
                    "bin",
                    "obj",  # Executables and object files
                    "class",
                    "jar",  # Java bytecode
                    "png",
                    "jpg",
                    "jpeg",
                    "gif",
                    "ico",  # Images
                    "pdf",
                    "doc",
                    "docx",
                    "xls",
                    "xlsx",  # Documents
                    "zip",
                    "tar",
                    "gz",
                    "7z",
                    "rar",  # Archives
                }
            else:
                # Convert to set and strip dots
                skip_extensions = {ext.lstrip(".") for ext in skip_extensions}
            self.skip_extensions = skip_extensions

    def to_dict(self) -> Dict[str, Any]:
        """Convert the configuration to a dictionary.

        Returns:
            Dict[str, Any]: Dictionary representation of the configuration
        """
        return {
            "model_name": self.model_name,
            "max_tokens": self.max_tokens,
            "base_dir": self.base_dir,
            "output_dir": self.output_dir,
            "output_format": self.output_format,
            "bypass_gitignore": self.bypass_gitignore,
            "include_metadata": self.include_metadata,
            "ignore_patterns": self.ignore_patterns,
            "file_extensions": list(self.file_extensions) if self.file_extensions else None,
            "skip_extensions": list(self.skip_extensions) if self.skip_extensions else None,
            "show_progress": self.show_progress,
            "verbose": self.verbose,
            "debug": self.debug,
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
