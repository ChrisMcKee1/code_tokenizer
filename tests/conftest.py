"""Test configuration and fixtures."""

import os
from typing import Dict

import pytest

from code_tokenizer.models.model_config import TokenizerConfig
from code_tokenizer.services.filesystem_service import FileSystemService, MockFileSystemService
from code_tokenizer.services.tokenizer_service import TokenizerService


@pytest.fixture(scope="module")
def mock_fs() -> MockFileSystemService:
    """Create a mock file system service.

    Returns:
        MockFileSystemService: Mock file system service
    """
    return MockFileSystemService()


class BaseFileSystemTest:
    """Base class for file system tests."""

    def setup_method(self):
        """Set up test method."""
        self.fs_service = self.get_fs_service()
        self.config = self.get_config()
        self.tokenizer = TokenizerService(self.config, self.fs_service)

    def get_fs_service(self) -> FileSystemService:
        """Get file system service for tests.

        Returns:
            FileSystemService: File system service instance
        """
        return MockFileSystemService()

    def get_config(self) -> TokenizerConfig:
        """Get tokenizer config for tests.

        Returns:
            TokenizerConfig: Tokenizer configuration
        """
        return TokenizerConfig(
            {
                "model_name": "gpt-4o",
                "max_tokens": 200000,
                "output_format": "markdown",
                "bypass_gitignore": False,
                "include_metadata": True,
            }
        )

    def setup_sample_codebase(self, fs_service, base_dir):
        """Set up a sample codebase in the mock filesystem."""
        # Create the base directory
        base_dir = str(base_dir)
        fs_service.create_directory(base_dir)

        # Sample files with content
        files = {
            "main.py": 'def main():\n    print("Hello, World!")\n\nif __name__ == "__main__":\n    main()',
            "config.json": '{\n    "name": "sample-project",\n    "version": "1.0.0"\n}',
            "styles.css": "body {\n    background-color: #f0f0f0;\n}",
            "index.html": "<!DOCTYPE html>\n<html><body><h1>Hello</h1></body></html>",
            "script.js": 'console.log("Hello from JavaScript!");',
            ".gitignore": "*.pyc\n__pycache__\n.env",
        }

        # Create each file
        for filename, content in files.items():
            file_path = os.path.join(base_dir, filename)
            # Normalize path to use forward slashes
            file_path = file_path.replace(os.sep, '/')
            fs_service.write_file(file_path, content)

        return base_dir


@pytest.fixture
def temp_dir(tmp_path):
    """Create a temporary directory for testing.

    Args:
        tmp_path (Path): Pytest's temporary directory fixture

    Returns:
        Path: Path to temporary directory
    """
    return tmp_path


@pytest.fixture
def sample_codebase(temp_dir):
    """Create a sample codebase directory.

    Args:
        temp_dir (Path): Temporary directory

    Returns:
        Path: Path to sample codebase
    """
    codebase_dir = temp_dir / "sample_codebase"
    codebase_dir.mkdir(exist_ok=True)

    # Sample files with content
    files = {
        "main.py": 'def main():\n    print("Hello, World!")\n\nif __name__ == "__main__":\n    main()',
        "config.json": '{\n    "name": "sample-project",\n    "version": "1.0.0"\n}',
        "styles.css": "body {\n    background-color: #f0f0f0;\n}",
        "index.html": "<!DOCTYPE html>\n<html><body><h1>Hello</h1></body></html>",
        "script.js": 'console.log("Hello from JavaScript!");',
        ".gitignore": "*.pyc\n__pycache__\n.env",
    }

    # Create each file
    for filename, content in files.items():
        file_path = codebase_dir / filename
        file_path.write_text(content)

    return codebase_dir


@pytest.fixture
def test_config(temp_dir: str) -> TokenizerConfig:
    """Create a test configuration.

    Args:
        temp_dir: Temporary directory path

    Returns:
        TokenizerConfig: Test configuration
    """
    return TokenizerConfig(
        {
            "base_dir": temp_dir,
            "output_dir": os.path.join(temp_dir, "output"),
            "model_name": "gpt-4o",
            "max_tokens": 200000,
            "output_format": "markdown",
            "bypass_gitignore": False,
            "include_metadata": True,
        }
    )


@pytest.fixture
def tokenizer_service(
    test_config: TokenizerConfig, mock_fs: MockFileSystemService
) -> TokenizerService:
    """Create a tokenizer service for testing.

    Args:
        test_config: Test configuration
        mock_fs: Mock file system service

    Returns:
        TokenizerService: Configured tokenizer service
    """
    # Set up sample files in mock filesystem
    files = {
        "main.py": 'def main():\n    print("Hello, World!")\n\nif __name__ == "__main__":\n    main()',
        "config.json": '{\n    "name": "sample-project",\n    "version": "1.0.0"\n}',
        "styles.css": "body {\n    background-color: #f0f0f0;\n}",
        "index.html": "<!DOCTYPE html>\n<html><body><h1>Hello</h1></body></html>",
        "script.js": 'console.log("Hello from JavaScript!");',
        ".gitignore": "*.pyc\n__pycache__\n.env",
    }

    # Create each file in the mock filesystem
    for filename, content in files.items():
        file_path = os.path.join(test_config.base_dir, "sample_codebase", filename)
        mock_fs.create_directory(os.path.dirname(file_path))
        mock_fs.write_file(file_path, content)

    return TokenizerService(test_config, mock_fs)


@pytest.fixture
def test_files(mock_fs: MockFileSystemService, temp_dir: str) -> Dict[str, str]:
    """Create test files.

    Args:
        mock_fs: Mock file system service
        temp_dir: Temporary directory path

    Returns:
        Dict[str, str]: Dictionary mapping file paths to content
    """
    files = {
        "test.py": "def test():\n    pass\n",
        "test.js": "function test() {\n    console.log('test');\n}\n",
        "test.html": "<html><body>Test</body></html>\n",
        "test.css": "body { color: red; }\n",
        "test.json": '{"test": "value"}\n',
        "test.md": "# Test\n\nThis is a test.\n",
    }

    for filename, content in files.items():
        file_path = os.path.join(temp_dir, filename)
        mock_fs.create_directory(os.path.dirname(file_path))
        mock_fs.write_file(file_path, content)

    return files
