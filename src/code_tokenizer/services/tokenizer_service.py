"""Service for tokenizing and processing code files."""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from pygments.lexers import guess_lexer_for_filename
from pygments.util import ClassNotFound

from ..core.tokenizer import CodeTokenizer
from ..utils.path_utils import get_gitignore_patterns, normalize_path, should_ignore_file


class TokenizerService:
    """Service for processing and tokenizing code files."""

    def __init__(self, config: Dict[str, Any]) -> None:
        """
        Initialize the tokenizer service.

        Args:
            config: Configuration dictionary with settings
        """
        self.base_dir = config.get("base_dir", ".")
        self.model_name = config.get("model_name", "claude-3-sonnet")
        self.max_tokens = config.get("max_tokens_per_file", 2000)
        self.output_format = config.get("output_format", "markdown")
        self.output_dir = config.get("output_dir", "output")
        self.include_metadata = config.get("include_metadata", True)
        self.bypass_gitignore = config.get("bypass_gitignore", False)

        self.tokenizer = CodeTokenizer(self.model_name)
        self.stats: Dict[str, Any] = {
            "files_processed": 0,
            "total_tokens": 0,
            "total_size": 0,
            "skipped_files": 0,
            "truncated_files": 0,
            "languages": {},
            "errors": [],
            "processed_files": [],
        }

    def detect_language(self, file_path: str, content: str) -> str:
        """
        Detect the programming language of a file.

        Args:
            file_path: Path to the file
            content: File content

        Returns:
            str: Detected language name
        """
        try:
            lexer = guess_lexer_for_filename(file_path, content)
            if hasattr(lexer, "aliases") and lexer.aliases:
                return lexer.aliases[0]
            return lexer.__class__.__name__.replace("Lexer", "")
        except ClassNotFound:
            return "text"

    def process_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        """
        Process a single file.

        Args:
            file_path: Path to the file to process

        Returns:
            Optional[Dict]: Processed file information or None if skipped
        """
        try:
            # Read file content
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Get file size
            size = os.path.getsize(file_path)

            # Detect language
            language = self.detect_language(file_path, content)

            # Update language stats
            self.stats["languages"][language] = self.stats["languages"].get(language, 0) + 1

            # Get token count
            token_count = self.tokenizer.count_tokens(content)

            # Update stats
            self.stats["total_tokens"] += token_count
            self.stats["total_size"] += size
            self.stats["files_processed"] += 1

            # Check if file needs truncation
            if self.max_tokens > 0 and token_count > self.max_tokens:
                content = self.tokenizer.truncate_to_token_limit(content, self.max_tokens)
                self.stats["truncated_files"] += 1

            return {
                "path": normalize_path(file_path),
                "language": language,
                "size": size,
                "tokens": token_count,
                "content": content,
            }

        except Exception as e:
            self.stats["errors"].append(f"Error processing {file_path}: {str(e)}")
            self.stats["skipped_files"] += 1
            return None

    def process_directory(self) -> Dict[str, Any]:
        """
        Process all files in the directory.

        Returns:
            Dict: Processing statistics and results
        """
        # Get gitignore patterns if not bypassing
        patterns = [] if self.bypass_gitignore else get_gitignore_patterns(self.base_dir)

        # Process all files
        for root, _, files in os.walk(self.base_dir):
            for file in files:
                file_path = os.path.join(root, file)

                # Skip if file should be ignored
                if not self.bypass_gitignore and should_ignore_file(
                    file_path, self.base_dir, patterns
                ):
                    self.stats["skipped_files"] += 1
                    continue

                # Process the file
                if result := self.process_file(file_path):
                    self.stats["processed_files"].append(result)

        return self.stats
