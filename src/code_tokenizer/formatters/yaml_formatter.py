"""YAML formatter for code tokenizer output."""

from typing import Any, Dict, List, Optional

import yaml

from ..models.content import FileContent
from .base_formatter import BaseFormatter


class YAMLFormatter(BaseFormatter):
    """Formats tokenizer output as YAML."""

    def format_content(
        self,
        files: List[FileContent],
        stats: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Format content as YAML.

        Args:
            files: List of FileContent objects
            stats: Optional statistics dictionary
            metadata: Optional metadata dictionary

        Returns:
            str: YAML formatted content
        """
        output_data = {
            "files": [file.as_dict for file in files],
            "stats": stats or {},
            "metadata": metadata or {},
        }

        # Use safe_dump to avoid Python-specific tags
        # Use default_flow_style=False for better readability
        # Sort keys for consistent output
        # Use allow_unicode=True for proper handling of non-ASCII characters
        return yaml.safe_dump(
            output_data,
            default_flow_style=False,
            sort_keys=True,
            allow_unicode=True,
            indent=2,
            width=120,  # Wider line width for code content
            explicit_start=True,  # Add YAML document start marker
        ) 