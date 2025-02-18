"""Unit tests for code tokenizer components."""

from pathlib import Path
from unittest.mock import patch

import pytest
from pygments.lexers import get_lexer_by_name

from code_tokenizer.core.tokenizer import count_tokens, truncate_text
from code_tokenizer.exceptions import ModelNotSupportedError
from code_tokenizer.models.model_config import (
    DEFAULT_MODEL,
    MODEL_ENCODINGS,
    Encoding,
    get_model_encoding,
    get_model_token_limit,
)
from code_tokenizer.services.language_detector import (
    LanguageDetector,
    detect_language,
    detect_language_by_patterns,
)
from code_tokenizer.services.tokenizer_service import TokenizerConfig, TokenizerService
from code_tokenizer.utils.path_utils import get_relative_path, normalize_path, should_ignore_path


class TestModelConfig:
    """Test model configuration functionality."""

    def test_model_encodings(self):
        """Test model encoding mappings."""
        # Test O-series models use o200k_base
        assert MODEL_ENCODINGS["gpt-4o"] == Encoding.O200K_BASE
        assert MODEL_ENCODINGS["o1-preview"] == Encoding.O200K_BASE

        # Test GPT-4 and GPT-3.5 models use cl100k_base
        assert MODEL_ENCODINGS["gpt-4"] == Encoding.CL100K_BASE
        assert MODEL_ENCODINGS["gpt-3.5-turbo"] == Encoding.CL100K_BASE

    def test_get_model_encoding(self):
        """Test getting model encodings."""
        # Test exact matches
        assert get_model_encoding("gpt-4o") == Encoding.O200K_BASE
        assert get_model_encoding("gpt-4") == Encoding.CL100K_BASE

        # Test prefix matches
        assert get_model_encoding("gpt-4o-test") == Encoding.O200K_BASE
        assert get_model_encoding("o1-custom") == Encoding.O200K_BASE

        # Test invalid model
        with pytest.raises(ValueError):
            get_model_encoding("invalid-model")

    def test_get_model_token_limit(self):
        """Test getting model token limits."""
        # Test O-series models
        assert get_model_token_limit("o1-preview") == 200000
        assert get_model_token_limit("gpt-4o") == 8192

        # Test standard models
        assert get_model_token_limit("gpt-4") == 8192
        assert get_model_token_limit("gpt-3.5-turbo") == 4096

        # Test invalid model
        with pytest.raises(ValueError):
            get_model_token_limit("invalid-model")


