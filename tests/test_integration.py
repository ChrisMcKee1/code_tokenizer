"""Integration tests for code tokenizer."""

import json
import os
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from code_tokenizer.__main__ import parse_args, read_ignore_patterns, write_output
from code_tokenizer.cli import main
from code_tokenizer.models.model_config import DEFAULT_MODEL
from code_tokenizer.services.filesystem_service import MockFileSystemService

from .conftest import BaseFileSystemTest


class TestCLI(BaseFileSystemTest):
    """Test command-line interface functionality."""

    def test_basic_cli(self, mock_fs, temp_dir):
        """Test basic CLI functionality."""
        # Set up sample codebase
        base_dir = temp_dir / "sample_codebase"
        self.setup_sample_codebase(mock_fs, base_dir)

        output_dir = temp_dir / "output"
        base_name = base_dir.name

        # Run CLI with basic options
        args = [
            "-d",
            str(base_dir),
            "-o",
            str(output_dir / f"{base_name}_docs.markdown"),
            "--model",
            "gpt-4o",  # Valid model name
        ]

        with patch("code_tokenizer.cli.RealFileSystemService", return_value=mock_fs):
            result = main(args)
            assert result == 0

        # Check output file exists
        assert mock_fs.exists(str(output_dir / f"{base_name}_docs.markdown"))

    def test_cli_with_options(self, mock_fs, temp_dir):
        """Test CLI with various options."""
        # Set up sample codebase
        base_dir = temp_dir / "sample_codebase"
        self.setup_sample_codebase(mock_fs, base_dir)

        output_dir = temp_dir / "output"
        base_name = base_dir.name
        json_file = output_dir / f"{base_name}_docs.json"

        # Run CLI with additional options
        args = [
            "-d",
            str(base_dir),
            "-o",
            str(json_file),
            "--model",
            "gpt-4o",  # Valid model name
            "--format",
            "json",
            "--max-tokens",
            "1000",
        ]

        with patch("code_tokenizer.cli.RealFileSystemService", return_value=mock_fs):
            result = main(args)
            assert result == 0

        # Check JSON output file exists
        assert mock_fs.exists(str(json_file))

    def test_cli_errors(self, mock_fs, temp_dir):
        """Test CLI error handling."""
        base_dir = temp_dir / "sample_codebase"
        output_dir = temp_dir / "output"

        # Test with invalid model
        args = ["-d", str(base_dir), "-o", str(output_dir), "--model", "invalid-model"]

        with pytest.raises(SystemExit) as exc_info:
            main(args)
        assert exc_info.value.code == 2


