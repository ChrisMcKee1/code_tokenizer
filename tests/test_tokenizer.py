"""Unit tests for code tokenizer components."""

import pytest
import tiktoken

from code_tokenizer.core.tokenizer import CodeTokenizer, count_tokens, truncate_text
from code_tokenizer.exceptions import ModelNotSupportedError
from code_tokenizer.models.model_config import get_model_encoding


class TestTokenizer:
    """Test tokenizer core functionality."""

    @pytest.mark.unit
    @pytest.mark.smoke
    def test_count_tokens(self):
        """Test token counting."""
        text = "Hello, world!"
        model_name = "gpt-4o"
        token_count = count_tokens(text, model_name)
        assert isinstance(token_count, int)
        assert token_count > 0

    @pytest.mark.unit
    def test_count_tokens_invalid_model(self):
        """Test token counting with invalid model."""
        with pytest.raises(ModelNotSupportedError):
            count_tokens("test", "invalid-model")

    @pytest.mark.unit
    @pytest.mark.smoke
    def test_truncate_text(self):
        """Test text truncation."""
        text = "This is a long text that needs to be truncated."
        model_name = "gpt-4o"
        max_tokens = 5
        truncated, count = truncate_text(text, max_tokens, model_name)
        assert count <= max_tokens
        assert len(truncated) < len(text)

    @pytest.mark.unit
    def test_truncate_text_no_truncation_needed(self):
        """Test truncation when text is already within limits."""
        text = "Short text"
        model_name = "gpt-4o"
        max_tokens = 100
        truncated, count = truncate_text(text, max_tokens, model_name)
        assert truncated == text
        assert count < max_tokens

    @pytest.mark.unit
    def test_truncate_text_invalid_model(self):
        """Test truncation with invalid model."""
        with pytest.raises(ModelNotSupportedError):
            truncate_text("test", 10, "invalid-model")


class TestCodeTokenizer:
    """Test CodeTokenizer class functionality."""

    @pytest.mark.unit
    def test_initialization(self):
        """Test tokenizer initialization."""
        tokenizer = CodeTokenizer()
        assert tokenizer.model_name == "gpt-4o"
        assert tokenizer.max_tokens == 8192
        assert isinstance(tokenizer.encoding, tiktoken.Encoding)

    @pytest.mark.unit
    def test_count_tokens_method(self):
        """Test count_tokens method."""
        tokenizer = CodeTokenizer("gpt-4o")
        text = "def test(): pass"
        count = tokenizer.count_tokens(text)
        assert isinstance(count, int)
        assert count > 0

    @pytest.mark.unit
    def test_truncate_to_token_limit(self):
        """Test truncation to token limit."""
        tokenizer = CodeTokenizer("gpt-4o")
        text = "This is a long text that needs to be truncated."
        max_tokens = 5
        truncated = tokenizer.truncate_to_token_limit(text, max_tokens)
        assert tokenizer.count_tokens(truncated) <= max_tokens

    @pytest.mark.unit
    def test_truncate_to_token_limit_no_truncation(self):
        """Test truncation when no truncation is needed."""
        tokenizer = CodeTokenizer("gpt-4o")
        text = "Short text"
        max_tokens = 100
        truncated = tokenizer.truncate_to_token_limit(text, max_tokens)
        assert truncated == text

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "model,text,expected_range",
        [
            ("gpt-4o", "Hello, world!", (2, 10)),
            ("o1-preview", "def test(): pass", (4, 10)),
            ("gpt-3.5-turbo", "print('test')", (3, 10)),
        ],
    )
    def test_different_models(self, model, text, expected_range):
        """Test token counting with different models."""
        tokenizer = CodeTokenizer(model)
        count = tokenizer.count_tokens(text)
        assert (
            expected_range[0] <= count <= expected_range[1]
        ), f"Token count {count} not in range {expected_range} for model {model}"
