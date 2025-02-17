import os
import tempfile
import shutil
import json
from pathlib import Path
import pytest
from rich.console import Console
import sys
from unittest.mock import patch

from code_tokenizer.converter import (
    process_codebase_to_docs,
    count_tokens,
    detect_language,
    read_file_content,
    should_ignore_path,
)
from code_tokenizer.cli import main

# Test Fixtures
# ============================================================================

@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def sample_codebase(temp_dir):
    """Create a sample codebase structure for testing.
    
    Creates:
    - Python file (main.py)
    - JSON file (config.json)
    - .gitignore
    - Ignored directory with content
    """
    # Create Python file
    python_file = Path(temp_dir) / "main.py"
    python_file.write_text("""
def hello_world():
    print("Hello, World!")
    
if __name__ == "__main__":
    hello_world()
""")
    
    # Create JSON file
    json_file = Path(temp_dir) / "config.json"
    json_file.write_text("""
{
    "name": "test",
    "version": "1.0.0"
}
""")
    
    # Create .gitignore
    gitignore = Path(temp_dir) / ".gitignore"
    gitignore.write_text("""
__pycache__/
*.pyc
temp/
""")
    
    # Create ignored directory and file
    temp_path = Path(temp_dir) / "temp"
    temp_path.mkdir()
    (temp_path / "ignored.txt").write_text("This should be ignored")
    
    return temp_dir

@pytest.fixture
def console():
    """Create a console instance that suppresses output during tests."""
    return Console(file=open(os.devnull, 'w'))

# Core Functionality Tests
# ============================================================================