class TestMain(BaseFileSystemTest):
    """Test main module functionality."""

    def test_parse_args(self, temp_dir: str):
        """Test argument parsing."""
        # Test with minimal arguments
        with patch("code_tokenizer.__main__.is_running_tests", return_value=False):
            with patch.object(
                sys, "argv", ["code-tokenizer", "-d", str(temp_dir), "-o", "output.txt"]
            ):
                args = parse_args()
                assert os.path.abspath(args.directory) == os.path.abspath(temp_dir)
                assert args.output == "output.txt"
                assert args.model == DEFAULT_MODEL
                assert args.max_tokens is None
                assert args.format == "markdown"
                assert not args.bypass_gitignore
                assert not args.no_metadata

            # Test with all arguments
            with patch.object(
                sys,
                "argv",
                [
                    "code-tokenizer",
                    "-d",
                    str(temp_dir),
                    "-o",
                    "output.json",
                    "--model",
                    "gpt-4o",
                    "--max-tokens",
                    "1000",
                    "--format",
                    "json",
                    "--bypass-gitignore",
                    "--no-metadata",
                ],
            ):
                args = parse_args()
                assert os.path.abspath(args.directory) == os.path.abspath(temp_dir)
                assert args.output == "output.json"
                assert args.model == "gpt-4o"
                assert args.max_tokens == 1000
                assert args.format == "json"
                assert args.bypass_gitignore
                assert args.no_metadata

    def test_read_ignore_patterns(self, mock_fs: MockFileSystemService, temp_dir: str):
        """Test reading ignore patterns from file."""
        # Create test gitignore file
        gitignore = Path(temp_dir) / ".gitignore"
        mock_fs.write_file(
            str(gitignore),
            """
# Comment
*.pyc
node_modules/

# Empty lines

dist/
""",
        )

        patterns = read_ignore_patterns(str(gitignore), mock_fs)
        assert len(patterns) == 3
        assert "*.pyc" in patterns
        assert "node_modules/" in patterns
        assert "dist/" in patterns

        # Test with non-existent file
        assert read_ignore_patterns("non_existent_file", mock_fs) == []

        # Test with empty file
        empty_gitignore = Path(temp_dir) / "empty.gitignore"
        mock_fs.write_file(str(empty_gitignore), "")
        assert read_ignore_patterns(str(empty_gitignore), mock_fs) == []

        # Test with only comments and empty lines
        comment_gitignore = Path(temp_dir) / "comment.gitignore"
        mock_fs.write_file(
            str(comment_gitignore),
            """
# Just a comment
        
# Another comment
""",
        )
        assert read_ignore_patterns(str(comment_gitignore), mock_fs) == []

    def test_main_function(self, mock_fs, temp_dir):
        """Test the main function with basic options."""
        # Set up sample codebase
        base_dir = temp_dir / "sample_codebase"
        self.setup_sample_codebase(mock_fs, base_dir)

        output_dir = temp_dir / "output"
        mock_fs.create_directory(str(output_dir))

        args = ["-d", str(base_dir), "-o", str(output_dir), "--model", "gpt-4"]  # Valid model name

        result = main(args)
        assert result == 0


class TestEndToEnd(BaseFileSystemTest):
    """End-to-end integration tests."""

    def test_full_processing(self, mock_fs, temp_dir):
        """Test full end-to-end processing of a sample codebase."""
        # Set up sample codebase
        base_dir = temp_dir / "sample_codebase"
        self.setup_sample_codebase(mock_fs, base_dir)

        output_dir = temp_dir / "output"
        mock_fs.create_directory(str(output_dir))

        # Create output file path
        output_file = output_dir / "sample_codebase_docs.json"

        args = [
            "-d",
            str(base_dir),
            "-o",
            str(output_file),
            "--model",
            "gpt-4",  # Valid model name
            "--format",
            "json",
            "--bypass-gitignore",  # Bypass gitignore to ensure all files are processed
        ]

        with patch("code_tokenizer.cli.RealFileSystemService", return_value=mock_fs):
            result = main(args)
            assert result == 0

        # Check output files exist
        assert mock_fs.exists(str(output_file))

        # Read and verify output
        content = mock_fs.read_file(str(output_file))
        data = json.loads(content)
        assert "files" in data
        assert "metadata" in data
        assert len(data["files"]) > 0

    def test_large_codebase(self, mock_fs, temp_dir):
        """Test processing a larger codebase."""
        # Set up a larger sample codebase
        src_dir = temp_dir / "src"
        self.setup_sample_codebase(mock_fs, src_dir)

        # Add more files to simulate a larger codebase
        additional_files = {
            "utils.py": "def helper():\n    pass",
            "config/settings.py": "DEBUG = True",
            "tests/test_main.py": "def test_something():\n    assert True",
        }

        for path, content in additional_files.items():
            file_path = src_dir / path
            mock_fs.create_directory(str(os.path.dirname(file_path)))
            mock_fs.write_file(str(file_path), content)

        output_dir = temp_dir / "output"
        mock_fs.create_directory(str(output_dir))

        # Create output file path
        output_file = output_dir / "src_docs.json"

        args = [
            "-d",
            str(src_dir),
            "-o",
            str(output_file),
            "--model",
            "gpt-4",  # Valid model name
            "--format",
            "json",
            "--bypass-gitignore",  # Bypass gitignore to ensure all files are processed
        ]

        with patch("code_tokenizer.cli.RealFileSystemService", return_value=mock_fs):
            result = main(args)
            assert result == 0

        # Check output files exist
        assert mock_fs.exists(str(output_file))

        # Read and verify output
        content = mock_fs.read_file(str(output_file))
        data = json.loads(content)
        assert len(data["files"]) > 5  # Should have more than 5 files


