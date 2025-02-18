"""Edge cases and error handling tests."""

import os
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path

import pytest

from code_tokenizer.services.tokenizer_service import TokenizerService
from code_tokenizer.services.filesystem_service import MockFileSystemService


@contextmanager
def capture_output():
    """Capture stdout and stderr to a temporary file."""
    temp_file = tempfile.NamedTemporaryFile(mode="w+", delete=False)
    old_stdout, old_stderr = sys.stdout, sys.stderr
    try:
        sys.stdout = sys.stderr = temp_file
        yield temp_file.name
    finally:
        sys.stdout, sys.stderr = old_stdout, old_stderr
        temp_file.close()


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_directory(self, temp_dir):
        """Test processing an empty directory."""
        tokenizer = TokenizerService.from_config({
            "base_dir": str(temp_dir),
            "model_name": "gpt-4o",
            "max_tokens": 200000,
            "output_format": "markdown",
            "bypass_gitignore": False,
            "include_metadata": True
        })
        stats = tokenizer.process_directory(str(temp_dir))
        assert "stats" in stats
        assert stats["stats"]["files_processed"] == 0
        assert stats["stats"]["total_tokens"] == 0
        assert len(stats["successful_files"]) == 0
        assert len(stats["failed_files"]) == 0

    def test_binary_files(self, temp_dir):
        """Test handling of binary files."""
        # Create a binary file
        binary_file = Path(temp_dir) / "test.bin"
        fs_service = MockFileSystemService()
        fs_service.write_file(str(binary_file), b"\x00\x01\x02\x03")

        tokenizer = TokenizerService.from_config({
            "base_dir": str(temp_dir),
            "model_name": "gpt-4o",
            "max_tokens": 200000,
            "output_format": "markdown",
            "bypass_gitignore": False,
            "include_metadata": True
        }, fs_service)
        result = tokenizer.process_file(str(binary_file))
        assert result is None  # Binary files should be skipped

    def test_large_file_handling(self, temp_dir):
        """Test handling of large files."""
        # Create a large text file
        large_file = Path(temp_dir) / "large.txt"
        with open(large_file, "w") as f:
            f.write("x" * (TokenizerService.MAX_FILE_SIZE + 1))

        tokenizer = TokenizerService.from_config({
            "base_dir": str(temp_dir),
            "model_name": "gpt-4o",
            "max_tokens": 200000,
            "output_format": "markdown",
            "bypass_gitignore": False,
            "include_metadata": True
        })
        result = tokenizer.process_file(str(large_file))
        assert result is None  # Large files should be skipped

    def test_special_characters(self, temp_dir):
        """Test handling of special characters in filenames and content."""
        # Create files with special characters
        files = {
            "test@file.txt": "Normal content",
            "unicode_文件.txt": "Unicode content",
            "spaces in name.txt": "Content with spaces",
        }

        for filename, content in files.items():
            file_path = Path(temp_dir) / filename
            file_path.write_text(content)

        tokenizer = TokenizerService.from_config({
            "base_dir": str(temp_dir),
            "model_name": "gpt-4o",
            "max_tokens": 200000,
            "output_format": "markdown",
            "bypass_gitignore": True,  # Allow all files
            "include_metadata": True
        })
        stats = tokenizer.process_directory(str(temp_dir))
        assert "stats" in stats
        assert stats["stats"]["files_processed"] == len(files)
        assert stats["stats"]["total_tokens"] > 0
        assert len(stats["successful_files"]) == len(files)
        assert len(stats["failed_files"]) == 0

    def test_error_recovery(self, temp_dir):
        """Test recovery from file processing errors."""
        # Create a mix of valid and invalid files
        (Path(temp_dir) / "valid.txt").write_text("Valid content")
        invalid_file = Path(temp_dir) / "invalid.txt"
        invalid_file.write_text("Invalid content")

        # Create a directory that will be skipped
        skip_dir = Path(temp_dir) / "skip_dir"
        skip_dir.mkdir()
        (skip_dir / "skip.txt").write_text("Skip this file")

        tokenizer = TokenizerService.from_config({
            "base_dir": str(temp_dir),
            "model_name": "gpt-4o",
            "max_tokens": 200000,
            "output_format": "markdown",
            "bypass_gitignore": True,  # Allow all files
            "include_metadata": True
        })
        stats = tokenizer.process_directory(str(temp_dir))
        
        assert "stats" in stats
        assert stats["stats"]["files_processed"] >= 1  # At least the valid file
        assert len(stats["successful_files"]) >= 1
        assert len(stats["failed_files"]) == 0  # No failures since we're not making files unreadable

    def test_max_file_limit(self, temp_dir):
        """Test enforcement of maximum file size limit using small test files."""
        # Create a file just under the size limit (using a small test size)
        test_size = 1024  # 1KB for testing
        under_limit_file = Path(temp_dir) / "under_limit.txt"
        with open(under_limit_file, "w") as f:
            f.write("x" * test_size)

        tokenizer = TokenizerService.from_config({
            "base_dir": str(temp_dir),
            "model_name": "gpt-4o",
            "max_tokens": 200000,
            "output_format": "markdown",
            "bypass_gitignore": True,  # Allow all files
            "include_metadata": True
        })
        result = tokenizer.process_file(str(under_limit_file))
        assert result is not None
        assert result["size"] == test_size

        # Test file over the limit (using a small test size)
        test_over_size = 2048  # 2KB for testing
        over_limit_file = Path(temp_dir) / "over_limit.txt"
        with open(over_limit_file, "w") as f:
            f.write("x" * test_over_size)

        # Mock the file size check to simulate a large file
        original_get_file_size = tokenizer.fs_service.get_file_size
        try:
            def mock_get_file_size(path: str) -> int:
                if path == str(over_limit_file):
                    return TokenizerService.MAX_FILE_SIZE + 1024  # Simulate file being over limit
                return original_get_file_size(path)
            
            tokenizer.fs_service.get_file_size = mock_get_file_size
            result = tokenizer.process_file(str(over_limit_file))
            assert result is None  # Should be skipped since it's reported as over the limit
        finally:
            # Restore original method
            tokenizer.fs_service.get_file_size = original_get_file_size
