"""Custom exceptions for the code tokenizer."""


class TokenizerError(Exception):
    """Base class for tokenizer errors."""

    pass


class ModelNotSupportedError(TokenizerError):
    """Raised when the model is not supported."""

    pass


class EncodingNotSupportedError(TokenizerError):
    """Raised when the encoding is not supported."""

    pass


class TokenizationError(TokenizerError):
    """Exception raised when tokenization fails."""

    pass


class FileProcessingError(TokenizerError):
    """Raised when there is an error processing a file."""

    pass


class DirectoryProcessingError(TokenizerError):
    """Raised when there is an error processing a directory."""

    pass


class LanguageDetectionError(TokenizerError):
    """Raised when there is an error detecting the language of a file."""

    pass
