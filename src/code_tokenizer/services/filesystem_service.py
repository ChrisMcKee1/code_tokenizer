"""File system service for handling file operations."""

import logging
import os
import shutil
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union

# Configure logging
logger = logging.getLogger(__name__)


class FileSystemService(ABC):
    """Base class for file system operations."""

    @abstractmethod
    def create_directory(self, path: str, permissions: Optional[int] = None) -> bool:
        """Create a directory with optional permissions.

        Args:
            path: Directory path to create
            permissions: Optional Unix-style permissions (e.g. 0o777)

        Returns:
            bool: True if successful
        """
        pass

    @abstractmethod
    def write_file(
        self, path: str, content: Union[str, bytes], permissions: Optional[int] = None
    ) -> bool:
        """Write content to a file with optional permissions.

        Args:
            path: File path to write to
            content: Content to write (string or bytes)
            permissions: Optional Unix-style permissions (e.g. 0o666)

        Returns:
            bool: True if successful
        """
        pass

    @abstractmethod
    def read_file(self, path: str) -> Union[str, bytes]:
        """Read content from a file.

        Args:
            path: File path to read from

        Returns:
            Union[str, bytes]: File content

        Raises:
            FileNotFoundError: If file does not exist
        """
        pass

    @abstractmethod
    def read_file_chunk(self, path: str, offset: int, size: int) -> bytes:
        """Read a chunk of data from a file.

        Args:
            path: File path to read from
            offset: Starting position in file
            size: Number of bytes to read

        Returns:
            bytes: Chunk of file data

        Raises:
            FileNotFoundError: If file does not exist
            ValueError: If offset or size is invalid
        """
        pass

    @abstractmethod
    def check_permissions(self, path: str) -> bool:
        """Check if we have read/write permissions for a path.

        Args:
            path: Path to check

        Returns:
            bool: True if we have read/write access
        """
        pass

    @abstractmethod
    def delete(self, path: str) -> bool:
        """Delete a file or directory.

        Args:
            path: Path to delete

        Returns:
            bool: True if successful
        """
        pass

    @abstractmethod
    def exists(self, path: str) -> bool:
        """Check if a path exists.

        Args:
            path: Path to check

        Returns:
            bool: True if exists
        """
        pass

    @abstractmethod
    def is_file(self, path: str) -> bool:
        """Check if path is a file.

        Args:
            path: Path to check

        Returns:
            bool: True if path is a file
        """
        pass

    @abstractmethod
    def is_directory(self, path: str) -> bool:
        """Check if path is a directory.

        Args:
            path: Path to check

        Returns:
            bool: True if path is a directory
        """
        pass

    @abstractmethod
    def list_files(self, directory: str, recursive: bool = False) -> List[str]:
        """List all files in a directory.

        Args:
            directory: Directory to list files from
            recursive: Whether to list files recursively

        Returns:
            List[str]: List of file paths
        """
        pass

    @abstractmethod
    def get_file_size(self, file_path: str) -> int:
        """Get the size of a file in bytes.

        Args:
            file_path: Path to the file

        Returns:
            int: Size of the file in bytes

        Raises:
            FileNotFoundError: If file does not exist
        """
        pass


