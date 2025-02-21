"""Markdown formatter for code tokenizer output."""

from typing import Any, Dict, List, Optional

from ..models.content import FileContent
from .base_formatter import BaseFormatter


class MarkdownFormatter(BaseFormatter):
    """Formats tokenizer output as Markdown."""

    def format_content(
        self,
        files: List[FileContent],
        stats: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Format content as Markdown.

        Args:
            files: List of FileContent objects
            stats: Optional statistics dictionary
            metadata: Optional metadata dictionary

        Returns:
            str: Markdown formatted content
        """
        lines = ["# Code Documentation\n"]

        # Add metadata section if provided
        if metadata:
            lines.append("## Metadata\n")
            for key, value in sorted(metadata.items()):
                lines.append(f"- **{key}**: {value}\n")
            lines.append("\n")

        # Add statistics section if provided
        if stats:
            lines.append("## Statistics\n")
            for key, value in sorted(stats.items()):
                if isinstance(value, dict):
                    lines.append(f"\n### {key.title()}\n")
                    for k, v in sorted(value.items()):
                        lines.append(f"- {k}: {v}\n")
                else:
                    lines.append(f"- **{key}**: {value}\n")
            lines.append("\n")

        # Add files section
        lines.append("## Files\n")
        for file in files:
            lines.extend(
                [
                    f"\n### {file.name}\n",
                    f"- **Path**: {file.path}\n",
                    f"- **Relative Path**: {file.relative_path}\n",
                    f"- **Language**: {file.language}\n",
                    f"- **Size**: {file.size} bytes\n",
                    f"- **Token Count**: {file.token_count}\n",
                    "\n```" + file.language.lower() + "\n",
                    file.content,
                    "```\n",
                ]
            )

        return "".join(lines) 