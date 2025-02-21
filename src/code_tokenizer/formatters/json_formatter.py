"""JSON formatter for code tokenizer output."""

import json
from typing import Any, Dict, List, Optional

from ..models.content import FileContent
from .base_formatter import BaseFormatter


class JSONFormatter(BaseFormatter):
    """Formats tokenizer output as JSON."""

    def format_content(
        self,
        files: List[FileContent],
        stats: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Format content as JSON.

        Args:
            files: List of FileContent objects
            stats: Optional statistics dictionary
            metadata: Optional metadata dictionary

        Returns:
            str: JSON formatted content
        """
        output_data = {
            "files": [file.as_dict for file in files],
            "stats": stats or {},
            "metadata": metadata or {},
        }

        return json.dumps(output_data, indent=2, sort_keys=True) 