"""Tests for gitignore functionality."""

import os
from pathlib import Path

import pytest

from code_tokenizer.services.tokenizer_service import TokenizerService


@pytest.fixture
def test_project(tmp_path):
    """Create a test project with some files and a .gitignore."""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()

    # Create source files
    (project_dir / "src").mkdir()
    (project_dir / "src/main.py").write_text("print('Hello, World!')")
    (project_dir / "src/utils.py").write_text("def helper(): pass")

    # Create test files
    (project_dir / "tests").mkdir()
    (project_dir / "tests/test_main.py").write_text("def test_main(): assert True")

    # Create project config files
    (project_dir / "package.json").write_text('{"name": "root-project"}')
    (project_dir / "setup.py").write_text("from setuptools import setup")

    # Create files that should be ignored
    node_modules = project_dir / "node_modules"
    node_modules.mkdir()

    # Create node_modules packages
    (node_modules / "react").mkdir()
    (node_modules / "react/package.json").write_text('{"name": "react"}')

    (node_modules / "lodash").mkdir()
    (node_modules / "lodash/package.json").write_text('{"name": "lodash"}')

    (node_modules / "typescript/lib").mkdir(parents=True)
    (node_modules / "typescript/lib/index.js").write_text("/* TypeScript */")

    # Create __pycache__ directory with binary files
    pycache = project_dir / "src/__pycache__"
    pycache.mkdir(parents=True)
    with open(pycache / "main.cpython-39.pyc", "wb") as f:
        f.write(b"\x00\x01\x02\x03")  # Write some binary data

    # Create build directory with binary files
    build = project_dir / "build"
    build.mkdir()
    with open(build / "temp.o", "wb") as f:
        f.write(b"\x00\x01\x02\x03")  # Write some binary data

    # Create a .gitignore file with common patterns
    gitignore_content = """
# Dependencies
node_modules/
__pycache__/

# Build outputs
build/
dist/
*.pyc
*.o
    """
    (project_dir / ".gitignore").write_text(gitignore_content)

    return project_dir


def test_bypass_gitignore(test_project, tmp_path):
    """Test that --bypass-gitignore processes all files."""
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    # First, test with normal gitignore behavior
    config_with_gitignore = {
        "base_dir": str(test_project),
        "output_dir": str(output_dir),
        "bypass_gitignore": False,
        "model_name": "gpt-4o",
        "max_tokens": 200000,
        "output_format": "markdown",
        "include_metadata": True,
    }

    tokenizer = TokenizerService.from_config(config_with_gitignore)
    stats_with_gitignore = tokenizer.process_directory(str(test_project))

    print("\nFiles processed in normal mode:")
    for file in sorted(stats_with_gitignore["successful_files"]):
        print(f"  - {file}")

    # Should only process source files and project config files
    # Files in node_modules/, __pycache__/, and build/ should be ignored
    expected_files = {
        "src/main.py",
        "src/utils.py",
        "tests/test_main.py",
        "package.json",
        "setup.py",
        ".gitignore",
    }
    processed_files = set(stats_with_gitignore["successful_files"])
    assert (
        processed_files == expected_files
    ), f"Expected {expected_files}, but got {processed_files}"

    # Now test with bypass_gitignore
    config_bypass = {
        "base_dir": str(test_project),
        "output_dir": str(output_dir),
        "bypass_gitignore": True,
        "model_name": "gpt-4o",
        "max_tokens": 200000,
        "output_format": "markdown",
        "include_metadata": True,
        "file_extensions": None,  # When bypassing gitignore, we want to process all files
        "skip_extensions": None,  # When bypassing gitignore, we want to process all files
    }

    tokenizer = TokenizerService.from_config(config_bypass)
    stats_bypass = tokenizer.process_directory(str(test_project))

    print("\nFiles processed in bypass mode:")
    for file in sorted(stats_bypass["successful_files"]):
        print(f"  - {file}")

    # Should process all files, including ignored ones
    assert (
        stats_bypass["stats"]["files_processed"] > stats_with_gitignore["stats"]["files_processed"]
    )
    assert len(stats_bypass["successful_files"]) > len(stats_with_gitignore["successful_files"])

    # Verify specific patterns
    processed_paths = {
        os.path.relpath(f, str(test_project)).replace(os.sep, "/")
        for f in stats_bypass["successful_files"]
    }
    assert any("node_modules" in p for p in processed_paths), "Should include node_modules files"
    assert any("__pycache__" in p for p in processed_paths), "Should include __pycache__ files"
    assert any(p.endswith(".pyc") for p in processed_paths), "Should include .pyc files"
    assert any(p.endswith(".o") for p in processed_paths), "Should include build artifacts"