class TestCoreFeatures:
    """Test core features of the code tokenizer."""
    
    def test_token_counting(self):
        """Test token counting with various inputs and models."""
        # Basic counting
        assert count_tokens("Hello, World!") > 0
        assert count_tokens("") == 0
        
        # Test different models
        text = "This is a test sentence."
        tokens_claude = count_tokens(text, model="claude-3-sonnet")
        tokens_gpt = count_tokens(text, model="gpt-4o")
        assert tokens_claude > 0
        assert tokens_gpt > 0
        
        # Edge cases
        assert count_tokens(" ") > 0  # Just whitespace
        assert count_tokens("\n\n\n") > 0  # Just newlines
        assert count_tokens("a" * 1000) > 0  # Long repetitive text
    
    def test_language_detection(self):
        """Test language detection for different file types."""
        assert detect_language("test.py") == "Python"
        assert detect_language("test.json") == "JSON"
        assert detect_language("test.md") == "Markdown"
        assert detect_language("test.unknown") == "text"
    
    def test_gitignore_handling(self):
        """Test .gitignore pattern matching."""
        patterns = ["*.pyc", "__pycache__/", "temp/"]
        from pathspec import PathSpec
        git_spec = PathSpec.from_lines("gitwildmatch", patterns)
        
        # Should ignore
        assert should_ignore_path("file.pyc", git_spec, [])[0]
        assert should_ignore_path("__pycache__/cache.txt", git_spec, [])[0]
        assert should_ignore_path("temp/test.txt", git_spec, [])[0]
        
        # Should not ignore
        assert not should_ignore_path("main.py", git_spec, [])[0]
        assert not should_ignore_path("src/util.js", git_spec, [])[0]

    def test_token_counting_edge_cases(self):
        """Test token counting with edge cases and special characters."""
        # Unicode characters
        assert count_tokens("Hello 世界") > 0
        assert count_tokens("🌟 Star") > 0
        
        # Code snippets
        assert count_tokens("def test(): pass") > 0
        assert count_tokens("SELECT * FROM table") > 0
        
        # Mixed content
        mixed_text = "print('Hello'); # Comment\n" * 10
        assert count_tokens(mixed_text) > 0
        
        # Invalid model fallback
        assert count_tokens("test", model="invalid-model") > 0
    
    def test_language_detection_edge_cases(self):
        """Test language detection with various file types and edge cases."""
        # Common web files
        assert detect_language("style.css") == "CSS"
        assert detect_language("script.js") == "JavaScript"
        assert detect_language("index.html") == "HTML"
        
        # Special cases
        assert detect_language("Dockerfile") == "Docker"
        assert detect_language(".env") == "Dotenv"
        assert detect_language("requirements.txt") == "Text"
        
        # Case sensitivity
        assert detect_language("Test.PY") == "Python"
        assert detect_language("test.JS") == "JavaScript"
        
        # Files without extensions
        assert detect_language("README") == "text"
        assert detect_language("LICENSE") == "text"
    
    def test_file_reading_edge_cases(self, temp_dir, console):
        """Test file reading with various edge cases and encodings."""
        # Test file with BOM
        bom_file = Path(temp_dir) / "bom.txt"
        bom_file.write_bytes(b'\xef\xbb\xbfHello, BOM!')
        content, encoding, success = read_file_content(str(bom_file), console)
        assert success
        assert "BOM" in content
        
        # Test file with mixed line endings
        mixed_file = Path(temp_dir) / "mixed.txt"
        mixed_file.write_bytes(b'line1\r\nline2\rline3\nline4')
        content, encoding, success = read_file_content(str(mixed_file), console)
        assert success
        assert content.count('\n') == 3
        
        # Test file with control characters
        control_file = Path(temp_dir) / "control.txt"
        control_file.write_bytes(b'Hello\x00World\x1FTest')
        content, encoding, success = read_file_content(str(control_file), console)
        assert success
        assert '\x00' not in content
        assert '\x1F' not in content
    
    def test_gitignore_pattern_edge_cases(self):
        """Test gitignore pattern matching with complex patterns."""
        patterns = [
            "*.{js,py,txt}",  # Multiple extensions
            "!important.js",   # Negation
            "temp/",          # Directory
            "**/node_modules", # Recursive
            "*.log",          # Simple pattern
        ]
        from pathspec import PathSpec
        git_spec = PathSpec.from_lines("gitwildmatch", patterns)
        
        # Test multiple extensions
        assert should_ignore_path("test.js", git_spec, [])[0]
        assert should_ignore_path("test.py", git_spec, [])[0]
        assert should_ignore_path("test.txt", git_spec, [])[0]
        assert not should_ignore_path("test.css", git_spec, [])[0]
        
        # Test negation
        assert not should_ignore_path("important.js", git_spec, [])[0]
        
        # Test directory patterns
        assert should_ignore_path("temp/file.txt", git_spec, [])[0]
        assert should_ignore_path("src/node_modules/file.js", git_spec, [])[0]
        
        # Test with custom ignore files
        custom_ignores = ["*.tmp", "backup/"]
        assert should_ignore_path("test.tmp", git_spec, custom_ignores)[0]
        assert should_ignore_path("backup/data.txt", git_spec, custom_ignores)[0]
    
    def test_error_handling(self, temp_dir):
        """Test error handling in various scenarios."""
        output_file = Path(temp_dir) / "output.md"
        
        # Test with non-existent directory
        with pytest.raises(ValueError):
            process_codebase_to_docs(
                "non_existent_dir",
                str(output_file),
                model="claude-3-sonnet"
            )
        
        # Test with invalid model
        with pytest.raises(ValueError):
            process_codebase_to_docs(
                temp_dir,
                str(output_file),
                model="invalid-model"
            )
        
        # Test with invalid output format
        with pytest.raises(ValueError):
            process_codebase_to_docs(
                temp_dir,
                str(output_file),
                output_format="invalid"
            )
        
        # Test with unreadable directory
        unreadable_dir = Path(temp_dir) / "unreadable"
        unreadable_dir.mkdir()
        if os.name != 'nt':  # Skip on Windows
            os.chmod(unreadable_dir, 0o000)
            with pytest.raises(PermissionError):
                process_codebase_to_docs(
                    str(unreadable_dir),
                    str(output_file),
                    model="claude-3-sonnet"
                )

# File Processing Tests
# ============================================================================

class TestFileProcessing:
    """Test file reading and processing capabilities."""
    
    def test_file_reading(self, temp_dir, console):
        """Test file content reading with different encodings."""
        # Test UTF-8
        file_path = Path(temp_dir) / "utf8.txt"
        file_path.write_text("Hello, World!", encoding="utf-8")
        content, encoding, success = read_file_content(str(file_path), console)
        assert success
        assert encoding == "utf-8"
        assert content.strip() == "Hello, World!"
        
        # Test empty file
        empty_file = Path(temp_dir) / "empty.txt"
        empty_file.touch()
        content, encoding, success = read_file_content(str(empty_file), console)
        assert not success
    
    def test_binary_file_handling(self, temp_dir, console):
        """Test handling of binary files."""
        binary_file = Path(temp_dir) / "binary.bin"
        with open(binary_file, 'wb') as f:
            f.write(b'\x00\x01\x02\x03')
        
        content, encoding, success = read_file_content(str(binary_file), console)
        assert not success
        assert encoding == "binary"
        assert content == ""
    
    def test_problematic_files(self, temp_dir, console):
        """Test handling of problematic files."""
        # Test non-existent file
        non_existent = Path(temp_dir) / "non_existent.txt"
        content, encoding, success = read_file_content(str(non_existent), console)
        assert not success
        assert encoding == "unknown"
        
        # Test empty file
        empty_file = Path(temp_dir) / "empty.txt"
        empty_file.touch()
        content, encoding, success = read_file_content(str(empty_file), console)
        assert not success

