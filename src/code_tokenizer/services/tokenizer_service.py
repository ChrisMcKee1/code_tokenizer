"""Main service for code tokenization and processing."""

import os
from typing import Dict, List, Optional, Tuple, Any
from pygments.lexers import get_lexer_for_filename
from pygments.util import ClassNotFound
from pathlib import Path

from rich.live import Live

from ..core.tokenizer import count_tokens, truncate_text
from ..models.model_config import get_model_token_limit, DEFAULT_MODEL
from ..services.language_detector import LanguageDetector
from ..ui.progress_display import (
    create_display_layout,
    create_progress_group,
    create_stats_table,
    update_display
)
from ..utils.path_utils import get_relative_path, normalize_path, should_ignore_path


class TokenizerService:
    """Service for processing and tokenizing code files."""

    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize the TokenizerService."""
        self.base_dir = config["base_dir"]
        self.model_name = config.get("model_name", DEFAULT_MODEL)
        self.max_tokens = config.get("max_tokens_per_file", 2000)
        self.output_format = config.get("output_format", "markdown")
        self.output_dir = config.get("output_dir", "output")
        self.include_metadata = config.get("include_metadata", True)
        self.disable_progress = config.get("disable_progress", False)
        
        # Initialize statistics
        self.stats = {
            "files_processed": 0,
            "total_tokens": 0,
            "total_size": 0,
            "skipped_files": 0,
            "truncated_files": 0,
            "languages": {}
        }
        
        # Initialize error list
        self.errors: list[str] = []
        
        # Load gitignore patterns
        self.ignore_patterns = [
            "*.pyc",
            "__pycache__/",
            "*.log",
            ".git/",
            ".env",
            "venv/",
            "node_modules/",
            "dist/",
            "build/"
        ]
        
        # Add custom gitignore patterns if provided
        custom_gitignore = config.get("custom_gitignore")
        if custom_gitignore and Path(custom_gitignore).exists():
            with open(custom_gitignore) as f:
                patterns = [p.strip() for p in f.readlines() if p.strip() and not p.startswith("#")]
                self.ignore_patterns.extend(patterns)

    def process_file(self, file_path: str) -> Dict[str, Any]:
        """
        Process a single file, detecting language and counting tokens.
        
        Args:
            file_path: Path to the file to process
            
        Returns:
            Dict[str, Any]: Processing results containing success, language, tokens, and any errors
        """
        try:
            # Get relative path for display
            rel_path = get_relative_path(file_path, self.base_dir)
            
            # Check if file should be ignored
            should_ignore, reason = should_ignore_path(rel_path, self.ignore_patterns)
            if should_ignore:
                self.stats["skipped_files"] += 1
                self.errors.append(f"Skipped {rel_path}: {reason}")
                return {
                    "success": False,
                    "language": "unknown",
                    "tokens": 0,
                    "error": reason
                }
            
            # Read file content
            content = self._read_file(file_path)
            if not content:
                self.stats["skipped_files"] += 1
                self.errors.append(f"Empty or unreadable file: {rel_path}")
                return {
                    "success": False,
                    "language": "unknown",
                    "tokens": 0,
                    "error": "Empty or unreadable file"
                }
            
            # Detect language
            language = LanguageDetector.detect_language(file_path)
            
            # Count tokens
            token_count = count_tokens(content, self.model_name)
            
            # Check if truncation is needed
            if token_count > self.max_tokens and self.max_tokens > 0:
                content, token_count = truncate_text(content, self.max_tokens, self.model_name)
                self.stats["truncated_files"] += 1
            
            # Update statistics
            self.stats["files_processed"] += 1
            self.stats["total_tokens"] += token_count
            self.stats["total_size"] += len(content)
            self.stats["languages"][language] = self.stats["languages"].get(language, 0) + 1
            
            return {
                "success": True,
                "language": language,
                "tokens": token_count,
                "content": content
            }
            
        except Exception as e:
            error_msg = str(e)
            self.errors.append(f"Error processing {file_path}: {error_msg}")
            return {
                "success": False,
                "language": "unknown",
                "tokens": 0,
                "error": error_msg
            }

    def _read_file(self, file_path: str) -> str:
        """Read file content with proper encoding detection."""
        # First check if it's a binary file
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(1024)  # Read first 1KB
                if b'\x00' in chunk:  # Simple binary check
                    raise ValueError("Binary file detected")
                
            # If not binary, read as text
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except UnicodeDecodeError:
            raise ValueError("Binary or non-UTF8 file detected")

    def _count_tokens(self, text: str) -> int:
        """Count tokens in text using the configured model."""
        # Implementation here
        return len(text.split())

    def _detect_language(self, file_path: str) -> str:
        """Detect the programming language of a file."""
        try:
            lexer = get_lexer_for_filename(file_path, '')
            return lexer.name
        except ClassNotFound:
            return "text"

    def process_directory(self) -> Dict:
        """
        Process all files in the base directory.

        Returns:
            Dict: Processing statistics and file contents
        """
        # Get list of files to process
        all_files = []
        processed_files = []
        for root, _, files in os.walk(self.base_dir):
            for file in files:
                file_path = os.path.join(root, file)
                all_files.append(file_path)

        if self.disable_progress:
            # Simple processing without progress display
            for file_path in all_files:
                result = self.process_file(file_path)
                if result["success"]:
                    processed_files.append({
                        "path": get_relative_path(file_path, self.base_dir),
                        "language": result["language"],
                        "tokens": result["tokens"],
                        "content": result.get("content", ""),
                        "size": len(result.get("content", ""))
                    })
        else:
            # Create progress display
            layout = create_display_layout()
            progress = create_progress_group()
            task_id = progress.add_task("[cyan]Processing files...", total=len(all_files))

            # Process files with live display
            with Live(layout, refresh_per_second=10):
                for file_path in all_files:
                    rel_path = get_relative_path(file_path, self.base_dir)
                    result = self.process_file(file_path)

                    # Update display
                    status = f"Processing: {rel_path}"
                    if result["success"]:
                        status += f" ({result['language']})"
                        processed_files.append({
                            "path": rel_path,
                            "language": result["language"],
                            "tokens": result["tokens"],
                            "content": result.get("content", ""),
                            "size": len(result.get("content", ""))
                        })

                    update_display(
                        layout,
                        progress,
                        self.stats,
                        current_file=rel_path,
                        status=status,
                        errors=self.errors,
                    )

                    progress.advance(task_id)

        # Add processed files to stats
        self.stats["processed_files"] = processed_files
        return self.stats
