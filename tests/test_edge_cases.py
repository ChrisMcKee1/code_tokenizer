"""Edge cases and error handling tests."""

import os
import sys
import pytest
from pathlib import Path
import tempfile
from contextlib import contextmanager

from code_tokenizer.services.tokenizer_service import TokenizerService

@contextmanager
def capture_output():
    """Capture stdout and stderr to a temporary file."""
    temp_file = tempfile.NamedTemporaryFile(mode='w+', delete=False)
    old_stdout, old_stderr = sys.stdout, sys.stderr
    try:
        sys.stdout = sys.stderr = temp_file
        yield temp_file.name
    finally:
        sys.stdout, sys.stderr = old_stdout, old_stderr
        temp_file.close()

class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_empty_directory(self, temp_dir):
        """Test processing an empty directory."""
        config = {
            "base_dir": temp_dir,
            "model_name": "claude-3-sonnet",
            "output_format": "json",  # Use JSON format to avoid rich display
            "disable_progress": True,
            "include_metadata": False  # Minimize output
        }
        tokenizer = TokenizerService(config)
        stats = tokenizer.process_directory()
        
        assert stats["files_processed"] == 0
        assert stats["total_tokens"] == 0
        assert not stats["languages"]
    
    def test_binary_files(self, temp_dir):
        """Test handling of binary files."""
        # Create a binary file
        binary_file = Path(temp_dir) / "test.bin"
        with open(binary_file, "wb") as f:
            f.write(bytes(range(256)))
        
        config = {
            "base_dir": temp_dir,
            "model_name": "claude-3-sonnet",
            "disable_progress": True
        }
        tokenizer = TokenizerService(config)
        result = tokenizer.process_file(str(binary_file))
        
        assert not result["success"]
        assert "binary" in result.get("error", "").lower()
    
    def test_large_file_handling(self, temp_dir):
        """Test handling of large files."""
        # Create a large text file
        large_file = Path(temp_dir) / "large.txt"
        content = "A" * 1000000  # 1MB of text
        large_file.write_text(content)
        
        config = {
            "base_dir": temp_dir,
            "model_name": "claude-3-sonnet",
            "max_tokens_per_file": 1000,
            "disable_progress": True
        }
        tokenizer = TokenizerService(config)
        result = tokenizer.process_file(str(large_file))
        
        assert result["success"]
        assert result["tokens"] <= 1000  # Should be truncated
    
    def test_special_characters(self, temp_dir):
        """Test handling of files with special characters."""
        # Create files with special characters
        files = {
            "unicode.txt": "Hello 世界",
            "emoji.txt": "🌟 Star ⭐",
            "control.txt": "Line1\x00Line2\x1FLine3",
            "mixed.txt": "ascii\n中文\nемодзи\n🎉"
        }
        
        for name, content in files.items():
            (Path(temp_dir) / name).write_text(content, encoding="utf-8")
        
        config = {
            "base_dir": temp_dir,
            "model_name": "claude-3-sonnet",
            "disable_progress": True
        }
        tokenizer = TokenizerService(config)
        
        for name in files:
            result = tokenizer.process_file(str(Path(temp_dir) / name))
            assert result["success"]
            assert result["tokens"] > 0
    
    def test_error_recovery(self, temp_dir):
        """Test error recovery during directory processing."""
        # Create a mix of valid and invalid files
        (Path(temp_dir) / "valid.txt").write_text("Valid content")
        (Path(temp_dir) / "binary.bin").write_bytes(bytes(range(256)))
        
        # Create an unreadable file
        unreadable = Path(temp_dir) / "unreadable.txt"
        unreadable.write_text("Content")
        os.chmod(unreadable, 0o000)  # Remove all permissions
        
        config = {
            "base_dir": temp_dir,
            "model_name": "claude-3-sonnet",
            "disable_progress": True
        }
        tokenizer = TokenizerService(config)
        stats = tokenizer.process_directory()
        
        # Should continue processing after errors
        assert stats["files_processed"] > 0
        assert len(stats.get("errors", [])) > 0
        assert "valid.txt" in str(stats.get("processed_files", []))
    
    def test_symlink_handling(self, temp_dir):
        """Test handling of symbolic links."""
        # Create a target file
        target_file = Path(temp_dir) / "target.txt"
        target_file.write_text("Target content")
        
        # Create a symlink
        link_file = Path(temp_dir) / "link.txt"
        try:
            link_file.symlink_to(target_file)
            
            config = {
                "base_dir": temp_dir,
                "model_name": "claude-3-sonnet",
                "disable_progress": True
            }
            tokenizer = TokenizerService(config)
            result = tokenizer.process_file(str(link_file))
            
            assert result["success"]
            assert result["tokens"] > 0
        except OSError:
            pytest.skip("Symlink creation not supported")
    
    def test_max_file_limit(self, temp_dir):
        """Test handling of maximum file size limit."""
        # Create a file larger than max size
        max_size = 10 * 1024 * 1024  # 10MB
        large_file = Path(temp_dir) / "huge.txt"
        
        try:
            with open(large_file, "w") as f:
                f.write("A" * max_size)
        except MemoryError:
            pytest.skip("Not enough memory for test")
        
        config = {
            "base_dir": temp_dir,
            "model_name": "claude-3-sonnet",
            "disable_progress": True
        }
        tokenizer = TokenizerService(config)
        result = tokenizer.process_file(str(large_file))
        
        assert not result["success"]
        assert "file too large" in result.get("error", "").lower() 