class TestMainModule(BaseFileSystemTest):
    """Test __main__ module functionality."""

    def test_main_entry_point(
        self, mock_fs: MockFileSystemService, temp_dir: str, sample_codebase: str
    ):
        """Test main entry point."""
        output_dir = Path(temp_dir) / "output"
        mock_fs.create_directory(str(temp_dir), 0o777)  # Full permissions for parent
        mock_fs.create_directory(str(output_dir), 0o777)  # Full permissions for output

        # Create sample codebase in mock filesystem
        self.setup_sample_codebase(mock_fs, sample_codebase)

        # Test successful execution
        with patch.object(
            sys,
            "argv",
            [
                "code-tokenizer",
                "-d",
                str(sample_codebase),
                "-o",
                str(output_dir / "output.txt"),
                "--model",
                "gpt-4o",
            ],
        ), patch("code_tokenizer.cli.RealFileSystemService", return_value=mock_fs):
            assert main() == 0

        # Test with invalid model (should exit with code 2)
        with pytest.raises(SystemExit) as exc_info:
            with patch.object(
                sys,
                "argv",
                [
                    "code-tokenizer",
                    "-d",
                    str(sample_codebase),
                    "-o",
                    str(output_dir / "output.txt"),
                    "--model",
                    "invalid-model",
                ],
            ):
                main()
        assert exc_info.value.code == 2

    def test_read_ignore_patterns_detailed(self, mock_fs: MockFileSystemService, temp_dir: str):
        """Test reading ignore patterns in detail."""
        # Test with non-existent file
        assert read_ignore_patterns("non_existent_file", mock_fs) == []

        # Test with empty file
        empty_file = Path(temp_dir) / "empty"
        mock_fs.write_file(str(empty_file), "")
        assert read_ignore_patterns(str(empty_file), mock_fs) == []

        # Test with only comments and empty lines
        comments_file = Path(temp_dir) / "comments"
        mock_fs.write_file(
            str(comments_file),
            """
# Comment 1
   # Indented comment
   
# Comment 2
        """,
        )
        assert read_ignore_patterns(str(comments_file), mock_fs) == []

        # Test with mixed content
        mixed_file = Path(temp_dir) / "mixed"
        mock_fs.write_file(
            str(mixed_file),
            """
# Python files
*.py[cod]
__pycache__/

# Empty line

# Build directories
build/
dist/
        """,
        )
        patterns = read_ignore_patterns(str(mixed_file), mock_fs)
        assert len(patterns) == 4
        assert "*.py[cod]" in patterns
        assert "__pycache__/" in patterns
        assert "build/" in patterns
        assert "dist/" in patterns

        # Test with invalid file permissions
        no_access_file = Path(temp_dir) / "no_access"
        mock_fs.write_file(str(no_access_file), "test")
        mock_fs.set_permission(str(no_access_file), 0o000)  # No permissions
        with pytest.raises(Exception):
            read_ignore_patterns(str(no_access_file), mock_fs)

    def setup_sample_codebase(self, mock_fs: MockFileSystemService, codebase_dir: str) -> None:
        """Set up a sample codebase in the mock filesystem."""
        files = {
            "main.py": "def main():\n    print('Hello, World!')\n\nif __name__ == '__main__':\n    main()",
            "config.json": '{\n    "name": "test",\n    "version": "1.0.0"\n}',
            "styles.css": "body {\n    color: blue;\n}\n",
            "index.html": "<html>\n<body>\n    <h1>Test</h1>\n</body>\n</html>",
            "script.js": "function test() {\n    console.log('test');\n}",
            ".gitignore": "*.pyc\n__pycache__/\ndist/",
        }

        mock_fs.create_directory(str(codebase_dir))
        for filename, content in files.items():
            file_path = os.path.join(codebase_dir, filename)
            mock_fs.write_file(str(file_path), content)
