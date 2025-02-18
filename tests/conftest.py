"""Shared test fixtures and configuration."""

import os
import shutil
import tempfile
from pathlib import Path

import pytest
from rich.console import Console


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_codebase(temp_dir):
    """Create a sample codebase structure for testing."""
    # Create Python file
    python_file = Path(temp_dir) / "main.py"
    python_file.write_text(
        """
def hello_world():
    print("Hello, World!")
    
if __name__ == "__main__":
    hello_world()
"""
    )

    # Create JSON file
    json_file = Path(temp_dir) / "config.json"
    json_file.write_text(
        """
{
    "name": "test",
    "version": "1.0.0"
}
"""
    )

    # Create .gitignore
    gitignore = Path(temp_dir) / ".gitignore"
    gitignore.write_text(
        """
__pycache__/
*.pyc
temp/
"""
    )

    # Create ignored directory and file
    temp_path = Path(temp_dir) / "temp"
    temp_path.mkdir()
    (temp_path / "ignored.txt").write_text("This should be ignored")

    # Create a file that should be ignored by extension
    (Path(temp_dir) / "test.pyc").write_text("This should be ignored")

    return temp_dir


@pytest.fixture
def console():
    """Create a console instance that suppresses output during tests."""
    return Console(file=open(os.devnull, "w"))


@pytest.fixture
def tokenizer_service(temp_dir):
    """Create a TokenizerService instance for testing."""
    from code_tokenizer.services.tokenizer_service import TokenizerService

    config = {
        "base_dir": temp_dir,
        "model_name": "claude-3-sonnet",
        "max_tokens_per_file": 2000,
        "output_format": "markdown",
        "output_dir": str(Path(temp_dir) / "output"),
        "include_metadata": True,
        "custom_gitignore": str(Path(temp_dir) / ".gitignore"),
    }
    return TokenizerService(config)