class TestPathUtils:
    """Test path utility functions."""

    @pytest.mark.unit
    def test_normalize_path(self):
        """Test path normalization."""
        # Test Windows paths
        assert normalize_path("path\\to\\file") == "path/to/file"
        assert normalize_path(".\\relative\\path") == "relative/path"
        assert normalize_path("C:\\absolute\\path") == "C:/absolute/path"
        assert normalize_path("..\\parent\\path") == "../parent/path"

        # Test Unix paths
        assert normalize_path("path/to/file") == "path/to/file"
        assert normalize_path("./relative/path") == "relative/path"
        assert normalize_path("/absolute/path") == "/absolute/path"
        assert normalize_path("../parent/path") == "../parent/path"

        # Test mixed separators
        assert normalize_path("path\\to/file") == "path/to/file"
        assert normalize_path("path/to\\file") == "path/to/file"

    @pytest.mark.unit
    def test_get_relative_path(self):
        """Test getting relative paths."""
        base_dir = "/base/dir"
        file_path = "/base/dir/sub/file.txt"

        # Test relative path calculation
        assert get_relative_path(file_path, base_dir) == "sub/file.txt"

        # Test path at same level as base
        assert get_relative_path("/base/dir/file.txt", base_dir) == "file.txt"

        # Test path outside base
        result = get_relative_path("/other/path/file.txt", base_dir)
        assert result.startswith("../") or result.startswith("..\\")

        # Test with Windows paths
        assert get_relative_path("C:\\base\\dir\\file.txt", "C:\\base\\dir") == "file.txt"
        assert get_relative_path("C:\\other\\path\\file.txt", "C:\\base\\dir").startswith("..")

    @pytest.mark.unit
    def test_should_ignore_path_patterns(self):
        """Test path ignore pattern matching."""
        # Test directory patterns
        assert should_ignore_path("src/test/file.txt", ["test/"])[0]
        assert should_ignore_path("src/test/nested/file.txt", ["test/"])[0]

        # Test recursive patterns
        assert should_ignore_path("deep/nested/file.txt", ["**/nested"])[0]
        assert should_ignore_path("nested/deep/nested/file.txt", ["**/nested"])[0]

        # Test wildcard patterns
        assert should_ignore_path("src/test.py", ["*.py"])[0]
        assert should_ignore_path("src/nested/test.py", ["**/*.py"])[0]

        # Test exact matches
        assert should_ignore_path("exact_file.txt", ["exact_file.txt"])[0]
        assert should_ignore_path("path/to/exact_file.txt", ["exact_file.txt"])[0]

        # Test non-matches
        assert not should_ignore_path("src/keep.txt", ["*.py"])[0]
        assert not should_ignore_path("src/test/keep.js", ["*.py", "*.css"])[0]

        # Test complex patterns
        assert should_ignore_path("node_modules/package/file.js", ["node_modules/**"])[0]
        assert should_ignore_path(".git/config", [".git/**"])[0]
        assert should_ignore_path("build/temp/cache.txt", ["build/", "dist/"])[0]

    @pytest.mark.unit
    def test_normalize_path_edge_cases(self):
        """Test path normalization edge cases."""
        # Test empty and special paths
        assert normalize_path("") == ""
        assert normalize_path(".") == "."
        assert normalize_path("..") == ".."
        assert normalize_path("./") == "."
        assert normalize_path("../") == ".."

        # Test multiple slashes
        assert normalize_path("path//to//file") == "path/to/file"
        assert normalize_path("path\\\\/to\\\\file") == "path/to/file"

        # Test dots in path
        assert normalize_path("./path/./to/./file") == "path/to/file"
        assert normalize_path("path/././to/file") == "path/to/file"

    @pytest.mark.unit
    def test_get_relative_path_edge_cases(self):
        """Test getting relative paths in edge cases."""
        # Test with same paths
        assert get_relative_path("/path/to/file", "/path/to/file") == "."
        assert get_relative_path("C:\\path\\to\\file", "C:\\path\\to\\file") == "."

        # Test with parent path
        assert get_relative_path("/path/to/file", "/path") == "to/file"
        assert get_relative_path("C:\\path\\to\\file", "C:\\path") == "to/file"

        # Test with different drives (Windows)
        result = get_relative_path("D:/path/file", "C:/path")
        assert result == "D:/path/file" or result == "D:\\path\\file"

        # Test with invalid paths
        assert normalize_path("invalid\\path\\*") == "invalid/path/*"
        assert normalize_path("path\\with\\spaces\\ ") == "path/with/spaces/ "


