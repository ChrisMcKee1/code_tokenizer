"""Tests for gitignore functionality."""

import os
import pytest
from pathlib import Path
from code_tokenizer.services.tokenizer_service import TokenizerService

@pytest.fixture
def test_project(tmp_path):
    """Create a test project with some files and a .gitignore."""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()
    
    # Create some Python files
    (project_dir / "main.py").write_text("print('Hello, World!')")
    (project_dir / "test.py").write_text("assert True")
    
    # Create some files that would typically be ignored
    (project_dir / "node_modules").mkdir()
    (project_dir / "node_modules/package.json").write_text('{"name": "test"}')
    (project_dir / "__pycache__").mkdir()
    (project_dir / "__pycache__/main.cpython-39.pyc").write_text("binary data")
    
    # Create a .gitignore file
    gitignore_content = """
node_modules/
__pycache__/
*.pyc
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
        "bypass_gitignore": False
    }
    
    tokenizer = TokenizerService(config_with_gitignore)
    stats_with_gitignore = tokenizer.process_directory()
    
    # Should only process .py files, not node_modules or __pycache__
    assert stats_with_gitignore["files_processed"] == 2
    
    # Now test with bypass_gitignore
    config_bypass = {
        "base_dir": str(test_project),
        "output_dir": str(output_dir),
        "bypass_gitignore": True
    }
    
    tokenizer = TokenizerService(config_bypass)
    stats_bypass = tokenizer.process_directory()
    
    # Should process all files
    assert stats_bypass["files_processed"] > stats_with_gitignore["files_processed"]
    assert any("node_modules" in file["path"] for file in stats_bypass.get("processed_files", []))
    
    # Verify specific files are included when bypassing
    processed_paths = [file["path"] for file in stats_bypass.get("processed_files", [])]
    assert any("package.json" in path for path in processed_paths)
    assert "main.py" in [Path(path).name for path in processed_paths]
    assert "test.py" in [Path(path).name for path in processed_paths] 