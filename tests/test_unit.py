"""Unit tests for code tokenizer components."""

import pytest
from pathlib import Path
from unittest.mock import patch

from code_tokenizer.core.tokenizer import count_tokens, truncate_text
from code_tokenizer.services.language_detector import LanguageDetector
from code_tokenizer.utils.path_utils import should_ignore_path, normalize_path, get_relative_path
from code_tokenizer.models.model_config import (
    MODEL_CONTEXT_SIZES,
    MODEL_ENCODINGS,
    get_model_encoding,
    get_model_token_limit,
    DEFAULT_MODEL
)

class TestModelConfig:
    """Test model configuration functionality."""
    
    def test_model_context_sizes(self):
        """Test model context size configurations."""
        # Test that all models have context sizes
        for model in MODEL_ENCODINGS.keys():
            assert model in MODEL_CONTEXT_SIZES
            assert MODEL_CONTEXT_SIZES[model] > 0
    
    def test_model_encodings(self):
        """Test model encoding configurations."""
        # Test that all models have encodings
        for model in MODEL_CONTEXT_SIZES.keys():
            assert model in MODEL_ENCODINGS
            assert MODEL_ENCODINGS[model] in ["cl100k_base", "p50k_base", "r50k_base"]
    
    def test_get_model_encoding(self):
        """Test getting model encodings."""
        # Test valid models
        assert get_model_encoding("claude-3-sonnet") == "cl100k_base"
        assert get_model_encoding("gpt-4") == "cl100k_base"
        
        # Test invalid model
        with pytest.raises(ValueError):
            get_model_encoding("invalid-model")
    
    def test_get_model_token_limit(self):
        """Test getting model token limits."""
        # Test valid models
        assert get_model_token_limit("claude-3-sonnet") == 200000
        assert get_model_token_limit("gpt-4") == 8192
        
        # Test invalid model
        with pytest.raises(ValueError):
            get_model_token_limit("invalid-model")

class TestPathUtils:
    """Test path utility functions."""
    
    def test_normalize_path(self):
        """Test path normalization."""
        # Test Windows paths
        assert normalize_path("path\\to\\file") == "path/to/file"
        assert normalize_path(".\\relative\\path") == "relative/path"
        
        # Test Unix paths
        assert normalize_path("path/to/file") == "path/to/file"
        assert normalize_path("./relative/path") == "relative/path"
    
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

class TestCoreFeatures:
    """Test core features of the code tokenizer."""
    
    def test_token_counting(self):
        """Test token counting with various inputs and models."""
        # Basic counting
        assert count_tokens("Hello, World!", "claude-3-sonnet") > 0
        assert count_tokens("", "claude-3-sonnet") == 0
        
        # Test different models
        text = "This is a test sentence."
        tokens_claude = count_tokens(text, "claude-3-sonnet")
        tokens_gpt = count_tokens(text, "gpt-4")
        assert tokens_claude > 0
        assert tokens_gpt > 0
        
        # Edge cases
        assert count_tokens(" ", "claude-3-sonnet") > 0  # Just whitespace
        assert count_tokens("\n\n\n", "claude-3-sonnet") > 0  # Just newlines
        assert count_tokens("a" * 1000, "claude-3-sonnet") > 0  # Long repetitive text
    
    def test_language_detection(self):
        """Test language detection for different file types."""
        assert LanguageDetector.detect_language("test.py") == "Python"
        assert LanguageDetector.detect_language("test.json") == "JSON"
        assert LanguageDetector.detect_language("test.md") == "Markdown"
        assert LanguageDetector.detect_language("test.unknown") == "text"
    
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
        truncated, count = truncate_text(text, 10, "claude-3-sonnet")
        assert truncated == text
        assert count < 10
        
        # Test truncation
        long_text = "This is a longer text that needs to be truncated." * 100
        truncated, count = truncate_text(long_text, 20, "claude-3-sonnet")
        assert len(truncated) < len(long_text)
        assert count == 20
        
        # Test with different models
        text = "Test text for different models."
        t1, c1 = truncate_text(text, 10, "claude-3-sonnet")
        t2, c2 = truncate_text(text, 10, "gpt-4")
        assert len(t1) > 0
        assert len(t2) > 0
        
        # Test invalid model
        with pytest.raises(ValueError):
            truncate_text(text, 10, "invalid-model")

class TestTokenizerService:
    """Test TokenizerService functionality."""
    
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
    
    def test_directory_processing(self, tokenizer_service, sample_codebase):
        """Test processing an entire directory."""
        stats = tokenizer_service.process_directory()
        assert stats["files_processed"] > 0
        assert stats["total_tokens"] > 0
        assert "Python" in stats["languages"]
        assert "JSON" in stats["languages"]
        assert stats["skipped_files"] > 0  # Should skip ignored files
    
    def test_error_handling(self, tokenizer_service, temp_dir):
        """Test error handling in TokenizerService."""
        # Test with non-existent file
        non_existent = Path(temp_dir) / "non_existent.txt"
        result = tokenizer_service.process_file(str(non_existent))
        assert not result["success"]
        assert result["language"] == "unknown"
        assert result["tokens"] == 0
        assert "error" in result

    def test_initialization_options(self, temp_dir):
        """Test TokenizerService initialization with different options."""
        # Test with minimal config
        config = {
            "base_dir": temp_dir
        }
        service = TokenizerService(config)
        assert service.model_name == DEFAULT_MODEL
        assert service.max_tokens == 2000
        assert service.output_format == "markdown"
        assert service.include_metadata is True
        
        # Test with custom config
        config = {
            "base_dir": temp_dir,
            "model_name": "gpt-4",
            "max_tokens_per_file": 5000,
            "output_format": "json",
            "output_dir": "custom_output",
            "include_metadata": False
        }
        service = TokenizerService(config)
        assert service.model_name == "gpt-4"
        assert service.max_tokens == 5000
        assert service.output_format == "json"
        assert service.include_metadata is False
        
        # Test with custom gitignore
        gitignore = Path(temp_dir) / ".custom_gitignore"
        gitignore.write_text("*.custom\ntest_dir/")
        config = {
            "base_dir": temp_dir,
            "custom_gitignore": str(gitignore)
        }
        service = TokenizerService(config)
        assert "*.custom" in service.ignore_patterns
        assert "test_dir/" in service.ignore_patterns 