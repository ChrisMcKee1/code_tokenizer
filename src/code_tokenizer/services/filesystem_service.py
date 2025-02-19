"""File system service for handling file operations."""

import os
import shutil
import sys
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union


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
            file_path (str): Path to the file

        Returns:
            int: Size of the file in bytes
        """
        pass


class RealFileSystemService(FileSystemService):
    """Real file system implementation."""

    def create_directory(self, path: str, permissions: Optional[int] = None) -> bool:
        try:
            os.makedirs(path, exist_ok=True)
            if permissions is not None:
                try:
                    os.chmod(path, permissions)
                except OSError:
                    # Continue even if chmod fails
                    pass
            return True
        except OSError:
            return False

    def write_file(
        self, path: str, content: Union[str, bytes], permissions: Optional[int] = None
    ) -> bool:
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
                    # Continue even if chmod fails
                    pass
            return True
        except OSError:
            return False

    def read_file(self, path: str) -> Union[str, bytes]:
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")

        try:
            # Try reading as text first
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except UnicodeDecodeError:
            # If that fails, read as binary
            with open(path, "rb") as f:
                return f.read()

    def check_permissions(self, path: str) -> bool:
        if not os.path.exists(path):
            # Check parent directory for new files/dirs
            path = os.path.dirname(path)
            if not path or not os.path.exists(path):
                return False
        return os.access(path, os.R_OK | os.W_OK)

    def delete(self, path: str) -> bool:
        try:
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
            return True
        except OSError:
            return False

    def exists(self, path: str) -> bool:
        return os.path.exists(path)

    def is_file(self, path: str) -> bool:
        return os.path.isfile(path)

    def is_directory(self, path: str) -> bool:
        return os.path.isdir(path)

    def list_files(self, directory: str, recursive: bool = False) -> List[str]:
        """List all files in a directory.

        Args:
            directory: Directory to list files from
            recursive: Whether to list files recursively

        Returns:
            List[str]: List of file paths
        """
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
            print(f"Error listing files in {directory}: {str(e)}", file=sys.stderr)
        return sorted(files)  # Sort for consistent ordering

    def get_file_size(self, file_path: str) -> int:
        """Get the size of a file in bytes.

        Args:
            file_path (str): Path to the file

        Returns:
            int: Size of the file in bytes
        """
        return os.path.getsize(file_path)


class MockFileSystemService(FileSystemService):
    """Mock file system service for testing."""

    def __init__(self) -> None:
        """Initialize mock file system."""
        self._files: Dict[str, Union[str, bytes]] = {}
        self._permissions: Dict[str, int] = {}
        self._directories: Dict[str, int] = {}

    def create_directory(self, path: str, permissions: Optional[int] = None) -> bool:
        """Create a directory in the mock file system.

        Args:
            path: Directory path to create
            permissions: Optional Unix-style permissions (e.g. 0o777)

        Returns:
            bool: True if successful
        """
        path = os.path.normpath(path)
        self._directories[path] = permissions or 0o777
        return True

    def write_file(
        self, path: str, content: Union[str, bytes], permissions: Optional[int] = None
    ) -> bool:
        """Write content to a file in the mock file system.

        Args:
            path: File path to write to
            content: Content to write (string or bytes)
            permissions: Optional Unix-style permissions (e.g. 0o666)

        Returns:
            bool: True if successful
        """
        path = os.path.normpath(path)
        self._files[path] = content
        self._permissions[path] = permissions or 0o666
        return True

    def read_file(self, path: str) -> Union[str, bytes]:
        """Read content from a file in the mock file system.

        Args:
            path: File path to read from

        Returns:
            Union[str, bytes]: File content
        """
        path = os.path.normpath(path)
        if path not in self._files:
            raise FileNotFoundError(f"File not found: {path}")
        return self._files[path]

    def exists(self, path: str) -> bool:
        """Check if a path exists in the mock file system.

        Args:
            path: Path to check

        Returns:
            bool: True if path exists
        """
        path = os.path.normpath(path)
        return path in self._files or path in self._directories

    def is_file(self, path: str) -> bool:
        """Check if a path is a file in the mock file system.

        Args:
            path: Path to check

        Returns:
            bool: True if path is a file
        """
        path = os.path.normpath(path)
        return path in self._files

    def is_directory(self, path: str) -> bool:
        """Check if a path is a directory in the mock file system.

        Args:
            path: Path to check

        Returns:
            bool: True if path is a directory
        """
        path = os.path.normpath(path)
        return path in self._directories

    def get_file_size(self, path: str) -> int:
        """Get the size of a file in bytes.

        Args:
            path: Path to the file

        Returns:
            int: Size of the file in bytes
        """
        path = os.path.normpath(path)
        if path not in self._files:
            raise FileNotFoundError(f"File not found: {path}")
        content = self._files[path]
        if isinstance(content, str):
            return len(content.encode("utf-8"))
        return len(content)

    def list_files(self, directory: str, recursive: bool = False) -> List[str]:
        """List files in a directory.

        Args:
            directory: Directory to list files from
            recursive: Whether to list files recursively

        Returns:
            List[str]: List of file paths
        """
        directory = os.path.normpath(directory)
        files = []
        for path in self._files.keys():
            if recursive:
                if path.startswith(directory):
                    files.append(path)
            else:
                if os.path.dirname(path) == directory:
                    files.append(path)
        return sorted(files)

    def check_permissions(self, path: str) -> bool:
        """Check if a path has read permissions.

        Args:
            path: Path to check

        Returns:
            bool: True if path has read permissions
        """
        path = os.path.normpath(path)
        if path in self._files:
            return bool(self._permissions.get(path, 0o666) & 0o444)
        if path in self._directories:
            return bool(self._directories.get(path, 0o777) & 0o444)
        return False

    def set_permission(self, path: str, permissions: int) -> bool:
        """Set permissions for a path.

        Args:
            path: Path to set permissions for
            permissions: Unix-style permissions (e.g. 0o666)

        Returns:
            bool: True if successful
        """
        path = os.path.normpath(path)
        if path in self._files:
            self._permissions[path] = permissions
            return True
        if path in self._directories:
            self._directories[path] = permissions
            return True
        return False

    def delete(self, path: str) -> bool:
        """Delete a file or directory.

        Args:
            path: Path to delete

        Returns:
            bool: True if successful
        """
        path = os.path.normpath(path)
        if path in self._files:
            del self._files[path]
            del self._permissions[path]
            return True
        if path in self._directories:
            del self._directories[path]
            return True
        return False
