"""Tokenizer service for processing code files."""

import json
import os
import sys
from collections import defaultdict
from typing import Any, Dict, List, Optional, Union, cast

from ..core.tokenizer import CodeTokenizer
from ..exceptions import TokenizationError
from ..models.model_config import TokenizerConfig
from ..services.filesystem_service import FileSystemService, RealFileSystemService
from ..services.language_detector import LanguageDetector
from ..ui.progress_display import ProgressDisplay
from ..utils.path_utils import should_ignore_file, should_ignore_path


def is_binary_file(content: bytes) -> bool:
    """
    Check if a file appears to be binary by looking for null bytes and non-printable characters.

    Args:
        content: File content to check in bytes

    Returns:
        bool: True if the file appears to be binary
    """
    # Check for null bytes first
    if b"\x00" in content:
        return True

    # Try to decode as UTF-8
    try:
        content.decode("utf-8")
        # Count non-printable characters (excluding whitespace)
        non_printable = sum(1 for byte in content if byte < 32 and byte not in (9, 10, 13))
        # If more than 30% of content is non-printable, consider it binary
        if non_printable > len(content) * 0.3:
            return True
        return False
    except UnicodeDecodeError:
        return True  # If we can't decode as UTF-8, it's binary


class TokenizerService:
    """Service for tokenizing code files."""

    MAX_FILE_SIZE = 1024 * 1024  # 1MB

    def __init__(
        self,
        config: Union[Dict[str, Any], TokenizerConfig],
        fs_service: Optional[FileSystemService] = None,
    ) -> None:
        """Initialize the tokenizer service.

        Args:
            config: Configuration for the tokenizer, either as a dict or TokenizerConfig
            fs_service: Optional file system service (defaults to RealFileSystemService)
        """
        if isinstance(config, dict):
            config = TokenizerConfig(config)

        self.config = config
        self.model_name = config.model_name
        self.max_tokens = config.max_tokens
        self.tokenizer = CodeTokenizer(self.model_name, self.max_tokens)
        self.language_detector = LanguageDetector()
        self.progress = ProgressDisplay()
        self.fs_service = fs_service or RealFileSystemService()
        self.stats: Dict[str, int] = {
            "total_files": 0,
            "files_processed": 0,
            "total_tokens": 0,
            "errors": 0,
        }
        self.ignore_patterns = []

        # Load gitignore patterns from .gitignore file if it exists and base_dir is set
        if not self.config.bypass_gitignore and self.config.base_dir:
            gitignore_path = os.path.join(self.config.base_dir, ".gitignore")
            if self.fs_service.is_file(gitignore_path):
                content = self.fs_service.read_file(gitignore_path)
                if isinstance(content, bytes):
                    content = content.decode("utf-8")
                self.ignore_patterns = [
                    line.strip()
                    for line in content.splitlines()
                    if line.strip() and not line.startswith("#")
                ]

    def process_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Process a single file.

        Args:
            file_path (str): Path to the file to process

        Returns:
            Optional[Dict[str, Any]]: File processing statistics or None if file should be skipped
        """
        try:
            # Check if file exists and is readable
            if not self.fs_service.exists(file_path):
                print(f"File not found: {file_path}", file=sys.stderr)
                return {
                    "success": False,
                    "path": file_path,
                    "language": "unknown",
                    "size": 0,
                    "tokens": 0,
                    "error": "File not found",
                }

            if not self.fs_service.is_file(file_path):
                print(f"Not a file: {file_path}", file=sys.stderr)
                return {
                    "success": False,
                    "path": file_path,
                    "language": "unknown",
                    "size": 0,
                    "tokens": 0,
                    "error": "Not a file",
                }

            # Get file extension and check if it should be processed
            filename = os.path.basename(file_path)
            _, ext = os.path.splitext(filename)
            ext = ext.lstrip(".")

            # Skip files that should be ignored based on extension
            if not self.config.bypass_gitignore and self.config.base_dir and should_ignore_file(
                file_path, self.config.base_dir, self.ignore_patterns
            ):
                return None

            # Check file size
            file_size = self.fs_service.get_file_size(file_path)
            if file_size > self.MAX_FILE_SIZE:
                print(f"File too large: {file_path}", file=sys.stderr)
                return None

            # Read file content
            content = self.fs_service.read_file(file_path)

            # Check for binary content first
            if isinstance(content, bytes):
                if is_binary_file(content):
                    print(f"Skipping binary file: {file_path}", file=sys.stderr)
                    return None
                try:
                    content = content.decode("utf-8")
                except UnicodeDecodeError:
                    print(f"Skipping binary file: {file_path}", file=sys.stderr)
                    return None

            # Only process text content
            language = self.language_detector.detect_language(content, filename)
            tokens = self.tokenizer.count_tokens(content)

            return {
                "success": True,
                "path": file_path,
                "language": language,
                "size": file_size,
                "tokens": tokens,
            }

        except Exception as e:
            print(f"Error processing file {file_path}: {str(e)}", file=sys.stderr)
            return {
                "success": False,
                "path": file_path,
                "language": "unknown",
                "size": 0,
                "tokens": 0,
                "error": str(e),
            }

    def process_directory(
        self, directory: str, output_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """Process all files in a directory.

        Args:
            directory: Directory to process
            output_path: Optional path to write output to

        Returns:
            Dict containing processing results and statistics
        """
        # Initialize statistics
        stats: Dict[str, Union[int, Dict[str, int]]] = {
            "files_processed": 0,
            "skipped_files": 0,
            "truncated_files": 0,
            "total_tokens": 0,
            "total_size": 0,
            "languages": defaultdict(int)
        }
        successful_files: List[str] = []
        failed_files: List[str] = []

        try:
            # Get list of files
            files = self.fs_service.list_files(directory, recursive=True)

            # Process each file
            for file_path in files:
                try:
                    # Get relative path
                    rel_path = os.path.relpath(file_path, directory).replace(os.sep, "/")

                    # Skip files matching ignore patterns only if not bypassing gitignore
                    if not self.config.bypass_gitignore:
                        if should_ignore_path(rel_path, self.ignore_patterns)[0]:
                            stats["skipped_files"] = cast(int, stats["skipped_files"]) + 1
                            continue

                    # Process file
                    file_stats = self.process_file(file_path)
                    if file_stats:
                        stats["files_processed"] = cast(int, stats["files_processed"]) + 1
                        stats["total_tokens"] = cast(int, stats["total_tokens"]) + file_stats["tokens"]
                        stats["total_size"] = cast(int, stats["total_size"]) + file_stats["size"]
                        languages = cast(Dict[str, int], stats["languages"])
                        languages[file_stats["language"]] += 1
                        if file_stats.get("truncated", False):
                            stats["truncated_files"] = cast(int, stats["truncated_files"]) + 1
                        successful_files.append(rel_path)
                    else:
                        # If bypass_gitignore is True, try to process binary files
                        if self.config.bypass_gitignore:
                            try:
                                # Get file size
                                size = self.fs_service.get_file_size(file_path)
                                # Add as binary file
                                stats["files_processed"] = cast(int, stats["files_processed"]) + 1
                                stats["total_size"] = cast(int, stats["total_size"]) + size
                                languages = cast(Dict[str, int], stats["languages"])
                                languages["Binary"] += 1
                                successful_files.append(rel_path)
                                continue
                            except Exception:
                                pass
                        failed_files.append(rel_path)
                except Exception as e:
                    failed_files.append(rel_path)
                    print(f"Warning: Failed to process {rel_path}: {str(e)}")

            # Write output if path provided
            if output_path:
                result = {
                    "stats": stats,
                    "successful_files": successful_files,
                    "failed_files": failed_files,
                    "model": self.config.model_name,
                }
                self.write_output(output_path, result)

            return {
                "stats": stats,
                "successful_files": successful_files,
                "failed_files": failed_files,
                "model": self.config.model_name,
            }

        except Exception as e:
            raise TokenizationError(f"Failed to process directory: {str(e)}")

    def get_stats(self) -> Dict[str, int]:
        """Get tokenization statistics.

        Returns:
            Dictionary containing tokenization statistics
        """
        return self.stats.copy()

    def reset_stats(self) -> None:
        """Reset tokenization statistics."""
        self.stats = {
            "total_files": 0,
            "files_processed": 0,
            "total_tokens": 0,
            "errors": 0,
        }

    def write_output(self, output_path: str, data: Dict[str, Any]) -> None:
        """Write output to a file.

        Args:
            output_path (str): Path to write output to
            data (Dict[str, Any]): Data to write

        Raises:
            TokenizationError: If writing fails
        """
        try:
            # Create output directory if it doesn't exist
            output_dir = os.path.dirname(output_path)
            if output_dir:
                self.fs_service.create_directory(output_dir)

            # Extract data
            stats = data.get("stats", {})
            successful_files = data.get("successful_files", [])
            failed_files = data.get("failed_files", [])
            model_name = data.get("model", self.config.model_name)

            # Prepare output data
            output_data = {
                "stats": stats,
                "files": successful_files,
                "failed_files": failed_files,
                "metadata": {
                    "model": model_name,
                    "max_tokens": self.config.max_tokens,
                    "bypass_gitignore": self.config.bypass_gitignore,
                },
            }

            # Write output based on format
            if output_path.endswith(".json"):
                self.fs_service.write_file(output_path, json.dumps(output_data, indent=2))
            else:
                # Generate markdown output
                markdown = [
                    "# Code Documentation\n",
                    f"## Model: {model_name}\n",
                    "## Statistics\n",
                    f"- Files processed: {stats.get('files_processed', 0)}\n",
                    f"- Total tokens: {stats.get('total_tokens', 0):,}\n",
                    f"- Total size: {stats.get('total_size', 0):,} bytes\n",
                    f"- Skipped files: {stats.get('skipped_files', 0)}\n",
                    f"- Truncated files: {stats.get('truncated_files', 0)}\n",
                    "\n## Languages\n",
                ]

                for lang, count in stats.get("languages", {}).items():
                    markdown.append(f"- {lang}: {count} files\n")

                if successful_files and self.config.include_metadata:
                    markdown.append("\n## Processed Files\n")
                    for file_path in successful_files:
                        markdown.append(f"- {file_path}\n")

                if failed_files:
                    markdown.append("\n## Failed Files\n")
                    for file_path in failed_files:
                        markdown.append(f"- {file_path}\n")

                self.fs_service.write_file(output_path, "".join(markdown))
        except Exception as e:
            raise TokenizationError(f"Failed to write output: {str(e)}")

    def read_ignore_patterns(self, directory: str) -> List[str]:
        """Read ignore patterns from .gitignore file.

        Args:
            directory: Directory containing .gitignore file

        Returns:
            List of ignore patterns
        """
        try:
            # Read .gitignore file
            gitignore_path = os.path.join(directory, ".gitignore")
            if self.fs_service.exists(gitignore_path):
                content = self.fs_service.read_file(gitignore_path)
                if isinstance(content, bytes):
                    content = content.decode("utf-8")
                lines = [line.strip() for line in content.splitlines()]
                return [line for line in lines if line and not line.startswith("#")]
            return []
        except Exception as e:
            print(f"Warning: Failed to read .gitignore: {str(e)}")
            return []

    def should_ignore_file(self, file_path: str, base_path: str) -> bool:
        """Check if a file should be ignored based on patterns.

        Args:
            file_path: Path to file
            base_path: Base path for relative path calculation

        Returns:
            True if file should be ignored, False otherwise
        """
        if not base_path:
            return False

        try:
            # Get relative path
            rel_path = os.path.relpath(file_path, base_path).replace(os.sep, "/")
            return should_ignore_path(rel_path, self.ignore_patterns)[0]
        except Exception:
            return False

    @classmethod
    def from_config(
        cls, config: Dict[str, Any], fs_service: Optional[FileSystemService] = None
    ) -> "TokenizerService":
        """Create a TokenizerService instance from a configuration dictionary.

        Args:
            config (Dict[str, Any]): Configuration dictionary
            fs_service (Optional[FileSystemService]): Optional file system service

        Returns:
            TokenizerService: Configured tokenizer service instance
        """
        return cls(TokenizerConfig(config), fs_service)