class TestCoreFeatures:
    """Test core features of the code tokenizer."""

    def test_token_counting(self):
        """Test token counting with various inputs and models."""
        # Basic counting
        assert count_tokens("Hello, World!", "gpt-4o") > 0
        assert count_tokens("", "gpt-4o") == 0

        # Test different models
        text = "This is a test sentence."
        tokens_claude = count_tokens(text, "gpt-4o")
        tokens_gpt = count_tokens(text, "gpt-3.5-turbo")
        assert tokens_claude > 0
        assert tokens_gpt > 0

        # Edge cases
        assert count_tokens(" ", "gpt-4o") > 0  # Just whitespace
        assert count_tokens("\n\n\n", "gpt-4o") > 0  # Just newlines
        assert count_tokens("a" * 1000, "gpt-4o") > 0  # Long repetitive text

    def test_language_detection(self):
        """Test language detection with various inputs."""
        # Basic detection
        assert detect_language("def test(): pass", "test.py") == "Python"
        assert detect_language('{"test": true}', "test.json") == "JSON"
        assert detect_language("# Test\n## Header", "test.md") == "Markdown"
        assert detect_language("random text", "test.txt") == "Text"

        # Edge cases
        assert detect_language("", "test.py") == "Text"
        assert detect_language(None, "test.py") == "Text"
        assert detect_language("print('hello')", None) == "Text"
        assert detect_language("", None) == "Text"

    def test_gitignore_handling(self):
        """Test .gitignore pattern matching."""
        patterns = ["*.pyc", "__pycache__/", "temp/"]

        # Should ignore
        assert should_ignore_path("file.pyc", patterns)[0]
        assert should_ignore_path("__pycache__/cache.txt", patterns)[0]
        assert should_ignore_path("temp/test.txt", patterns)[0]

        # Should not ignore
        assert not should_ignore_path("main.py", patterns)[0]
        assert not should_ignore_path("src/util.js", patterns)[0]

    def test_truncate_text(self):
        """Test text truncation functionality."""
        # Test no truncation needed
        text = "This is a short text."
        truncated, count = truncate_text(text, 10, "gpt-4o")
        assert truncated == text
        assert count < 10

        # Test truncation
        long_text = "This is a longer text that needs to be truncated." * 100
        truncated, count = truncate_text(long_text, 20, "gpt-4o")
        assert len(truncated) < len(long_text)
        assert count <= 20  # Changed from == to <= since truncation might result in fewer tokens

        # Test with different models
        text = "Test text for different models."
        t1, c1 = truncate_text(text, 10, "gpt-4o")
        t2, c2 = truncate_text(text, 10, "gpt-3.5-turbo")
        assert len(t1) > 0
        assert len(t2) > 0
        assert c1 <= 10  # Add assertion to verify token count is within limit
        assert c2 <= 10  # Add assertion to verify token count is within limit

        # Test invalid model
        with pytest.raises(ModelNotSupportedError):
            truncate_text(text, 10, "invalid-model")


