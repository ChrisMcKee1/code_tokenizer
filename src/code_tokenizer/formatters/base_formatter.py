"""Base formatter interface for code tokenizer output."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from ..models.content import FileContent


class BaseFormatter(ABC):
    """Base class for output formatters."""

    @abstractmethod
    def format_content(
        self,
        files: List[FileContent],
        stats: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Format content into a string.

        Args:
            files: List of FileContent objects
            stats: Optional statistics dictionary
            metadata: Optional metadata dictionary

        Returns:
            str: Formatted content
        """
        pass 