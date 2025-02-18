"""Tests for UI components."""

import unittest
from unittest.mock import MagicMock, patch
import os
import pytest

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.progress import Progress

from code_tokenizer.ui.progress_display import (
    DISPLAY_MODE,
    DisplayMode,
    create_progress_group,
    create_stats_table,
    create_display_layout,
    update_display,
)

def test_display_mode_initialization():
    """Test DisplayMode initialization and properties."""
    display_mode = DisplayMode()
    assert display_mode._is_test_mode is True
    assert isinstance(display_mode._console, Console)

def test_display_mode_detect_test():
    """Test test mode detection."""
    display_mode = DisplayMode()
    assert display_mode._detect_test_mode() is True

def test_display_mode_properties():
    """Test DisplayMode property access."""
    display_mode = DisplayMode()
    assert display_mode.is_test_mode is True
    assert isinstance(display_mode.console, Console)

def test_create_progress_group():
    """Test progress group creation."""
    progress = create_progress_group()
    assert isinstance(progress, Progress)

def test_create_stats_table_test_mode():
    """Test stats table creation in test mode."""
    stats = {
        "files_processed": 10,
        "total_tokens": 1000,
        "total_size": 5000,
        "skipped_files": 2,
        "truncated_files": 1,
        "languages": {"Python": 5, "JavaScript": 3}
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

def test_create_display_layout():
    """Test display layout creation."""
    layout = create_display_layout()
    assert isinstance(layout, Layout)
    assert "header" in layout
    assert "body" in layout
    assert "footer" in layout
    assert "progress" in layout["body"]
    assert "stats" in layout["body"]
