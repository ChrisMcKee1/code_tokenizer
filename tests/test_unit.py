"""Unit tests for code tokenizer components."""

import pytest

from code_tokenizer.core.tokenizer import count_tokens, truncate_text
from code_tokenizer.models.model_config import (
    MODEL_ENCODINGS,
    Encoding,
    get_model_encoding,
    get_model_token_limit,
)
from code_tokenizer.services.language_detector import detect_language
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
        print("\n=== Testing Python Detection ===")
        result = detect_language("def test(): pass", "test.py")
        print(f"Python test - Input: 'def test(): pass', Filename: test.py, Result: {result}")
        assert result == "Python"

        print("\n=== Testing JSON Detection ===")
        result = detect_language('{"test": true}', "test.json")
        print(f'JSON test - Input: {{"test": true}}, Filename: test.json, Result: {result}')
        assert result == "JSON"

        print("\n=== Testing Markdown Detection ===")
        result = detect_language("# Test\n## Header", "test.md")
        print(f"Markdown test - Input: '# Test\\n## Header', Filename: test.md, Result: {result}")
        assert result == "Markdown"

        print("\n=== Testing Plain Text Detection ===")
        result = detect_language("random text", "test.txt")
        print(f"Text test - Input: 'random text', Filename: test.txt, Result: {result}")
        assert result == "Text"

        # Test empty content cases
        assert detect_language("", "test.py") == "Text"
        assert detect_language(None, "test.py") == "Text"
        assert detect_language("   \n  ", "test.py") == "Text"

        # Test case sensitivity
        assert detect_language("def test(): pass", "TEST.PY") == "Python"
        assert detect_language('{"test": true}', "TEST.JSON") == "JSON"
        assert detect_language("# Header", "TEST.MD") == "Markdown"
        assert detect_language("random text", "TEST.TXT") == "Text"

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

        # Test truncation needed
        long_text = (
            "This is a much longer text that needs to be truncated to fit within the token limit."
        )
        truncated, count = truncate_text(long_text, 10, "gpt-4o")
        assert len(truncated) < len(long_text)
        assert count <= 10

        # Test edge cases
        assert truncate_text("", 10, "gpt-4o")[0] == ""
        assert truncate_text(" ", 10, "gpt-4o")[0] == " "
        assert truncate_text("\n\n", 10, "gpt-4o")[0] == "\n\n"
