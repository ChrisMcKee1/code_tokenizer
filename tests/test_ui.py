"""UI component tests."""

from code_tokenizer.ui.progress_display import (
    create_progress_group,
    create_stats_table,
    create_display_layout,
    update_display,
)

class TestUI:
    """Test UI components."""
    
    def test_progress_display(self, console):
        """Test progress display functionality."""
        # Test progress group creation
        progress = create_progress_group()
        assert progress is not None
        
        # Test stats table creation
        stats = {
            "files_processed": 10,
            "total_tokens": 1000,
            "total_size": 5000,
            "skipped_files": 2,
            "truncated_files": 1,
            "languages": {"Python": 5, "JavaScript": 3}
        }
        table = create_stats_table(stats)
        assert table is not None
        
        # Test layout creation
        layout = create_display_layout()
        assert layout is not None
        
        # Test layout rendering
        console.print(layout)
        assert True  # If we get here, the layout rendered successfully 

    def test_progress_display_comprehensive(self, console):
        """Test all aspects of progress display."""
        # Test progress group with tasks
        progress = create_progress_group()
        task_id = progress.add_task("Test task", total=100)
        progress.advance(task_id, 50)
        assert progress.tasks[0].completed == 50
        
        # Test stats table with all possible fields
        stats = {
            "files_processed": 10,
            "total_tokens": 1000,
            "total_size": 5000,
            "skipped_files": 2,
            "truncated_files": 1,
            "errors": ["Test error 1", "Test error 2"],
            "languages": {
                "Python": 5,
                "JavaScript": 3,
                "JSON": 2
            }
        }
        table = create_stats_table(stats)
        assert table is not None
        
        # Test layout with all sections
        layout = create_display_layout()
        assert layout.get("header") is not None
        assert layout.get("body") is not None
        assert layout.get("footer") is not None
        assert layout["body"].get("progress") is not None
        assert layout["body"].get("stats") is not None
        
        # Test display update with all parameters
        update_display(
            layout=layout,
            progress=progress,
            stats=stats,
            current_file="test.py",
            status="Processing test.py",
            errors=["Test error"]
        )
        
        # Verify layout sections have content
        assert layout["header"].renderable is not None
        assert layout["body"]["progress"].renderable is not None
        assert layout["body"]["stats"].renderable is not None
        assert layout["footer"].renderable is not None
    
    def test_progress_display_updates(self, console):
        """Test progress display updates and animations."""
        # Create initial display
        progress = create_progress_group()
        layout = create_display_layout()
        stats = {"files_processed": 0, "total_tokens": 0}
        
        # Add multiple tasks
        tasks = [
            progress.add_task("Processing files", total=100),
            progress.add_task("Analyzing code", total=50),
            progress.add_task("Generating docs", total=10)
        ]
        
        # Update tasks and display
        for i in range(5):
            for task_id in tasks:
                progress.advance(task_id, 10)
                stats["files_processed"] = i + 1
                stats["total_tokens"] = (i + 1) * 1000
                
                update_display(
                    layout=layout,
                    progress=progress,
                    stats=stats,
                    current_file=f"file_{i}.py",
                    status=f"Processing file {i + 1}/5"
                )
                
                # Verify display updates
                assert layout["header"].renderable is not None
                assert "file_" in str(layout["header"].renderable)
                assert layout["body"]["progress"].renderable is not None
                assert layout["body"]["stats"].renderable is not None
    
    def test_error_display(self, console):
        """Test error display in progress UI."""
        progress = create_progress_group()
        layout = create_display_layout()
        
        # Test with no errors
        update_display(
            layout=layout,
            progress=progress,
            stats={},
            status="Running"
        )
        assert layout["footer"].renderable is not None
        assert "error" not in str(layout["footer"].renderable).lower()
        
        # Test with single error
        update_display(
            layout=layout,
            progress=progress,
            stats={},
            status="Error occurred",
            errors=["Test error message"]
        )
        footer_text = str(layout["footer"].renderable)
        assert "error" in footer_text.lower()
        assert "Test error message" in footer_text
        
        # Test with multiple errors
        errors = [
            "First error message",
            "Second error message",
            "Third error message"
        ]
        update_display(
            layout=layout,
            progress=progress,
            stats={},
            status="Multiple errors",
            errors=errors
        )
        footer_text = str(layout["footer"].renderable)
        assert all(error in footer_text for error in errors)
    
    def test_stats_table_formatting(self, console):
        """Test statistics table formatting."""
        # Test empty stats
        empty_table = create_stats_table({})
        assert empty_table is not None
        
        # Test minimal stats
        minimal_stats = {
            "files_processed": 1,
            "total_tokens": 100
        }
        minimal_table = create_stats_table(minimal_stats)
        assert minimal_table is not None
        assert "1" in str(minimal_table)
        assert "100" in str(minimal_table)
        
        # Test full stats with formatting
        full_stats = {
            "files_processed": 1234,
            "total_tokens": 1000000,
            "total_size": 5242880,  # 5MB
            "skipped_files": 10,
            "truncated_files": 5,
            "languages": {
                "Python": 100,
                "JavaScript": 50,
                "TypeScript": 25,
                "JSON": 10,
                "Markdown": 5
            }
        }
        full_table = create_stats_table(full_stats)
        table_str = str(full_table)
        
        # Verify number formatting
        assert "1,234" in table_str  # Comma-separated files
        assert "1,000,000" in table_str  # Comma-separated tokens
        assert "5,242,880" in table_str  # Formatted file size
        
        # Verify language formatting
        for lang, count in full_stats["languages"].items():
            assert f"{lang}: {count}" in table_str 