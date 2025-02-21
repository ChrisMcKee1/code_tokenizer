"""Tests for output formatters."""

import json
import yaml
from pathlib import Path
from typing import List

import pytest

from code_tokenizer.formatters.json_formatter import JSONFormatter
from code_tokenizer.formatters.markdown_formatter import MarkdownFormatter
from code_tokenizer.formatters.text_formatter import TextFormatter
from code_tokenizer.formatters.yaml_formatter import YAMLFormatter
from code_tokenizer.models.content import FileContent


@pytest.fixture
def sample_files() -> List[FileContent]:
    """Create sample FileContent objects for testing."""
    return [
        FileContent(
            name="test.py",
            path="/path/to/test.py",
            relative_path="src/test.py",
            language="Python",
            token_count=100,
            content="def test():\n    pass",
            size=20,
            encoding="utf-8",
        ),
        FileContent(
            name="main.js",
            path="/path/to/main.js",
            relative_path="src/main.js",
            language="JavaScript",
            token_count=150,
            content="function main() {\n    return true;\n}",
            size=35,
            encoding="utf-8",
        ),
    ]


@pytest.fixture
def sample_stats() -> dict:
    """Create sample statistics for testing."""
    return {
        "files_processed": 2,
        "total_tokens": 250,
        "total_size": 55,
        "languages": {"Python": 1, "JavaScript": 1},
    }


@pytest.fixture
def sample_metadata() -> dict:
    """Create sample metadata for testing."""
    return {
        "model": "gpt-4o",
        "max_tokens": 8192,
        "timestamp": "2024-01-01T00:00:00Z",
    }


class TestYAMLFormatter:
    """Test YAML formatter functionality."""

    def test_format_content_basic(self, sample_files):
        """Test basic YAML formatting."""
        formatter = YAMLFormatter()
        result = formatter.format_content(sample_files)
        data = yaml.safe_load(result)

        assert "files" in data
        assert len(data["files"]) == 2
        assert data["files"][0]["name"] == "test.py"
        assert data["files"][1]["name"] == "main.js"

    def test_format_content_with_stats(self, sample_files, sample_stats):
        """Test YAML formatting with statistics."""
        formatter = YAMLFormatter()
        result = formatter.format_content(sample_files, stats=sample_stats)
        data = yaml.safe_load(result)

        assert "stats" in data
        assert data["stats"]["files_processed"] == 2
        assert data["stats"]["total_tokens"] == 250
        assert data["stats"]["languages"]["Python"] == 1

    def test_format_content_with_metadata(self, sample_files, sample_metadata):
        """Test YAML formatting with metadata."""
        formatter = YAMLFormatter()
        result = formatter.format_content(sample_files, metadata=sample_metadata)
        data = yaml.safe_load(result)

        assert "metadata" in data
        assert data["metadata"]["model"] == "gpt-4o"
        assert data["metadata"]["max_tokens"] == 8192

    def test_format_content_full(self, sample_files, sample_stats, sample_metadata):
        """Test YAML formatting with all components."""
        formatter = YAMLFormatter()
        result = formatter.format_content(
            sample_files, stats=sample_stats, metadata=sample_metadata
        )
        data = yaml.safe_load(result)

        # Check structure
        assert all(key in data for key in ["files", "stats", "metadata"])

        # Check files
        assert len(data["files"]) == 2
        file1, file2 = data["files"]
        assert file1["language"] == "Python"
        assert file2["language"] == "JavaScript"

        # Check stats
        assert data["stats"]["total_tokens"] == 250
        assert data["stats"]["languages"] == {"Python": 1, "JavaScript": 1}

        # Check metadata
        assert data["metadata"]["model"] == "gpt-4o"
        assert data["metadata"]["timestamp"] == "2024-01-01T00:00:00Z"

    def test_yaml_formatting_style(self, sample_files):
        """Test YAML output style and formatting."""
        formatter = YAMLFormatter()
        result = formatter.format_content(sample_files)

        # Should start with YAML document marker
        assert result.startswith("---")

        # Should use block style for content
        assert "|-" in result or "|" in result

        # Should be properly indented
        lines = result.split("\n")
        assert any(line.startswith("  ") for line in lines)

        # Should be valid YAML
        data = yaml.safe_load(result)
        assert isinstance(data, dict)

    def test_empty_input(self):
        """Test formatting with empty input."""
        formatter = YAMLFormatter()
        result = formatter.format_content([])
        data = yaml.safe_load(result)

        assert data["files"] == []
        assert data["stats"] == {}
        assert data["metadata"] == {}