class RealFileSystemService(FileSystemService):
    """Real file system implementation."""

    def create_directory(self, path: str, permissions: Optional[int] = None) -> bool:
        """Create a directory with optional permissions."""
        try:
            os.makedirs(path, exist_ok=True)
            if permissions is not None:
                try:
                    os.chmod(path, permissions)
                except OSError:
                    logger.warning(f"Failed to set permissions on directory: {path}")
            return True
        except OSError as e:
            logger.error(f"Failed to create directory {path}: {str(e)}")
            return False

    def write_file(
        self, path: str, content: Union[str, bytes], permissions: Optional[int] = None
    ) -> bool:
        """Write content to a file with optional permissions."""
        try:
            # Create parent directory if it doesn't exist
            parent = os.path.dirname(path)
            if parent:
                self.create_directory(parent)

            # Write content
            mode = "wb" if isinstance(content, bytes) else "w"
            encoding = None if isinstance(content, bytes) else "utf-8"

            with open(path, mode, encoding=encoding) as f:
                f.write(content)

            # Set permissions if specified
            if permissions is not None:
                try:
                    os.chmod(path, permissions)
                except OSError:
                    logger.warning(f"Failed to set permissions on file: {path}")
            return True
        except OSError as e:
            logger.error(f"Failed to write file {path}: {str(e)}")
            return False

    def read_file(self, path: str) -> Union[str, bytes]:
        """Read content from a file."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")

        try:
            # Always read as binary first
            with open(path, "rb") as f:
                content = f.read()

            # Try to decode as text if it looks like text
            try:
                # Check if content is likely binary
                if b"\x00" in content or any(byte > 127 for byte in content):
                    return content
                return content.decode("utf-8")
            except UnicodeDecodeError:
                return content
        except OSError as e:
            logger.error(f"Failed to read file {path}: {str(e)}")
            raise

    def read_file_chunk(self, path: str, offset: int, size: int) -> bytes:
        """Read a chunk of data from a file.

        Args:
            path: File path to read from
            offset: Starting position in file
            size: Number of bytes to read

        Returns:
            bytes: Chunk of file data

        Raises:
            FileNotFoundError: If file does not exist
            ValueError: If offset or size is invalid
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")

        if offset < 0:
            raise ValueError("Offset must be non-negative")

        if size <= 0:
            raise ValueError("Size must be positive")

        try:
            with open(path, "rb") as f:
                f.seek(offset)
                return f.read(size)
        except OSError as e:
            logger.error(f"Failed to read chunk from {path}: {str(e)}")
            raise

    def check_permissions(self, path: str) -> bool:
        """Check if we have read/write permissions for a path."""
        if not os.path.exists(path):
            # Check parent directory for new files/dirs
            path = os.path.dirname(path)
            if not path or not os.path.exists(path):
                return False
        return os.access(path, os.R_OK | os.W_OK)

    def delete(self, path: str) -> bool:
        """Delete a file or directory."""
        try:
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
            return True
        except OSError as e:
            logger.error(f"Failed to delete {path}: {str(e)}")
            return False

    def exists(self, path: str) -> bool:
        """Check if a path exists."""
        return os.path.exists(path)

    def is_file(self, path: str) -> bool:
        """Check if path is a file."""
        return os.path.isfile(path)

    def is_directory(self, path: str) -> bool:
        """Check if path is a directory."""
        return os.path.isdir(path)

    def list_files(self, directory: str, recursive: bool = False) -> List[str]:
        """List all files in a directory."""
        files = []
        try:
            if recursive:
                for root, _, filenames in os.walk(directory):
                    for filename in filenames:
                        path = os.path.join(root, filename)
                        # Normalize path to use forward slashes
                        path = path.replace(os.sep, "/")
                        files.append(path)
            else:
                for entry in os.listdir(directory):
                    path = os.path.join(directory, entry)
                    if os.path.isfile(path):
                        # Normalize path to use forward slashes
                        path = path.replace(os.sep, "/")
                        files.append(path)
        except OSError as e:
            logger.error(f"Error listing files in {directory}: {str(e)}")
        return sorted(files)  # Sort for consistent ordering

    def get_file_size(self, file_path: str) -> int:
        """Get the size of a file in bytes."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        return os.path.getsize(file_path)


class MockFileSystemService(FileSystemService):
    """Mock file system service for testing."""

    def __init__(self) -> None:
        """Initialize mock file system."""
        self._files: Dict[str, Union[str, bytes]] = {}
        self._permissions: Dict[str, int] = {}
        self._directories: Dict[str, int] = {}

    def create_directory(self, path: str, permissions: Optional[int] = None) -> bool:
        """Create a directory in the mock file system."""
        path = os.path.normpath(path)
        self._directories[path] = permissions or 0o777
        return True

    def write_file(
        self, path: str, content: Union[str, bytes], permissions: Optional[int] = None
    ) -> bool:
        """Write content to a file in the mock file system."""
        path = os.path.normpath(path)
        self._files[path] = content
        self._permissions[path] = permissions or 0o666
        return True

    def read_file(self, path: str) -> Union[str, bytes]:
        """Read content from a file in the mock file system."""
        path = os.path.normpath(path)
        if path not in self._files:
            raise FileNotFoundError(f"File not found: {path}")
        return self._files[path]

    def read_file_chunk(self, path: str, offset: int, size: int) -> bytes:
        """Read a chunk of data from a file in the mock file system."""
        path = os.path.normpath(path)
        if path not in self._files:
            raise FileNotFoundError(f"File not found: {path}")

        if offset < 0:
            raise ValueError("Offset must be non-negative")

        if size <= 0:
            raise ValueError("Size must be positive")

        content = self._files[path]
        if isinstance(content, str):
            content = content.encode("utf-8")

        return content[offset : offset + size]

    def check_permissions(self, path: str) -> bool:
        """Check if a path has read permissions."""
        path = os.path.normpath(path)
        if path in self._files:
            return bool(self._permissions.get(path, 0o666) & 0o444)
        if path in self._directories:
            return bool(self._directories.get(path, 0o777) & 0o444)
        return False

    def delete(self, path: str) -> bool:
        """Delete a file or directory."""
        path = os.path.normpath(path)
        if path in self._files:
            del self._files[path]
            del self._permissions[path]
            return True
        if path in self._directories:
            del self._directories[path]
            return True
        return False

    def exists(self, path: str) -> bool:
        """Check if a path exists."""
        path = os.path.normpath(path)
        return path in self._files or path in self._directories

    def is_file(self, path: str) -> bool:
        """Check if a path is a file."""
        path = os.path.normpath(path)
        return path in self._files

    def is_directory(self, path: str) -> bool:
        """Check if a path is a directory."""
        path = os.path.normpath(path)
        return path in self._directories

    def list_files(self, directory: str, recursive: bool = False) -> List[str]:
        """List files in a directory."""
        directory = os.path.normpath(directory)
        files = []
        for path in self._files.keys():
            if recursive:
                if path.startswith(directory):
                    # Normalize path to use forward slashes
                    normalized_path = path.replace("\\", "/")
                    files.append(normalized_path)
            else:
                if os.path.dirname(path) == directory:
                    # Normalize path to use forward slashes
                    normalized_path = path.replace("\\", "/")
                    files.append(normalized_path)
        return sorted(files)

    def get_file_size(self, path: str) -> int:
        """Get the size of a file in bytes."""
        path = os.path.normpath(path)
        if path not in self._files:
            raise FileNotFoundError(f"File not found: {path}")
        content = self._files[path]
        if isinstance(content, str):
            return len(content.encode("utf-8"))
        return len(content)

    def set_permission(self, path: str, permissions: int) -> bool:
        """Set permissions for a path."""
        path = os.path.normpath(path)
        if path in self._files:
            self._permissions[path] = permissions
            return True
        if path in self._directories:
            self._directories[path] = permissions
            return True
        return False
