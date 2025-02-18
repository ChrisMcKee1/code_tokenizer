"""Path utilities for handling file paths and ignore patterns."""

import os
import re
from typing import List, Optional, Tuple


def normalize_path(path: str) -> str:
    """Normalize a path to use forward slashes and handle relative paths correctly.

    Args:
        path: The path to normalize

    Returns:
        str: The normalized path with forward slashes and resolved dot notation
    """
    if not path:
        return ""

    # Convert backslashes to forward slashes
    normalized = path.replace("\\", "/")

    # Handle multiple slashes
    while "//" in normalized:
        normalized = normalized.replace("//", "/")

    # Handle special cases
    if normalized in [".", "./"]:
        return "."
    if normalized in ["..", "../"]:
        return ".."

    # Split path into components
    parts = normalized.split("/")
    result = []

    for part in parts:
        if part == "." or not part:
            continue
        elif part == "..":
            if result and result[-1] != "..":
                result.pop()
            else:
                result.append("..")
        else:
            result.append(part)

    # Reconstruct the path
    normalized = "/".join(result)

    # Preserve root slash if present
    if path.startswith("/"):
        normalized = "/" + normalized

    return normalized


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

    # Get the relative path from base_dir
    rel_path = os.path.relpath(file_path, base_dir)

    # Normalize path separators
    rel_path = rel_path.replace(os.sep, "/")
    path_parts = rel_path.split("/")

    for pattern in patterns:
        pattern = pattern.strip()
        if not pattern or pattern.startswith("#"):
            continue

        # Handle directory patterns (ending with /)
        if pattern.endswith("/"):
            pattern = pattern.rstrip("/")
            # Check if any directory component matches the pattern
            # For a pattern like "node_modules/", this will match any path
            # that has "node_modules" as a directory
            if pattern in path_parts[:-1]:  # Exclude the last part (filename)
                return True
            continue

        # Handle recursive patterns (**)
        if "**" in pattern:
            regex_pattern = pattern.replace("**", ".*").replace("*", "[^/]*")
            if re.search(regex_pattern, rel_path):
                # If pattern ends with a file extension, treat it as a pattern match
                if pattern.endswith(".py") or pattern.endswith(".js") or pattern.endswith(".txt"):
                    return True
                return True

        # Handle file patterns with wildcards
        if "*" in pattern:
            # Convert gitignore pattern to regex
            regex_pattern = pattern.replace(".", r"\.").replace("*", "[^/]*")
            if not pattern.startswith("/"):
                # If pattern doesn't start with /, it can match anywhere in the path
                if any(re.match(f"^{regex_pattern}$", part) for part in path_parts):
                    return True
            else:
                # Pattern starts with /, must match from root
                if re.match(f"^{regex_pattern[1:]}$", rel_path):
                    return True
            continue

        # Handle exact matches
        # For a pattern like "node_modules", this will match any path
        # that has "node_modules" as a component
        if pattern in path_parts:
            return True

    return False


def get_relative_path(path: str, base_path: str) -> str:
    """Get the relative path from base_path to path."""
    if not path or not base_path:
        return path

    # Handle the case where paths are identical
    if os.path.abspath(path) == os.path.abspath(base_path):
        return "."

    # Normalize paths to use forward slashes
    path = normalize_path(path)
    base_path = normalize_path(base_path)

    # If path is already relative to base_path, return it as is
    if path.startswith(base_path):
        rel = path[len(base_path) :].lstrip("/")
        return rel if rel else "."

    # Convert both paths to absolute paths
    try:
        abs_path = os.path.abspath(path)
        abs_base = os.path.abspath(base_path)

        # Get the relative path
        rel_path = os.path.relpath(abs_path, abs_base)

        # Normalize the result
        return normalize_path(rel_path)
    except ValueError:
        # If paths are on different drives, return normalized path
        return normalize_path(path)


def should_ignore_path(path: str, patterns: List[str]) -> Tuple[bool, str]:
    """
    Check if a path should be ignored based on gitignore patterns.

    Args:
        path: The path to check
        patterns: List of gitignore patterns

    Returns:
        Tuple[bool, str]: (should_ignore, reason)
    """
    if not patterns:
        return False, ""

    normalized_path = normalize_path(path)
    path_parts = normalized_path.split("/")

    for pattern in patterns:
        pattern = pattern.strip()
        if not pattern or pattern.startswith("#"):
            continue

        # Handle directory patterns (ending with /)
        if pattern.endswith("/"):
            pattern = pattern.rstrip("/")
            # Check if any directory component matches the pattern
            for part in path_parts[:-1]:  # Exclude the last part (filename)
                if part == pattern:
                    return True, f"Matches directory pattern: {pattern}/"

        # Handle recursive patterns (**)
        elif "**" in pattern:
            regex_pattern = pattern.replace("**", ".*").replace("*", "[^/]*")
            if re.search(regex_pattern, normalized_path):
                # If pattern ends with a file extension, treat it as a pattern match
                if pattern.endswith(".py") or pattern.endswith(".js") or pattern.endswith(".txt"):
                    return True, f"Matches pattern: {pattern}"
                return True, f"Matches recursive pattern: {pattern}"

        # Handle file patterns with wildcards
        elif "*" in pattern:
            # Convert gitignore pattern to regex
            regex_pattern = pattern.replace(".", r"\.").replace("*", "[^/]*")
            if not pattern.startswith("/"):
                # If pattern doesn't start with /, it can match anywhere in the path
                if any(re.match(f"^{regex_pattern}$", part) for part in path_parts):
                    return True, f"Matches pattern: {pattern}"
            else:
                # Pattern starts with /, must match from root
                if re.match(f"^{regex_pattern[1:]}$", normalized_path):
                    return True, f"Matches pattern: {pattern}"

        # Handle exact matches
        else:
            # Check if any path component matches exactly
            if pattern in path_parts:
                return True, f"Matches exact pattern: {pattern}"

    return False, ""


def get_file_paths(
    directory: str,
    file_extensions: Optional[List[str]] = None,
    skip_extensions: Optional[List[str]] = None,
    ignore_patterns: Optional[List[str]] = None,
    bypass_gitignore: bool = False,
) -> List[str]:
    """
    Get all file paths in a directory that match the given criteria.

    Args:
        directory: Directory to search in
        file_extensions: List of file extensions to include (e.g. ['.py', '.js'])
        skip_extensions: List of file extensions to skip
        ignore_patterns: List of gitignore patterns to apply
        bypass_gitignore: Whether to bypass gitignore patterns and skip_extensions

    Returns:
        List[str]: List of file paths
    """
    file_paths = []

    # Normalize the base directory path
    directory = os.path.abspath(directory)

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)

            # If bypassing gitignore, include all files
            if bypass_gitignore:
                # Only filter by file_extensions if specified and not empty
                if file_extensions and len(file_extensions) > 0:
                    if any(file.lower().endswith(ext.lower()) for ext in file_extensions):
                        file_paths.append(file_path)
                else:
                    # If no file_extensions specified, include all files
                    file_paths.append(file_path)
                continue

            # Skip files that match ignore patterns
            if ignore_patterns and should_ignore_file(file_path, directory, ignore_patterns):
                continue

            # Skip files with unwanted extensions
            if skip_extensions and any(
                file.lower().endswith(ext.lower()) for ext in skip_extensions
            ):
                continue

            # Only include files with wanted extensions (if specified)
            if file_extensions and not any(
                file.lower().endswith(ext.lower()) for ext in file_extensions
            ):
                continue

            file_paths.append(file_path)

    return sorted(file_paths)
