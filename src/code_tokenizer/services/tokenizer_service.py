"""Tokenizer service for processing code files."""

import json
import logging
import os
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List, Optional, Union, cast

from ..core.sanitizer import ContentSanitizer
from ..core.tokenizer import CodeTokenizer
from ..environment import environment
from ..exceptions import TokenizationError
from ..models.content import FileContent
from ..models.model_config import TokenizerConfig
from ..services.filesystem_service import FileSystemService, RealFileSystemService
from ..services.language_detector import LanguageDetector
from ..ui.progress_display import ProgressDisplay
from ..utils.path_utils import should_ignore_path

# Configure logging
logger = logging.getLogger(__name__)

# Constants
MAX_WORKERS = 4  # Maximum number of threads for parallel processing
CHUNK_SIZE = 1024 * 1024  # 1MB chunk size for file reading
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


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
        return True


class TokenizerService:
    """Service for tokenizing code files."""

    def __init__(
        self,
        config: Union[Dict[str, Any], TokenizerConfig],
        fs_service: Optional[FileSystemService] = None
    ) -> None:
        """Initialize the tokenizer service.

        Args:
            config: Configuration dictionary or TokenizerConfig instance
            fs_service: Optional file system service
        """
        # Convert config dict to TokenizerConfig if needed
        if isinstance(config, dict):
            self.config = TokenizerConfig(config)
        else:
            self.config = config

        self.tokenizer = CodeTokenizer(self.config.model_name)
        self.sanitizer = ContentSanitizer()
        self.fs_service = fs_service or RealFileSystemService()
        self.language_detector = LanguageDetector()
        self.progress = ProgressDisplay()
        self.executor: Optional[ThreadPoolExecutor] = None
        self.stats = {
            "files_processed": 0,
            "total_tokens": 0,
            "total_size": 0,
            "languages": defaultdict(int),
            "errors": 0,
            "failed_files": []
        }

    def process_directory(self, directory: str, **kwargs) -> Dict[str, Any]:
        """Process all files in a directory.

        Args:
            directory: Directory path to process
            **kwargs: Additional keyword arguments (ignored)

        Returns:
            Dict containing processing results and statistics
        """
        stats: Dict[str, Any] = {
            "files_processed": 0,
            "total_tokens": 0,
            "total_size": 0,
            "languages": defaultdict(int),
            "failed_files": []
        }
        successful_files: List[str] = []
        failed_files: List[str] = []

        try:
            # Get all files in directory
            files = self.fs_service.get_files_in_directory(directory)
            total_files = len(files)

            if total_files == 0:
                logger.warning(f"No files found in directory: {directory}")
                return {"stats": stats}

            # Process files in chunks
            chunk_size = min(total_files, MAX_WORKERS * 2)
            chunks = [files[i:i + chunk_size] for i in range(0, total_files, chunk_size)]

            # Process chunks
            if environment.is_testing():
                # Process sequentially in test environment
                for chunk in chunks:
                    for file_path in chunk:
                        result = self.process_file(file_path)
                        if result:
                            stats["files_processed"] += 1
                            stats["total_tokens"] += result["tokens"]
                            stats["total_size"] += result["size"]
                            stats["languages"][result["language"]] += 1
                            successful_files.append(file_path)
                        else:
                            failed_files.append(file_path)
            else:
                # Process in parallel in other environments
                with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                    self.executor = executor
                    futures = {}
                    for chunk in chunks:
                        for file_path in chunk:
                            future = executor.submit(
                                self.process_file,
                                file_path
                            )
                            futures[future] = file_path

                    # Collect results
                    for future in as_completed(futures):
                        file_path = futures[future]
                        try:
                            result = future.result()
                            if result:
                                stats["files_processed"] += 1
                                stats["total_tokens"] += result["tokens"]
                                stats["total_size"] += result["size"]
                                stats["languages"][result["language"]] += 1
                                successful_files.append(file_path)
                            else:
                                failed_files.append(file_path)
                        except Exception as e:
                            logger.error(f"Error processing {file_path}: {str(e)}")
                            failed_files.append(file_path)

                        # Update progress
                        self.progress.update_progress(
                            len(successful_files) + len(failed_files),
                            total_files
                        )

            # Prepare output data
            output_data = {
                "stats": stats,
                "successful_files": successful_files,
                "failed_files": failed_files,
                "model": self.config.model_name,
                "metadata": {
                    "max_tokens": self.config.max_tokens,
                    "bypass_gitignore": self.config.bypass_gitignore,
                    "sanitize_content": self.config.sanitize_content,
                }
            }

            # Write output if output_path is provided
            output_path = kwargs.get("output_path")
            if output_path:
                self.write_output(output_path, output_data)

            return output_data

        except Exception as e:
            logger.error(f"Error processing directory: {str(e)}")
            raise TokenizationError(f"Failed to process directory: {str(e)}")
        finally:
            if self.executor:
                self.executor.shutdown()

    def _process_file_chunk(self, chunk: bytes, file_path: str) -> Optional[Dict[str, Any]]:
        """Process a chunk of file content."""
        try:
            # Check for binary content
            if is_binary_file(chunk):
                logger.debug(f"Skipping binary chunk in file: {file_path}")
                return None

            # Decode content
            try:
                content = chunk.decode("utf-8")
            except UnicodeDecodeError:
                logger.debug(f"Failed to decode chunk in file: {file_path}")
                return None

            # Detect language
            language = self.language_detector.detect_language(content, file_path)

            # Sanitize content if enabled
            if self.config.sanitize_content:
                content = self.sanitizer.clean_content(content, language)

            # Process content
            tokens = self.tokenizer.count_tokens(content)

            return {
                "language": language,
                "tokens": tokens,
                "size": len(chunk),
                "content": content,
            }

        except Exception as e:
            logger.warning(f"Error processing chunk in {file_path}: {str(e)}")
            return None

    def process_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Process a single file."""
        try:
            # Validate file
            if not self.fs_service.exists(file_path):
                logger.warning(f"File not found: {file_path}")
                return None

            if not self.fs_service.is_file(file_path):
                logger.warning(f"Not a file: {file_path}")
                return None

            # Check file size
            file_size = self.fs_service.get_file_size(file_path)
            if file_size > self.MAX_FILE_SIZE:
                logger.warning(f"File too large: {file_path}")
                return None

            # Read and process file in chunks
            chunks = []
            offset = 0
            while offset < file_size:
                chunk = self.fs_service.read_file_chunk(file_path, offset, CHUNK_SIZE)
                if not chunk:
                    break
                chunks.append(chunk)
                offset += len(chunk)

            # Process chunks based on environment
            results = []
            if environment.is_testing() or environment.is_development():
                # Process sequentially in test/dev mode
                for chunk in chunks:
                    # In bypass mode, we still want to process binary files
                    if self.config.bypass_gitignore:
                        try:
                            content = chunk.decode("utf-8", errors="ignore")
                            language = self.language_detector.detect_language(content, file_path)

                            # Sanitize content if enabled
                            if self.config.sanitize_content:
                                content = self.sanitizer.clean_content(content, language)

                            tokens = self.tokenizer.count_tokens(content)
                            results.append(
                                {
                                    "language": language,
                                    "tokens": tokens,
                                    "size": len(chunk),
                                    "content": content,
                                }
                            )
                        except Exception as e:
                            logger.debug(f"Error processing chunk in {file_path}: {str(e)}")
                            continue
                    else:
                        # Normal mode - skip binary files
                        if is_binary_file(chunk):
                            logger.debug(f"Skipping binary chunk in file: {file_path}")
                            continue
                        try:
                            content = chunk.decode("utf-8")
                            language = self.language_detector.detect_language(content, file_path)

                            # Sanitize content if enabled
                            if self.config.sanitize_content:
                                content = self.sanitizer.clean_content(content, language)

                            tokens = self.tokenizer.count_tokens(content)
                            results.append(
                                {
                                    "language": language,
                                    "tokens": tokens,
                                    "size": len(chunk),
                                    "content": content,
                                }
                            )
                        except Exception as e:
                            logger.debug(f"Error processing chunk in {file_path}: {str(e)}")
                            continue
            else:
                # Process in parallel in other environments
                futures = {}
                for chunk in chunks:
                    if self.config.bypass_gitignore:
                        # In bypass mode, process all files
                        future = self._executor.submit(
                            lambda c: {
                                "language": self.language_detector.detect_language(
                                    c.decode("utf-8", errors="ignore"), file_path
                                ),
                                "tokens": self.tokenizer.count_tokens(
                                    self.sanitizer.clean_content(
                                        c.decode("utf-8", errors="ignore"),
                                        self.language_detector.detect_language(
                                            c.decode("utf-8", errors="ignore"), file_path
                                        ),
                                    )
                                    if self.config.sanitize_content
                                    else c.decode("utf-8", errors="ignore")
                                ),
                                "size": len(c),
                                "content": c.decode("utf-8", errors="ignore"),
                            },
                            chunk,
                        )
                        futures[future] = rel_path
                    else:
                        # Normal mode - skip binary files
                        if not is_binary_file(chunk):
                            future = self._executor.submit(
                                self._process_file_chunk, chunk, file_path
                            )
                            futures[future] = rel_path

                # Collect results
                for future in as_completed(futures):
                    rel_path = futures[future]
                    try:
                        file_stats = future.result()
                        if file_stats:
                            if file_stats["success"]:
                                stats["files_processed"] = cast(int, stats["files_processed"]) + 1
                                stats["total_tokens"] = (
                                    cast(int, stats["total_tokens"]) + file_stats["tokens"]
                                )
                                stats["total_size"] = (
                                    cast(int, stats["total_size"]) + file_stats["size"]
                                )
                                languages = cast(Dict[str, int], stats["languages"])
                                languages[file_stats["language"]] += 1
                                successful_files.append(rel_path)
                            else:
                                failed_files.append(rel_path)
                    except Exception as e:
                        logger.error(f"Error processing {rel_path}: {str(e)}")
                        failed_files.append(rel_path)

                    # Update progress
                    self.progress.update_progress(
                        len(successful_files) + len(failed_files), total_files
                    )

            if not results:
                return None

            # Aggregate results
            total_tokens = sum(r["tokens"] for r in results)
            total_size = sum(r["size"] for r in results)
            language = max(results, key=lambda x: x["tokens"])["language"]

            # Combine content if needed
            combined_content = "".join(r["content"] for r in results)
            if self.config.sanitize_content:
                combined_content = self.sanitizer.clean_content(combined_content, language)

            return {
                "success": True,
                "path": file_path,
                "language": language,
                "size": total_size,
                "tokens": total_tokens,
                "content": combined_content,
            }

        except Exception as e:
            logger.error(f"Error processing file {file_path}: {str(e)}")
            self.stats["errors"] += 1
            return {
                "success": False,
                "path": file_path,
                "language": "unknown",
                "size": 0,
                "tokens": 0,
                "error": str(e),
            }

    def write_output(self, output_path: str, data: Dict[str, Any]) -> None:
        """Write output to a file with error handling.

        Args:
            output_path: Path to write output to
            data: Data to write

        Raises:
            TokenizationError: If writing fails
        """
        try:
            # Create output directory if needed
            output_dir = os.path.dirname(output_path)
            if output_dir:
                self.fs_service.create_directory(output_dir)

            # Extract data
            stats = data.get("stats", {})
            successful_files = data.get("successful_files", [])
            failed_files = data.get("failed_files", [])
            model_name = data.get("model", self.config.model_name)
            metadata = data.get("metadata", {})

            # Write output based on format
            if output_path.endswith(".json"):
                # JSON output
                output_data = {
                    "stats": stats,
                    "files": successful_files,
                    "failed_files": failed_files,
                    "metadata": {
                        "model": model_name,
                        **metadata
                    }
                }
                self.fs_service.write_file(output_path, json.dumps(output_data, indent=2))
            else:
                # Markdown output
                markdown = [
                    "# Code Documentation\n",
                    f"## Model: {model_name}\n",
                    "## Statistics\n",
                    f"- Files processed: {stats.get('files_processed', 0)}\n",
                    f"- Total tokens: {stats.get('total_tokens', 0):,}\n",
                    f"- Total size: {stats.get('total_size', 0):,} bytes\n",
                ]

                # Add language statistics
                if languages := stats.get("languages"):
                    markdown.append("\n## Languages\n")
                    for lang, count in languages.items():
                        markdown.append(f"- {lang}: {count} files\n")

                # Add metadata if included
                if metadata and self.config.include_metadata:
                    markdown.append("\n## Metadata\n")
                    for key, value in metadata.items():
                        markdown.append(f"- {key}: {value}\n")

                # Add file lists if metadata is included
                if self.config.include_metadata:
                    if successful_files:
                        markdown.append("\n## Processed Files\n")
                        for file_path in successful_files:
                            markdown.append(f"- {file_path}\n")

                    if failed_files:
                        markdown.append("\n## Failed Files\n")
                        for file_path in failed_files:
                            markdown.append(f"- {file_path}\n")

                self.fs_service.write_file(output_path, "".join(markdown))

        except Exception as e:
            logger.error(f"Failed to write output: {str(e)}")
            raise TokenizationError(f"Failed to write output: {str(e)}")

    def __del__(self):
        """Clean up resources on deletion."""
        if self.executor:
            self.executor.shutdown(wait=False)

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
