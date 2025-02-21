"""Tests for file content models."""

import dataclasses
from pathlib import Path

import pytest

from code_tokenizer.models.content import FileContent


@pytest.fixture
def sample_content() -> str:
    """Sample file content for testing."""
    return "def test():\n    print('hello')"


@pytest.fixture
def sample_file_info(tmp_path: Path) -> tuple[Path, Path]:
    """Create a sample file structure for testing.

    Returns:
        tuple[Path, Path]: (root_dir, file_path)
    """
    root_dir = tmp_path / "project"
    root_dir.mkdir()

    file_path = root_dir / "src" / "test.py"
    file_path.parent.mkdir()
    file_path.write_text("def test():\n    print('hello')")

    return root_dir, file_path


def test_file_content_creation():
    """Test basic FileContent creation."""
    content = FileContent(
        name="test.py",
        path="/path/to/test.py",
        relative_path="src/test.py",
        language="Python",
        token_count=10,
        content="def test(): pass",
        size=15,
        encoding="utf-8",
    )

    assert content.name == "test.py"
    assert content.path == "/path/to/test.py"
    assert content.relative_path == "src/test.py"
    assert content.language == "Python"
    assert content.token_count == 10
    assert content.content == "def test(): pass"
    assert content.size == 15
    assert content.encoding == "utf-8"


def test_path_normalization():
    """Test path normalization with different separators."""
    content = FileContent(
        name="test.py",
        path="C:\\path\\to\\test.py",
        relative_path="src\\test.py",
        language="Python",
        token_count=10,
        content="def test(): pass",
        size=15,
        encoding="utf-8",
    )

    assert content.path == "C:/path/to/test.py"
    assert content.relative_path == "src/test.py"


def test_invalid_encoding():
    """Test validation of supported encodings."""
    with pytest.raises(ValueError, match="Unsupported encoding"):
        FileContent(
            name="test.py",
            path="/path/to/test.py",
            relative_path="src/test.py",
            language="Python",
            token_count=10,
            content="def test(): pass",
            size=15,
            encoding="invalid-encoding",  # type: ignore
        )


def test_from_path_factory(sample_file_info: tuple[Path, Path], sample_content: str):
    """Test FileContent.from_path factory method."""
    root_dir, file_path = sample_file_info

    content = FileContent.from_path(
        file_path=file_path,
        root_dir=root_dir,
        content=sample_content,
        language="Python",
        token_count=8,
        encoding="utf-8",
    )

    assert content.name == "test.py"
    assert Path(content.path).is_absolute()
    assert content.relative_path == "src/test.py"
    assert content.language == "Python"
    assert content.token_count == 8
    assert content.content == sample_content
    assert content.size == len(sample_content.encode("utf-8"))
    assert content.encoding == "utf-8"


def test_from_path_with_string_paths():
    """Test factory method with string paths."""
    content = FileContent.from_path(
        file_path="test.py",
        root_dir=".",
        content="test content",
        language="Python",
        token_count=2,
        encoding="utf-8",
    )

    assert isinstance(content, FileContent)
    assert content.name == "test.py"
    assert "/" in content.path  # Should be normalized
    assert isinstance(content.path, str)


def test_as_dict_conversion():
    """Test conversion to dictionary."""
    content = FileContent(
        name="test.py",
        path="/path/to/test.py",
        relative_path="src/test.py",
        language="Python",
        token_count=10,
        content="def test(): pass",
        size=15,
        encoding="utf-8",
    )

    data = content.as_dict
    assert isinstance(data, dict)
    assert data["name"] == "test.py"
    assert data["path"] == "/path/to/test.py"
    assert data["relative_path"] == "src/test.py"
    assert data["language"] == "Python"
    assert data["token_count"] == 10
    assert data["content"] == "def test(): pass"
    assert data["size"] == 15
    assert data["encoding"] == "utf-8"


def test_string_representation():
    """Test string representation."""
    content = FileContent(
        name="test.py",
        path="/path/to/test.py",
        relative_path="src/test.py",
        language="Python",
        token_count=10,
        content="def test(): pass",
        size=15,
        encoding="utf-8",
    )

    str_rep = str(content)
    assert "test.py" in str_rep
    assert "Python" in str_rep
    assert "10 tokens" in str_rep
    assert "15 bytes" in str_rep
    assert "def test(): pass" not in str_rep  # Content should not be in string rep


def test_immutability():
    """Test that FileContent is immutable."""
    content = FileContent(
        name="test.py",
        path="/path/to/test.py",
        relative_path="src/test.py",
        language="Python",
        token_count=10,
        content="def test(): pass",
        size=15,
        encoding="utf-8",
    )

    with pytest.raises(dataclasses.FrozenInstanceError):
        content.name = "new.py"  # type: ignore

    with pytest.raises(dataclasses.FrozenInstanceError):
        content.path = "new/path"  # type: ignore
