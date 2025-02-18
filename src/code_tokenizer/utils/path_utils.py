"""Path utilities for handling file paths and ignore patterns."""

import fnmatch
import os
from pathlib import Path
from typing import List, Optional, Set, Tuple

import pathspec
from pathspec import PathSpec


def normalize_path(path: str) -> str:
    """
    Normalize a file path to use forward slashes and relative form.

    Args:
        path: File path to normalize

    Returns:
        str: Normalized path using forward slashes
    """
    return str(Path(path).resolve()).replace(os.sep, "/")


def get_gitignore_patterns(base_dir: str, gitignore_file: Optional[str] = None) -> List[str]:
    """
    Get the list of ignore patterns from a .gitignore file.

    Args:
        base_dir: Base directory containing the .gitignore file
        gitignore_file: Optional path to a specific .gitignore file

    Returns:
        List[str]: List of ignore patterns
    """
    if gitignore_file and os.path.isfile(gitignore_file):
        gitignore_path = gitignore_file
    else:
        gitignore_path = os.path.join(base_dir, ".gitignore")

    if not os.path.isfile(gitignore_path):
        return []

    with open(gitignore_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


def should_ignore_file(file_path: str, base_dir: str, patterns: List[str]) -> bool:
    """
    Check if a file should be ignored based on gitignore patterns.

    Args:
        file_path: Path to the file to check
        base_dir: Base directory for relative paths
        patterns: List of ignore patterns

    Returns:
        bool: True if the file should be ignored
    """
    if not patterns:
        return False

    # Create a PathSpec matcher from the patterns
    spec = pathspec.PathSpec.from_lines("gitwildmatch", patterns)

    # Get the relative path from base_dir
    rel_path = os.path.relpath(file_path, base_dir)

    # Normalize path separators
    rel_path = rel_path.replace(os.sep, "/")

    return spec.match_file(rel_path)


def get_relative_path(file_path: str, base_dir: str) -> str:
    """
    Get the relative path from base_dir to file_path.

    Args:
        file_path: Absolute path to the file
        base_dir: Base directory to make path relative to

    Returns:
        str: Relative path from base_dir to file_path
    """
    try:
        rel_path = os.path.relpath(file_path, base_dir)
        return normalize_path(rel_path)
    except ValueError:
        # If paths are on different drives, return normalized absolute path
        return normalize_path(file_path)


def should_ignore_path(path: str, ignore_patterns: List[str]) -> Tuple[bool, str]:
    """
    Check if a path should be ignored based on gitignore patterns.

    Args:
        path: Path to check
        ignore_patterns: List of gitignore patterns

    Returns:
        Tuple[bool, str]: Whether to ignore the path and the reason
    """
    # Normalize path separators
    path = path.replace("\\", "/")

    # Check each pattern
    for pattern in ignore_patterns:
        pattern = pattern.strip()
        if not pattern or pattern.startswith("#"):
            continue

        # Handle directory patterns
        if pattern.endswith("/"):
            pattern = pattern[:-1]  # Remove trailing slash
            if path.startswith(pattern + "/") or f"/{pattern}/" in path:
                return True, f"Matches directory pattern: {pattern}/"

        # Handle recursive patterns
        elif pattern.startswith("**/"):
            if pattern[3:] in path:
                return True, f"Matches recursive pattern: {pattern}"

        # Handle file patterns with wildcards
        elif "*" in pattern:
            # Convert gitignore pattern to regex pattern
            regex_pattern = pattern.replace(".", r"\.").replace("*", ".*")
            if fnmatch.fnmatch(path, pattern):
                return True, f"Matches pattern: {pattern}"

        # Handle exact matches
        elif pattern == path or path.endswith("/" + pattern):
            return True, f"Matches exact pattern: {pattern}"

    return False, ""
