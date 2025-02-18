"""Integration tests for code tokenizer."""

import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from code_tokenizer.__main__ import parse_args, read_ignore_patterns
from code_tokenizer.cli import main
from code_tokenizer.models.model_config import DEFAULT_MODEL


class TestCLI:
    """Test command-line interface functionality."""

    def test_basic_cli(self, temp_dir, sample_codebase):
        """Test basic CLI functionality."""
        output_dir = Path(temp_dir) / "output"
        output_dir.mkdir()

        with patch.object(
            sys,
            "argv",
            [
                "code-tokenizer",
                "-d",
                str(sample_codebase),
                "-o",
                str(output_dir),
                "--model",
                "claude-3-sonnet",
            ],
        ):
            main()

        base_name = Path(sample_codebase).name
        assert (output_dir / f"{base_name}_docs.markdown").exists()
        assert (output_dir / f"{base_name}_analysis.md").exists()

    def test_cli_with_options(self, temp_dir, sample_codebase):
        """Test CLI with various options."""
        output_dir = Path(temp_dir) / "output"
        output_dir.mkdir()

        # Test with JSON format
        with patch.object(
            sys,
            "argv",
            [
                "code-tokenizer",
                "-d",
                str(sample_codebase),
                "-o",
                str(output_dir),
                "--format",
                "json",
                "--model",
                "claude-3-sonnet",
            ],
        ):
            main()

        base_name = Path(sample_codebase).name
        json_file = output_dir / f"{base_name}_docs.json"
        assert json_file.exists()

        # Verify JSON content
        with open(json_file) as f:
            data = json.load(f)
            assert "project_name" in data
            assert "files" in data
            assert len(data["files"]) > 0

    def test_cli_errors(self, temp_dir):
        """Test CLI error handling."""
        output_dir = Path(temp_dir) / "output"
        output_dir.mkdir()

        # Test invalid model
        with pytest.raises(SystemExit) as exc_info:
            with patch.object(
                sys,
                "argv",
                [
                    "code-tokenizer",
                    "-d",
                    str(temp_dir),
                    "-o",
                    str(output_dir),
                    "--model",
                    "invalid-model",
                ],
            ):
                main()
        assert exc_info.value.code == 2  # argparse exit code for argument errors


class TestMain:
    """Test main module functionality."""

    def test_parse_args(self, temp_dir):
        """Test argument parsing."""
        # Test with minimal arguments
        with patch.object(sys, "argv", ["code-tokenizer", temp_dir]):
            args = parse_args()
            assert args.directory == temp_dir
            assert args.model == DEFAULT_MODEL
            assert args.max_tokens is None
            assert args.ignore_file is None

    def test_read_ignore_patterns(self, temp_dir):
        """Test reading ignore patterns from file."""
        # Create test gitignore file
        gitignore = Path(temp_dir) / ".gitignore"
        gitignore.write_text(
            """
# Comment
*.pyc
node_modules/

# Empty lines

dist/
"""
        )

        patterns = read_ignore_patterns(str(gitignore))
        assert len(patterns) == 3
        assert "*.pyc" in patterns
        assert "node_modules/" in patterns
        assert "dist/" in patterns

        # Test with non-existent file
        assert read_ignore_patterns("non_existent_file") == []

    def test_main_function(self, temp_dir, sample_codebase):
        """Test main function execution."""
        # Test successful execution
        with patch.object(sys, "argv", ["code-tokenizer", sample_codebase]):
            assert main() == 0

        # Test with invalid directory
        with patch.object(sys, "argv", ["code-tokenizer", "non_existent_dir"]):
            assert main() == 1

        # Test with keyboard interrupt
        with patch.object(sys, "argv", ["code-tokenizer", sample_codebase]):
            with patch(
                "code_tokenizer.services.tokenizer_service.TokenizerService.process_directory",
                side_effect=KeyboardInterrupt,
            ):
                assert main() == 130

        # Test with general exception
        with patch.object(sys, "argv", ["code-tokenizer", sample_codebase]):
            with patch(
                "code_tokenizer.services.tokenizer_service.TokenizerService.process_directory",
                side_effect=Exception("Test error"),
            ):
                assert main() == 1


class TestEndToEnd:
    """End-to-end integration tests."""

    def test_full_processing(self, temp_dir, sample_codebase):
        """Test full processing of a sample codebase."""
        output_dir = Path(temp_dir) / "output"
        output_dir.mkdir()

        # Run with various options
        configs = [
            {
                "args": ["-d", str(sample_codebase), "-o", str(output_dir)],
                "format": "markdown",
                "model": DEFAULT_MODEL,
            },
            {
                "args": ["-d", str(sample_codebase), "-o", str(output_dir), "--format", "json"],
                "format": "json",
                "model": DEFAULT_MODEL,
            },
            {
                "args": ["-d", str(sample_codebase), "-o", str(output_dir), "--model", "gpt-4"],
                "format": "markdown",
                "model": "gpt-4",
            },
        ]

        for config in configs:
            with patch.object(sys, "argv", ["code-tokenizer"] + config["args"]):
                assert main() == 0

                base_name = Path(sample_codebase).name
                if config["format"] == "json":
                    output_file = output_dir / f"{base_name}_docs.json"
                    with open(output_file) as f:
                        data = json.load(f)
                        assert data["model"] == config["model"]
                        assert len(data["files"]) > 0
                else:
                    output_file = output_dir / f"{base_name}_docs.markdown"
                    assert output_file.exists()
                    content = output_file.read_text()
                    assert config["model"] in content

    def test_large_codebase(self, temp_dir):
        """Test processing a larger codebase structure."""
        # Create a more complex codebase
        src = Path(temp_dir) / "src"
        src.mkdir()

        # Create multiple file types
        files = {
            "main.py": "def main():\n    print('Hello')",
            "config.json": '{"version": "1.0.0"}',
            "README.md": "# Test Project",
            "style.css": "body { color: black; }",
            "script.js": "console.log('test');",
            "data.yaml": "key: value",
        }

        for name, content in files.items():
            (src / name).write_text(content)

        # Create nested directories
        (src / "tests").mkdir()
        (src / "tests" / "test_main.py").write_text("def test_main(): pass")

        output_dir = Path(temp_dir) / "output"
        output_dir.mkdir()

        with patch.object(
            sys,
            "argv",
            ["code-tokenizer", "-d", str(src), "-o", str(output_dir), "--format", "json"],
        ):
            assert main() == 0

            # Verify output
            docs_file = output_dir / "src_docs.json"
            with open(docs_file) as f:
                data = json.load(f)
                assert len(data["files"]) >= len(files)
                assert len(data["stats"]["languages"]) >= 5
                assert data["stats"]["files_processed"] >= len(files)
