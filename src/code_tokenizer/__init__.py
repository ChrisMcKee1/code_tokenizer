"""Code tokenizer package for processing and counting tokens in code files."""

import os
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv

# Load .env file from the project root
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(env_path)

# Version
try:
    from code_tokenizer._version import __version__  # type: ignore
except ImportError:  # pragma: no cover
    # Package is not installed, version is unknown
    __version__ = "0.0.0"

__all__ = ["__version__"]

# Configuration with defaults
config: Dict[str, Any] = {
    # Default settings
    "DEFAULT_MODEL": os.getenv("DEFAULT_MODEL", "gpt-4o"),
    "DEFAULT_MAX_TOKENS": int(os.getenv("DEFAULT_MAX_TOKENS", "2000")),
    "DEFAULT_OUTPUT_FORMAT": os.getenv("DEFAULT_OUTPUT_FORMAT", "markdown"),
    # Performance settings
    "BATCH_SIZE": int(os.getenv("BATCH_SIZE", "100")),
    "PROGRESS_REFRESH_RATE": int(os.getenv("PROGRESS_REFRESH_RATE", "10")),
    # Debug settings
    "DEBUG": os.getenv("DEBUG", "false").lower() == "true",
    "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),
    # File processing
    "DEFAULT_ENCODING": os.getenv("DEFAULT_ENCODING", "utf-8"),
    "BINARY_DETECTION_THRESHOLD": float(os.getenv("BINARY_DETECTION_THRESHOLD", "0.3")),
    # API keys (if needed in future)
    "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", ""),
    "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY", ""),
}