# Codebase Conversion Tests
# ============================================================================

class TestCodebaseConversion:
    """Test full codebase conversion functionality."""
    
    def test_basic_conversion(self, temp_dir, sample_codebase):
        """Test basic codebase conversion with default settings."""
        output_file = Path(temp_dir) / "output.md"
        stats = process_codebase_to_docs(
            sample_codebase,
            str(output_file),
            model="claude-3-sonnet",
            include_metadata=True
        )
        
        assert stats["total_files"] == 2  # main.py and config.json
        assert stats["total_tokens"] > 0
        assert "Python" in stats["languages"]
        assert "JSON" in stats["languages"]
        assert output_file.exists()
    
    def test_output_formats(self, temp_dir, sample_codebase):
        """Test different output formats (markdown and JSON)."""
        # Test markdown
        md_file = Path(temp_dir) / "output.md"
        process_codebase_to_docs(
            sample_codebase,
            str(md_file),
            output_format="markdown"
        )
        assert md_file.exists()
        assert "```python" in md_file.read_text()
        
        # Test JSON
        json_file = Path(temp_dir) / "output.json"
        process_codebase_to_docs(
            sample_codebase,
            str(json_file),
            output_format="json"
        )
        assert json_file.exists()
        content = json_file.read_text()
        assert '"language": "Python"' in content
        # Validate JSON structure
        data = json.loads(content)
        assert "project_name" in data
        assert "files" in data
        assert len(data["files"]) > 0
    
    def test_directory_ignore_behavior(self, temp_dir):
        """Test that ignored directories are skipped entirely."""
        # Create a mock node_modules structure
        node_modules = Path(temp_dir) / "node_modules"
        node_modules.mkdir()
        
        package_dir = node_modules / "some-package"
        package_dir.mkdir()
        (package_dir / "index.js").write_text("console.log('test');")
        (package_dir / "package.json").write_text('{"name": "test"}')
        
        # Create a regular source file
        src_dir = Path(temp_dir) / "src"
        src_dir.mkdir()
        (src_dir / "main.js").write_text("import test from 'test';")
        
        output_file = Path(temp_dir) / "output.md"
        console = Console(record=True)
        
        stats = process_codebase_to_docs(
            str(temp_dir),
            str(output_file),
            model="claude-3-sonnet"
        )
        
        # Verify node_modules was skipped
        console_output = console.export_text()
        assert "node_modules" not in console_output or "Skipping directory: node_modules" in console_output
        assert stats["total_files"] == 1
        assert "JavaScript" in stats["languages"]
        assert stats["languages"]["JavaScript"] == 1

# CLI Tests
# ============================================================================

class TestCLI:
    """Test command-line interface functionality."""
    
    def test_basic_cli(self, temp_dir, sample_codebase):
        """Test basic CLI functionality."""
        output_dir = Path(temp_dir) / "output"
        output_dir.mkdir()
        
        with patch.object(sys, 'argv', [
            'code-tokenizer',
            '-d', str(sample_codebase),
            '-o', str(output_dir),
            '--model', 'claude-3-sonnet'
        ]):
            main()
        
        base_name = Path(sample_codebase).name
        assert (output_dir / f"{base_name}_docs.markdown").exists()
        assert (output_dir / f"{base_name}_analysis.md").exists()
    
    def test_cli_with_options(self, temp_dir, sample_codebase):
        """Test CLI with various options."""
        output_dir = Path(temp_dir) / "output"
        output_dir.mkdir()
        
        # Test with JSON format
        with patch.object(sys, 'argv', [
            'code-tokenizer',
            '-d', str(sample_codebase),
            '-o', str(output_dir),
            '--format', 'json',
            '--model', 'claude-3-sonnet'
        ]):
            main()
        
        base_name = Path(sample_codebase).name
        json_file = output_dir / f"{base_name}_docs.json"
        assert json_file.exists()
        
        # Verify JSON content
        with open(json_file) as f:
            data = json.load(f)
            assert "project_name" in data
            assert "files" in data
            assert len(data["files"]) > 0
    
    def test_cli_errors(self, temp_dir):
        """Test CLI error handling."""
        output_dir = Path(temp_dir) / "output"
        output_dir.mkdir()
        
        # Test invalid model
        with pytest.raises(SystemExit) as exc_info:
            with patch.object(sys, 'argv', [
                'code-tokenizer',
                '-d', str(temp_dir),
                '-o', str(output_dir),
                '--model', 'invalid-model'
            ]):
                main()
        assert exc_info.value.code == 2  # argparse exit code for argument errors 