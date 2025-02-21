"""File system service for handling file operations."""

import logging
import os
import shutil
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union, Set
from pathlib import Path

# Configure logging
logger = logging.getLogger(__name__)


class FileSystemService(ABC):
    """Base class for file system operations."""

    def normalize_path(self, path: str) -> str:
        """Normalize a path to use forward slashes."""
        return path.replace(os.sep, '/')

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

    def get_files_in_directory(self, directory: str) -> List[str]:
        """Get all files in a directory recursively."""
        if not directory:
            return []
            
        directory = self.normalize_path(directory)
        if not directory.endswith('/'):
            directory += '/'
            
        files = []
        
        for path in self._files.keys():
            path = self.normalize_path(path)
            # Check if this path is within the target directory
            if path.startswith(directory):
                try:
                    rel_path = os.path.relpath(path, directory)
                    # Normalize to forward slashes for consistency
                    rel_path = rel_path.replace(os.sep, '/')
                    files.append(rel_path)
                except ValueError:
                    # Path is not relative to directory
                    continue
                
        return sorted(files)


class RealFileSystemService(FileSystemService):
    """Real file system implementation."""

    def __init__(self):
        """Initialize the filesystem service."""
        self.gitignore = None
        self.base_dir = None

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
        return sorted(files)

    def get_file_size(self, path: str) -> int:
        """Get the size of a file in bytes."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        return os.path.getsize(path)

    def get_files_in_directory(self, directory: str) -> List[str]:
        """Get all files in a directory recursively."""
        if not directory:
            return []

        directory = self.normalize_path(directory)
        if not directory.endswith('/'):
            directory += '/'

        files = []
        try:
            for root, _, filenames in os.walk(directory.rstrip('/')):
                for filename in filenames:
                    full_path = os.path.join(root, filename)
                    rel_path = os.path.relpath(full_path, directory.rstrip('/'))
                    # Normalize to forward slashes for consistency
                    rel_path = rel_path.replace(os.sep, '/')
                    files.append(rel_path)
        except Exception as e:
            logger.error(f"Error walking directory {directory}: {str(e)}")
            return []

        return sorted(files)


class MockFileSystemService(FileSystemService):
    """Mock file system service for testing."""

    def __init__(self):
        """Initialize mock file system service."""
        self._files: Dict[str, str] = {}
        self._directories: Set[str] = set()
        self._permissions: Dict[str, int] = {}  # Changed to int for octal permissions

    def normalize_path(self, path: str) -> str:
        """Normalize a path to use forward slashes."""
        # Convert backslashes to forward slashes and remove any trailing slashes
        normalized = path.replace('\\', '/').rstrip('/')
        # Handle absolute Windows paths
        if normalized.startswith('C:/'):
            normalized = normalized[2:]  # Remove 'C:'
        return normalized

    def write_file(self, path: str, content: str) -> None:
        """Write content to a file.

        Args:
            path (str): Path to file
            content (str): Content to write
        """
        normalized_path = self.normalize_path(path)
        # Ensure the directory exists
        dir_path = os.path.dirname(normalized_path)
        if dir_path:
            self.create_directory(dir_path)
        self._files[normalized_path] = content
        self._permissions[normalized_path] = 0o666  # Default file permissions

    def create_directory(self, path: str, permissions: Optional[int] = None) -> None:
        """Create a directory.

        Args:
            path (str): Path to directory
            permissions (Optional[int], optional): Directory permissions. Defaults to None.
        """
        normalized_path = self.normalize_path(path)
        if normalized_path:
            self._directories.add(normalized_path)
            self._permissions[normalized_path] = permissions or 0o777  # Default directory permissions
            # Create parent directories
            parent = os.path.dirname(normalized_path)
            if parent:
                self.create_directory(parent)

    def exists(self, path: str) -> bool:
        """Check if a path exists.

        Args:
            path (str): Path to check

        Returns:
            bool: True if path exists, False otherwise
        """
        normalized_path = self.normalize_path(path)
        return normalized_path in self._files or normalized_path in self._directories

    def is_file(self, path: str) -> bool:
        """Check if a path is a file.

        Args:
            path (str): Path to check

        Returns:
            bool: True if path is a file, False otherwise
        """
        normalized_path = self.normalize_path(path)
        return normalized_path in self._files

    def is_directory(self, path: str) -> bool:
        """Check if a path is a directory.

        Args:
            path (str): Path to check

        Returns:
            bool: True if path is a directory, False otherwise
        """
        normalized_path = self.normalize_path(path)
        return normalized_path in self._directories

    def get_files_in_directory(self, directory: str) -> List[str]:
        """Get all files in a directory.

        Args:
            directory (str): Directory to get files from

        Returns:
            List[str]: List of file paths
        """
        normalized_dir = self.normalize_path(directory)
        if not normalized_dir.endswith('/'):
            normalized_dir += '/'
        
        files = []
        for file_path in self._files.keys():
            if file_path.startswith(normalized_dir):
                files.append(file_path)
        return files

    def list_files(self, directory: str, recursive: bool = False) -> List[str]:
        """List files in a directory.

        Args:
            directory (str): Directory to list files from
            recursive (bool, optional): Whether to list files recursively. Defaults to False.

        Returns:
            List[str]: List of file paths
        """
        normalized_dir = self.normalize_path(directory)
        if not normalized_dir.endswith('/'):
            normalized_dir += '/'

        files = []
        for file_path in self._files.keys():
            normalized_path = self.normalize_path(file_path)
            if recursive:
                if normalized_path.startswith(normalized_dir):
                    files.append(normalized_path)
            else:
                parent = os.path.dirname(normalized_path)
                if parent == normalized_dir.rstrip('/'):
                    files.append(normalized_path)
        return sorted(files)

    def read_file(self, path: str) -> str:
        """Read content from a file.

        Args:
            path (str): Path to file

        Returns:
            str: File content

        Raises:
            FileNotFoundError: If file does not exist
        """
        normalized_path = self.normalize_path(path)
        if normalized_path not in self._files:
            raise FileNotFoundError(f"File not found: {path}")
        return self._files[normalized_path]

    def read_file_chunk(self, path: str, start: int = 0, size: int = -1) -> str:
        """Read a chunk of content from a file.

        Args:
            path (str): Path to file
            start (int, optional): Start position. Defaults to 0.
            size (int, optional): Number of bytes to read. Defaults to -1 (read all).

        Returns:
            str: File content chunk

        Raises:
            FileNotFoundError: If file does not exist
        """
        content = self.read_file(path)
        if size == -1:
            return content[start:]
        return content[start:start + size]

    def get_file_size(self, path: str) -> int:
        """Get the size of a file in bytes.

        Args:
            path (str): Path to file

        Returns:
            int: File size in bytes

        Raises:
            FileNotFoundError: If file does not exist
        """
        content = self.read_file(path)
        return len(content.encode('utf-8'))

    def check_permissions(self, path: str) -> bool:
        """Check if a path has read permissions.

        Args:
            path (str): Path to check

        Returns:
            bool: True if path has read permissions, False otherwise
        """
        normalized_path = self.normalize_path(path)
        permissions = self._permissions.get(normalized_path, 0)
        return bool(permissions & 0o444)  # Check read permissions

    def set_permission(self, path: str, permissions: int) -> None:
        """Set permissions for a path.

        Args:
            path (str): Path to set permissions for
            permissions (int): Permissions to set
        """
        normalized_path = self.normalize_path(path)
        if normalized_path in self._files or normalized_path in self._directories:
            self._permissions[normalized_path] = permissions

    def add_file(self, path: str, content: str) -> None:
        """Add a file to the mock filesystem.

        This is a convenience method for tests that combines create_directory and write_file.

        Args:
            path (str): Path to the file to add
            content (str): Content to write to the file
        """
        normalized_path = self.normalize_path(path)
        dir_path = os.path.dirname(normalized_path)
        if dir_path:
            self.create_directory(dir_path)
        self.write_file(normalized_path, content)

    def delete(self, path: str) -> None:
        """Delete a file or directory.

        Args:
            path (str): Path to delete
        """
        normalized_path = self.normalize_path(path)
        if normalized_path in self._files:
            del self._files[normalized_path]
            del self._permissions[normalized_path]
        elif normalized_path in self._directories:
            self._directories.remove(normalized_path)
            # Remove all files and subdirectories under this directory
            for file_path in list(self._files.keys()):
                if file_path.startswith(normalized_path + '/'):
                    del self._files[file_path]
                    del self._permissions[file_path]
            for dir_path in list(self._directories):
                if dir_path.startswith(normalized_path + '/'):
                    self._directories.remove(dir_path)