class TestLanguageDetector:
    """Test language detection functionality."""

    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Set up test cases."""
        self.detector = LanguageDetector()

    def test_detect_javascript(self):
        """Test JavaScript detection."""
        js_samples = [
            "const foo = 'bar';",
            "function test() { return true; }",
            "class MyClass extends BaseClass { }",
            "import React from 'react';",
            "export default function App() {}",
            "const handler = () => { console.log('test'); }",
            "async function fetchData() {}",
            "React.useState()",
        ]
        for sample in js_samples:
            assert self.detector.detect_language(sample, "test.js") == "JavaScript"

    def test_detect_python(self):
        """Test Python detection."""
        py_samples = [
            "def test_function():\n    pass",
            "class TestClass(BaseClass):\n    pass",
            "import os",
            "from typing import List",
            "@decorator\ndef func(): pass",
            "print('Hello')",
            "if __name__ == '__main__':",
        ]
        for sample in py_samples:
            assert self.detector.detect_language(sample, "test.py") == "Python"

    def test_detect_html(self):
        """Test HTML detection."""
        html_samples = [
            "<!DOCTYPE html><html></html>",
            "<html><head><title>Test</title></head></html>",
            "<div class='test'>Content</div>",
            "<script>console.log('test');</script>",
            "<style>.test { color: red; }</style>",
        ]
        for sample in html_samples:
            assert self.detector.detect_language(sample, "test.html") == "HTML"

    def test_detect_css(self):
        """Test CSS detection."""
        css_samples = [
            ".class { color: red; }",
            "#id { margin: 0; }",
            "@media screen { body { color: blue; } }",
            "@import url('style.css');",
            "@keyframes animation { from {} to {} }",
        ]
        for sample in css_samples:
            assert self.detector.detect_language(sample, "test.css") == "CSS"

    def test_normalize_language_name(self):
        """Test language name normalization."""
        test_cases = [
            ("python", "Python"),
            ("javascript", "JavaScript"),
            ("typescript", "TypeScript"),
            ("html", "HTML"),
            ("css", "CSS"),
            ("json", "JSON"),
            ("markdown", "Markdown"),
            ("shell", "Shell"),
            ("dockerfile", "Dockerfile"),
            ("yaml", "YAML"),
            ("unknown", "Unknown"),
        ]
        for input_name, expected in test_cases:
            assert self.detector.normalize_language_name(input_name) == expected

    def test_detect_by_extension(self):
        """Test language detection by file extension."""
        test_cases = [
            ("test.py", "Python", "def test(): pass"),  # With content
            ("test.js", "JavaScript", "function test() {}"),  # With content
            ("test.ts", "TypeScript", "interface Test {}"),  # With content
            ("test.html", "HTML", "<html></html>"),  # With content
            ("test.css", "CSS", ".test {}"),  # With content
            ("test.json", "JSON", "{}"),  # With content
            ("test.md", "Markdown", "# Test"),  # With content
            ("test.sh", "Shell", "#!/bin/bash"),  # With content
            ("test.py", "Text", ""),  # Empty content
            ("test.js", "Text", ""),  # Empty content
            ("test.unknown", "Text", ""),  # Unknown extension
        ]
        for filename, expected, content in test_cases:
            assert detect_language(content, filename) == expected

    def test_detect_mixed_content(self):
        """Test detection with mixed content."""
        content = """
        def python_function():
            pass

        function javascript_function() {
            console.log('test');
        }

        <div>Some HTML</div>

        .css-class {
            color: red;
        }
        """
        # Test with different file extensions to ensure extension takes precedence
        assert self.detector.detect_language(content, "test.py") == "Python"
        assert self.detector.detect_language(content, "test.js") == "JavaScript"
        assert self.detector.detect_language(content, "test.html") == "HTML"
        assert self.detector.detect_language(content, "test.css") == "CSS"

    def test_empty_content(self):
        """Test detection with empty content."""
        assert self.detector.detect_language("", "test.py") == "Text"
        assert self.detector.detect_language("", "test.js") == "Text"
        assert self.detector.detect_language("", None) == "Text"
        assert self.detector.detect_language(None, None) == "Text"

    def test_detect_by_patterns(self):
        """Test pattern-based language detection."""
        content = """
        def test_function():
            print("Hello")
            return True
        """
        result = detect_language_by_patterns(content)
        assert result == "Python"


class TestTokenizerService:
    """Test the tokenizer service functionality."""

    def test_basic_processing(self, tokenizer_service, sample_codebase):
        """Test basic file processing."""
        # Process Python file
        python_file = Path(sample_codebase) / "main.py"
        result = tokenizer_service.process_file(str(python_file))
        assert result["success"]
        assert result["language"] == "Python"
        assert result["tokens"] > 0

        # Process JSON file
        json_file = Path(sample_codebase) / "config.json"
        result = tokenizer_service.process_file(str(json_file))
        assert result["success"]
        assert result["language"] == "JSON"
        assert result["tokens"] > 0

    def test_directory_processing(self, tmp_path):
        """Test processing a directory."""
        # Create test files
        test_files = {
            "test1.py": "def test(): pass",
            "test2.js": "function test() {}",
            "test3.txt": "Plain text file",
        }

        for filename, content in test_files.items():
            (tmp_path / filename).write_text(content)

        config = TokenizerConfig({"base_dir": str(tmp_path)})
        tokenizer_service = TokenizerService(config)
        stats = tokenizer_service.process_directory(str(tmp_path))

        assert "stats" in stats
        assert stats["stats"]["files_processed"] == len(test_files)
        assert stats["stats"]["total_tokens"] > 0
        assert len(stats["successful_files"]) == len(test_files)
        assert len(stats["failed_files"]) == 0

    def test_error_handling(self, tokenizer_service, temp_dir):
        """Test error handling in TokenizerService."""
        # Test with non-existent file
        non_existent = Path(temp_dir) / "non_existent.txt"
        result = tokenizer_service.process_file(str(non_existent))
        assert not result["success"]
        assert result["language"] == "unknown"
        assert result["tokens"] == 0
        assert "error" in result

    def test_initialization_options(self):
        """Test tokenizer service initialization with different options."""
        config = TokenizerConfig(
            {"model_name": "gpt-4o", "max_tokens": 200000, "output_format": "markdown"}
        )
        service = TokenizerService(config)
        assert service.model_name == "gpt-4o"
        assert service.max_tokens == 200000

    def test_truncate_text(self):
        """Test truncating text with an invalid model."""
        config = TokenizerConfig({"model_name": "gpt-4o"})
        tokenizer_service = TokenizerService(config)
        with pytest.raises(ModelNotSupportedError):
            tokenizer_service.tokenizer.truncate_text("test text", "invalid-model", 10)
