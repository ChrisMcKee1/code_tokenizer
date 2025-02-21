"""Models for file content and metadata."""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Literal, Union

from typing_extensions import TypeAlias

# Type definitions
PathLike: TypeAlias = Union[str, Path]
SupportedEncodings: TypeAlias = Literal["utf-8", "utf-16", "ascii", "latin-1"]
ContentDict: TypeAlias = Dict[str, Union[str, int]]


@dataclass(frozen=True)
class FileContent:
    """Model representing a processed file's content and metadata.

    Attributes:
        name: File name without path
        path: Absolute path to file
        relative_path: Path relative to project root
        language: Programming language
        token_count: Number of tokens in content
        content: File content (sanitized)
        size: Content size in bytes
        encoding: File encoding used
    """

    name: str
    path: str
    relative_path: str
    language: str
    token_count: int
    content: str
    size: int
    encoding: SupportedEncodings

    def __post_init__(self) -> None:
        """Validate and normalize paths after initialization."""
        # Normalize paths to use forward slashes
        object.__setattr__(self, "path", self._normalize_path(self.path))
        object.__setattr__(self, "relative_path", self._normalize_path(self.relative_path))

        # Validate encoding
        if self.encoding not in ("utf-8", "utf-16", "ascii", "latin-1"):
            raise ValueError(f"Unsupported encoding: {self.encoding}")

    @staticmethod
    def _normalize_path(path: str) -> str:
        """Normalize path separators to forward slashes.

        Args:
            path: Path to normalize

        Returns:
            str: Normalized path using forward slashes
        """
        return path.replace(os.sep, "/")

    @classmethod
    def from_path(
        cls,
        file_path: PathLike,
        root_dir: PathLike,
        content: str,
        language: str,
        token_count: int,
        encoding: SupportedEncodings = "utf-8",
    ) -> "FileContent":
        """Create FileContent instance from a file path.

        Args:
            file_path: Path to the file
            root_dir: Project root directory
            content: File content
            language: Detected language
            token_count: Number of tokens
            encoding: File encoding (default: utf-8)

        Returns:
            FileContent: New instance with file information

        Raises:
            ValueError: If paths are invalid or encoding is unsupported
        """
        file_path = Path(file_path)
        root_dir = Path(root_dir)

        try:
            return cls(
                name=file_path.name,
                path=str(file_path.absolute()),
                relative_path=str(file_path.relative_to(root_dir)),
                language=language,
                token_count=token_count,
                content=content,
                size=len(content.encode(encoding)),
                encoding=encoding,
            )
        except Exception as e:
            raise ValueError(f"Failed to create FileContent: {str(e)}") from e

    @property
    def as_dict(self) -> ContentDict:
        """Convert to dictionary for serialization.

        Returns:
            ContentDict: Dictionary representation with normalized paths
        """
        return {
            "name": self.name,
            "path": self.path,
            "relative_path": self.relative_path,
            "language": self.language,
            "token_count": self.token_count,
            "content": self.content,
            "size": self.size,
            "encoding": self.encoding,
        }

    def __str__(self) -> str:
        """String representation without content for logging.

        Returns:
            str: Human-readable representation
        """
        return f"{self.name} ({self.language}): {self.token_count} tokens, {self.size} bytes"