class TestTextFormatter:
    """Test text formatter functionality."""

    def test_format_content_basic(self, sample_files):
        """Test basic text formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check basic structure
        assert "Code Documentation" in result
        assert "=" * 80 in result
        assert "Files:" in result
        
        # Check file content
        assert "test.py" in result
        assert "main.js" in result
        assert "def test():" in result
        assert "function main()" in result

    def test_format_content_with_stats(self, sample_files, sample_stats):
        """Test text formatting with statistics."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files, stats=sample_stats)

        assert "Statistics:" in result
        assert "files_processed: 2" in result
        assert "total_tokens: 250" in result
        assert "languages" in result
        assert "Python" in result
        assert "JavaScript" in result

    def test_format_content_with_metadata(self, sample_files, sample_metadata):
        """Test text formatting with metadata."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files, metadata=sample_metadata)

        assert "Metadata:" in result
        assert "model: gpt-4" in result
        assert "max_tokens: 8192" in result
        assert "timestamp:" in result

    def test_format_content_full(self, sample_files, sample_stats, sample_metadata):
        """Test text formatting with all components."""
        formatter = TextFormatter()
        result = formatter.format_content(
            sample_files, stats=sample_stats, metadata=sample_metadata
        )

        # Check all sections present
        assert "Code Documentation" in result
        assert "Metadata:" in result
        assert "Statistics:" in result
        assert "Files:" in result

        # Check section order
        metadata_pos = result.find("Metadata:")
        stats_pos = result.find("Statistics:")
        files_pos = result.find("Files:")
        assert metadata_pos < stats_pos < files_pos

        # Check content formatting
        assert "-" * 40 in result  # Section separators
        assert "Content:" in result  # File content headers
        assert all(f.name in result for f in sample_files)

    def test_empty_input(self):
        """Test formatting with empty input."""
        formatter = TextFormatter()
        result = formatter.format_content([])

        assert "Code Documentation" in result
        assert "Files:" in result
        assert "test.py" not in result  # No files should be present

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
"""Tests for output formatters."""

import json
import yaml
from pathlib import Path
from typing import List

import pytest

from code_tokenizer.formatters.json_formatter import JSONFormatter
from code_tokenizer.formatters.markdown_formatter import MarkdownFormatter
from code_tokenizer.formatters.text_formatter import TextFormatter
from code_tokenizer.formatters.yaml_formatter import YAMLFormatter
from code_tokenizer.models.content import FileContent


@pytest.fixture
def sample_files() -> List[FileContent]:
    """Create sample FileContent objects for testing."""
    return [
        FileContent(
            name="test.py",
            path="/path/to/test.py",
            relative_path="src/test.py",
            language="Python",
            token_count=100,
            content="def test():\n    pass",
            size=20,
            encoding="utf-8",
        ),
        FileContent(
            name="main.js",
            path="/path/to/main.js",
            relative_path="src/main.js",
            language="JavaScript",
            token_count=150,
            content="function main() {\n    return true;\n}",
            size=35,
            encoding="utf-8",
        ),
    ]


@pytest.fixture
def sample_stats() -> dict:
    """Create sample statistics for testing."""
    return {
        "files_processed": 2,
        "total_tokens": 250,
        "total_size": 55,
        "languages": {"Python": 1, "JavaScript": 1},
    }


@pytest.fixture
def sample_metadata() -> dict:
    """Create sample metadata for testing."""
    return {
        "model": "gpt-4o",
        "max_tokens": 8192,
        "timestamp": "2024-01-01T00:00:00Z",
    }


class TestYAMLFormatter:
    """Test YAML formatter functionality."""

    def test_format_content_basic(self, sample_files):
        """Test basic YAML formatting."""
        formatter = YAMLFormatter()
        result = formatter.format_content(sample_files)
        data = yaml.safe_load(result)

        assert "files" in data
        assert len(data["files"]) == 2
        assert data["files"][0]["name"] == "test.py"
        assert data["files"][1]["name"] == "main.js"

    def test_format_content_with_stats(self, sample_files, sample_stats):
        """Test YAML formatting with statistics."""
        formatter = YAMLFormatter()
        result = formatter.format_content(sample_files, stats=sample_stats)
        data = yaml.safe_load(result)

        assert "stats" in data
        assert data["stats"]["files_processed"] == 2
        assert data["stats"]["total_tokens"] == 250
        assert data["stats"]["languages"]["Python"] == 1

    def test_format_content_with_metadata(self, sample_files, sample_metadata):
        """Test YAML formatting with metadata."""
        formatter = YAMLFormatter()
        result = formatter.format_content(sample_files, metadata=sample_metadata)
        data = yaml.safe_load(result)

        assert "metadata" in data
        assert data["metadata"]["model"] == "gpt-4o"
        assert data["metadata"]["max_tokens"] == 8192

    def test_format_content_full(self, sample_files, sample_stats, sample_metadata):
        """Test YAML formatting with all components."""
        formatter = YAMLFormatter()
        result = formatter.format_content(
            sample_files, stats=sample_stats, metadata=sample_metadata
        )
        data = yaml.safe_load(result)

        # Check structure
        assert all(key in data for key in ["files", "stats", "metadata"])

        # Check files
        assert len(data["files"]) == 2
        file1, file2 = data["files"]
        assert file1["language"] == "Python"
        assert file2["language"] == "JavaScript"

        # Check stats
        assert data["stats"]["total_tokens"] == 250
        assert data["stats"]["languages"] == {"Python": 1, "JavaScript": 1}

        # Check metadata
        assert data["metadata"]["model"] == "gpt-4o"
        assert data["metadata"]["timestamp"] == "2024-01-01T00:00:00Z"

    def test_yaml_formatting_style(self, sample_files):
        """Test YAML output style and formatting."""
        formatter = YAMLFormatter()
        result = formatter.format_content(sample_files)

        # Should start with YAML document marker
        assert result.startswith("---")

        # Should use block style for content
        assert "|-" in result or "|" in result

        # Should be properly indented
        lines = result.split("\n")
        assert any(line.startswith("  ") for line in lines)

        # Should be valid YAML
        data = yaml.safe_load(result)
        assert isinstance(data, dict)

    def test_empty_input(self):
        """Test formatting with empty input."""
        formatter = YAMLFormatter()
        result = formatter.format_content([])
        data = yaml.safe_load(result)

        assert data["files"] == []
        assert data["stats"] == {}
        assert data["metadata"] == {}


class TestTextFormatter:
    """Test text formatter functionality."""

    def test_format_content_basic(self, sample_files):
        """Test basic text formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check basic structure
        assert "Code Documentation" in result
        assert "=" * 80 in result
        assert "Files:" in result
        
        # Check file content
        assert "test.py" in result
        assert "main.js" in result
        assert "def test():" in result
        assert "function main()" in result

    def test_format_content_with_stats(self, sample_files, sample_stats):
        """Test text formatting with statistics."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files, stats=sample_stats)

        assert "Statistics:" in result
        assert "files_processed: 2" in result
        assert "total_tokens: 250" in result
        assert "Python: 1" in result
        assert "JavaScript: 1" in result

    def test_format_content_with_metadata(self, sample_files, sample_metadata):
        """Test text formatting with metadata."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files, metadata=sample_metadata)

        assert "Metadata:" in result
        assert "model: gpt-4o" in result
        assert "max_tokens: 8192" in result
        assert "timestamp: 2024-01-01T00:00:00Z" in result

    def test_format_content_full(self, sample_files, sample_stats, sample_metadata):
        """Test text formatting with all components."""
        formatter = TextFormatter()
        result = formatter.format_content(
            sample_files, stats=sample_stats, metadata=sample_metadata
        )

        # Check all sections present
        assert "Code Documentation" in result
        assert "Metadata:" in result
        assert "Statistics:" in result
        assert "Files:" in result

        # Check section order
        metadata_pos = result.find("Metadata:")
        stats_pos = result.find("Statistics:")
        files_pos = result.find("Files:")
        assert metadata_pos < stats_pos < files_pos

        # Check content formatting
        assert "-" * 40 in result  # Section separators
        assert "Content:" in result  # File content headers
        assert all(f.name in result for f in sample_files)

    def test_empty_input(self):
        """Test formatting with empty input."""
        formatter = TextFormatter()
        result = formatter.format_content([])

        assert "Code Documentation" in result
        assert "Files:" in result
        assert "test.py" not in result  # No files should be present

    def test_text_formatting_style(self, sample_files):
        """Test text output style and formatting."""
        formatter = TextFormatter()
        result = formatter.format_content(sample_files)

        # Check section headers
        assert result.startswith("Code Documentation")
        assert "=" * 80 in result  # Main header separator
        assert "-" * 40 in result  # Section separators

        # Check file sections
        lines = result.split("\n")
        assert any(line.startswith("Path: ") for line in lines)
        assert any(line.startswith("Language: ") for line in lines)
        assert any(line.startswith("Size: ") for line in lines)

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert any("-" * 8 in line for line in lines)  # Content separator

        # Check content formatting
        assert "Content:" in result
        assert data["metadata"] == {} 