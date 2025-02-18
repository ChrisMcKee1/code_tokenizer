"""Utilities for handling file paths and filtering."""

import os
from pathlib import Path
from typing import List, Set, Tuple
import fnmatch

from pathspec import PathSpec


def normalize_path(path: str) -> str:
    """
    Normalize a file path to use forward slashes and relative format.

    Args:
        path: File path to normalize

    Returns:
        str: Normalized path using forward slashes
    """
    # Convert to forward slashes for consistency
    normalized = path.replace(os.sep, "/")

    # Remove leading ./ if present
    if normalized.startswith("./"):
        normalized = normalized[2:]

    return normalized


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


def should_ignore_path(path: str, ignore_patterns: list[str]) -> Tuple[bool, str]:
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
