"""Tests for UI components."""

import pytest
from rich.console import Console
from rich.layout import Layout
from rich.progress import Progress

from code_tokenizer.ui.progress_display import (
    DisplayMode,
    create_display_layout,
    create_progress_group,
    create_stats_table,
)


@pytest.mark.smoke
@pytest.mark.unit
def test_display_mode_initialization():
    """Test DisplayMode initialization and properties."""
    display_mode = DisplayMode()
    assert display_mode._is_test_mode is True
    assert isinstance(display_mode._console, Console)


@pytest.mark.unit
def test_display_mode_detect_test():
    """Test test mode detection."""
    display_mode = DisplayMode()
    assert display_mode._detect_test_mode() is True


@pytest.mark.unit
def test_display_mode_properties():
    """Test DisplayMode property access."""
    display_mode = DisplayMode()
    assert display_mode.is_test_mode is True
    assert isinstance(display_mode.console, Console)


@pytest.mark.smoke
@pytest.mark.unit
def test_create_progress_group():
    """Test progress group creation."""
    progress = create_progress_group()
    assert isinstance(progress, Progress)


@pytest.mark.integration
def test_create_stats_table_test_mode():
    """Test stats table creation in test mode."""
    stats = {
        "files_processed": 10,
        "total_tokens": 1000,
        "total_size": 5000,
        "skipped_files": 2,
        "truncated_files": 1,
        "languages": {"Python": 5, "JavaScript": 3},
    }

    result = create_stats_table(stats)
    assert isinstance(result, str)
    assert "Files Processed: 10" in result
    assert "Total Tokens: 1,000" in result
    assert "Total Size: 5,000 bytes" in result
    assert "Skipped Files: 2" in result
    assert "Truncated Files: 1" in result
    assert "Python: 5" in result
    assert "JavaScript: 3" in result


@pytest.mark.smoke
@pytest.mark.integration
def test_create_display_layout():
    """Test display layout creation."""
    # Create mock components
    progress = create_progress_group()
    stats = {"files_processed": 10, "total_tokens": 1000, "total_size": 5000}
    stats_table = create_stats_table(stats)

    # Create layout
    layout = create_display_layout(progress, stats_table)

    # Verify layout is created
    assert isinstance(layout, Layout)

    # Verify essential sections exist
    sections = ["header", "progress", "stats", "footer"]
    for section in sections:
        assert layout.get(section) is not None, f"Layout missing {section} section"

    # Verify section properties
    assert layout.get("header").size == 3
    assert layout.get("footer").size == 10
    assert layout.get("progress").ratio == 2
