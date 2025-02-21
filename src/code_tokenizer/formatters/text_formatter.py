"""Text formatter for code content."""

from typing import Dict, List, Optional

from .base_formatter import BaseFormatter
from ..models.content import FileContent


class TextFormatter(BaseFormatter):
    """Formats code content as plain text."""

    def format_content(
        self,
        files: List[FileContent],
        stats: Optional[Dict] = None,
        metadata: Optional[Dict] = None,
    ) -> str:
        """Format code content as plain text.
        
        Args:
            files: List of FileContent objects containing code content
            stats: Optional statistics about the code
            metadata: Optional metadata about the processing
            
        Returns:
            Formatted text string
        """
        lines = []
        
        # Header
        lines.append("Code Documentation")
        lines.append("=" * 80)
        lines.append("")
        
        # Metadata section if provided
        if metadata:
            lines.append("Metadata:")
            lines.append("-" * 40)
            for key, value in metadata.items():
                lines.append(f"{key}: {value}")
            lines.append("")
            
        # Stats section if provided
        if stats:
            lines.append("Statistics:")
            lines.append("-" * 40)
            for key, value in stats.items():
                lines.append(f"{key}: {value}")
            lines.append("")
            
        # Files section
        lines.append("Files:")
        lines.append("-" * 40)
        
        for file in files:
            lines.append(f"Path: {file.name}")
            lines.append(f"Language: {file.language}")
            lines.append(f"Size: {len(file.content)} bytes")
            lines.append("")
            lines.append("Content:")
            lines.append("-" * 8)
            lines.append(file.content)
            lines.append("")
            
        return "\n".join(lines) 