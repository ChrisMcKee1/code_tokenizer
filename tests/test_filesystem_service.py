"""Tests for the filesystem service."""

import os

import pytest

from code_tokenizer.services.filesystem_service import MockFileSystemService, RealFileSystemService


@pytest.fixture
def real_fs():
    """Create a real filesystem service."""
    return RealFileSystemService()


@pytest.fixture
def mock_fs():
    """Create a mock filesystem service."""
    return MockFileSystemService()


def test_create_directory(real_fs, mock_fs):
    """Test creating directories."""
    test_dir = "test_dir"

    # Test real fs
    assert real_fs.create_directory(test_dir)
    assert os.path.exists(test_dir)
    assert os.path.isdir(test_dir)
    os.rmdir(test_dir)

    # Test mock fs
    assert mock_fs.create_directory(test_dir)
    assert mock_fs.exists(test_dir)
    assert mock_fs.is_directory(test_dir)


def test_write_and_read_file(real_fs, mock_fs):
    """Test writing and reading files."""
    test_file = "test.txt"
    content = "Hello, World!"

    # Test real fs
    assert real_fs.write_file(test_file, content)
    assert os.path.exists(test_file)
    assert real_fs.read_file(test_file) == content
    os.remove(test_file)

    # Test mock fs
    assert mock_fs.write_file(test_file, content)
    assert mock_fs.exists(test_file)
    assert mock_fs.read_file(test_file) == content


def test_read_file_chunk(real_fs, mock_fs):
    """Test reading file chunks."""
    test_file = "test_chunk.txt"
    content = b"Hello, World! This is a test of chunked reading."

    # Test real fs
    assert real_fs.write_file(test_file, content)
    chunk = real_fs.read_file_chunk(test_file, 0, 5)
    assert chunk == b"Hello"
    chunk = real_fs.read_file_chunk(test_file, 7, 5)
    assert chunk == b"World"
    os.remove(test_file)

    # Test mock fs
    assert mock_fs.write_file(test_file, content)
    chunk = mock_fs.read_file_chunk(test_file, 0, 5)
    assert chunk == b"Hello"
    chunk = mock_fs.read_file_chunk(test_file, 7, 5)
    assert chunk == b"World"


def test_read_file_chunk_errors(real_fs, mock_fs):
    """Test error cases for reading file chunks."""
    test_file = "test_chunk_errors.txt"
    content = "Hello, World!"

    # Create test file first
    real_fs.write_file(test_file, content)
    mock_fs.write_file(test_file, content)

    try:
        # Test invalid offset
        with pytest.raises(ValueError):
            real_fs.read_file_chunk(test_file, -1, 5)
        with pytest.raises(ValueError):
            mock_fs.read_file_chunk(test_file, -1, 5)

        # Test invalid size
        with pytest.raises(ValueError):
            real_fs.read_file_chunk(test_file, 0, 0)
        with pytest.raises(ValueError):
            mock_fs.read_file_chunk(test_file, 0, -1)

        # Test non-existent file
        with pytest.raises(FileNotFoundError):
            real_fs.read_file_chunk("nonexistent.txt", 0, 5)
        with pytest.raises(FileNotFoundError):
            mock_fs.read_file_chunk("nonexistent.txt", 0, 5)
    finally:
        # Clean up
        if os.path.exists(test_file):
            os.remove(test_file)


def test_check_permissions(real_fs, mock_fs):
    """Test checking permissions."""
    test_file = "test_perms.txt"
    content = "Hello, World!"

    # Test real fs
    assert real_fs.write_file(test_file, content)
    assert real_fs.check_permissions(test_file)
    os.remove(test_file)

    # Test mock fs
    assert mock_fs.write_file(test_file, content)
    assert mock_fs.check_permissions(test_file)


def test_delete(real_fs, mock_fs):
    """Test deleting files and directories."""
    test_file = "test_delete.txt"
    test_dir = "test_delete_dir"
    content = "Hello, World!"

    # Test real fs
    assert real_fs.write_file(test_file, content)
    assert real_fs.create_directory(test_dir)
    assert real_fs.delete(test_file)
    assert real_fs.delete(test_dir)
    assert not os.path.exists(test_file)
    assert not os.path.exists(test_dir)

    # Test mock fs
    assert mock_fs.write_file(test_file, content)
    assert mock_fs.create_directory(test_dir)
    assert mock_fs.delete(test_file)
    assert mock_fs.delete(test_dir)
    assert not mock_fs.exists(test_file)
    assert not mock_fs.exists(test_dir)


def test_list_files(real_fs, mock_fs):
    """Test listing files."""
    test_dir = "test_list"
    test_files = ["file1.txt", "file2.txt"]
    content = "Hello, World!"

    try:
        # Test real fs
        real_fs.create_directory(test_dir)
        for file in test_files:
            path = os.path.join(test_dir, file)
            real_fs.write_file(path, content)
        files = real_fs.list_files(test_dir)
        assert len(files) == 2
        expected_files = [os.path.join(test_dir, f).replace(os.sep, "/") for f in test_files]
        assert sorted(files) == sorted(expected_files)

        # Test mock fs
        mock_fs.create_directory(test_dir)
        for file in test_files:
            path = os.path.join(test_dir, file)
            mock_fs.write_file(path, content)
        files = mock_fs.list_files(test_dir)
        assert len(files) == 2
        assert sorted(files) == sorted(expected_files)
    finally:
        # Clean up
        if os.path.exists(test_dir):
            real_fs.delete(test_dir)


def test_get_file_size(real_fs, mock_fs):
    """Test getting file size."""
    test_file = "test_size.txt"
    content = "Hello, World!"

    # Test real fs
    assert real_fs.write_file(test_file, content)
    assert real_fs.get_file_size(test_file) == len(content.encode("utf-8"))
    os.remove(test_file)

    # Test mock fs
    assert mock_fs.write_file(test_file, content)
    assert mock_fs.get_file_size(test_file) == len(content.encode("utf-8"))


def test_binary_file(real_fs, mock_fs):
    """Test handling binary files."""
    test_file = "test_binary.bin"
    content = bytes([0x00, 0x01, 0x02, 0x03])

    try:
        # Test real fs
        assert real_fs.write_file(test_file, content)
        read_content = real_fs.read_file(test_file)
        assert isinstance(read_content, bytes)
        assert read_content == content

        # Test mock fs
        assert mock_fs.write_file(test_file, content)
        read_content = mock_fs.read_file(test_file)
        assert isinstance(read_content, bytes)
        assert read_content == content
    finally:
        # Clean up
        if os.path.exists(test_file):
            os.remove(test_file)
