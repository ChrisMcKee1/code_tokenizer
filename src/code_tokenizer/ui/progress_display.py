"""UI components for displaying progress and statistics."""

import os
import sys
from typing import Dict, List, Optional, Union

from rich import box
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.text import Text


class DisplayMode:
    """Controls the display mode of the UI"""

    def __init__(self) -> None:
        self._is_test_mode = self._detect_test_mode()
        self._console = Console(force_terminal=not self._is_test_mode)

    @staticmethod
    def _detect_test_mode() -> bool:
        """Detect if we're running in a test environment"""
        return (
            "pytest" in sys.modules
            or os.getenv("DISABLE_RICH_PROGRESS", "0") == "1"
            or os.getenv("PYTEST_CURRENT_TEST") is not None
        )

    @property
    def is_test_mode(self) -> bool:
        return self._is_test_mode

    @property
    def console(self) -> Console:
        return self._console


# Global display mode instance
DISPLAY_MODE = DisplayMode()


def create_progress_group() -> Progress:
    """
    Create a progress group with multiple progress bars.

    Returns:
        Progress: Rich progress group with configured columns
    """
    if DISPLAY_MODE.is_test_mode:
        return Progress(
            TextColumn("[progress.description]{task.description}"),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TextColumn("[progress.remaining]{task.completed}/{task.total}"),
            console=DISPLAY_MODE.console,
            expand=True,
        )

    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TextColumn("[progress.remaining]{task.completed}/{task.total}"),
        TextColumn("[progress.elapsed]{task.elapsed:.2f}s"),
        console=DISPLAY_MODE.console,
        expand=True,
    )


def create_stats_table(stats: Dict) -> Union[Table, str]:
    """Create a table displaying processing statistics."""
    if DISPLAY_MODE.is_test_mode:
        # Return simple string representation for tests
        lines = [
            f"Files Processed: {stats.get('files_processed', 0)}",
            f"Total Tokens: {stats.get('total_tokens', 0):,}",
            f"Total Size: {stats.get('total_size', 0):,} bytes",
        ]
        if stats.get("skipped_files"):
            lines.append(f"Skipped Files: {stats['skipped_files']}")
        if stats.get("truncated_files"):
            lines.append(f"Truncated Files: {stats['truncated_files']}")
        if languages := stats.get("languages", {}):
            lang_str = ", ".join(f"{lang}: {count}" for lang, count in languages.items())
            lines.append(f"Languages: {lang_str}")
        return "\n".join(lines)

    # Rich table for CLI usage
    table = Table(show_header=False, box=box.SIMPLE)
    table.add_column("Metric", style="bold cyan")
    table.add_column("Value")

    table.add_row("Files Processed", str(stats.get("files_processed", 0)))
    table.add_row("Total Tokens", f"{stats.get('total_tokens', 0):,}")
    table.add_row("Total Size", f"{stats.get('total_size', 0):,} bytes")

    if stats.get("skipped_files"):
        table.add_row("Skipped Files", str(stats["skipped_files"]))
    if stats.get("truncated_files"):
        table.add_row("Truncated Files", str(stats["truncated_files"]))

    if languages := stats.get("languages", {}):
        lang_str = ", ".join(f"{lang}: {count}" for lang, count in languages.items())
        table.add_row("Languages", lang_str)

    return table


def create_display_layout() -> Layout:
    """Create the display layout for the progress UI."""
    layout = Layout()

    # Create main sections
    layout.split(Layout(name="header", size=3), Layout(name="body"), Layout(name="footer", size=10))

    # Split body into progress and stats
    layout["body"].split_row(Layout(name="progress", ratio=2), Layout(name="stats"))

    return layout


def update_display(
    layout: Layout,
    progress: Progress,
    stats: Dict,
    current_file: str = "",
    status: str = "",
    errors: Optional[List[str]] = None,
) -> None:
    """
    Update the display layout with current progress and statistics.

    Args:
        layout: Rich layout to update
        progress: Progress group containing progress bars
        stats: Current statistics dictionary
        current_file: Currently processing file
        status: Current status message
        errors: List of error messages to display
    """
    if DISPLAY_MODE.is_test_mode:
        # Simple output for tests
        DISPLAY_MODE.console.print(f"Processing: {current_file}")
        if status:
            DISPLAY_MODE.console.print(f"Status: {status}")
        if isinstance(stats, dict):
            DISPLAY_MODE.console.print(create_stats_table(stats))
        if errors:
            DISPLAY_MODE.console.print("Errors:", style="red")
            for error in errors:
                DISPLAY_MODE.console.print(f"• {error}", style="red")
        return

    # Rich UI for CLI usage
    layout["header"].update(
        Panel(
            Text(f"Processing: {current_file}", style="bold blue"),
            title="Code Tokenizer",
            border_style="blue",
        )
    )

    layout["progress"].update(Panel(progress, title="Progress", border_style="green"))

    stats_table = create_stats_table(stats)
    layout["stats"].update(Panel(stats_table, title="Statistics", border_style="magenta"))

    footer_content = [Text(status, style="bold green")]
    if errors:
        footer_content.extend(
            [
                Text("\nErrors:", style="bold red"),
                Text("\n" + "\n".join(f"• {error}" for error in errors), style="red"),
            ]
        )

    layout["footer"].update(
        Panel(Text.assemble(*footer_content), title="Status", border_style="yellow")
    )


class ProgressDisplay:
    """Handles progress display and updates."""
    
    def __init__(self) -> None:
        self.current = 0
        self.total = 0
        self.file_path = ""
        self.errors: List[str] = []
        self.layout = create_display_layout()
        self.progress = create_progress_group()
        
    def update_progress(
        self,
        current: int,
        total: int,
        file_path: str = "",
        errors: Optional[List[str]] = None,
    ) -> None:
        """Update the progress display with current status."""
        self.current = current
        self.total = total
        self.file_path = file_path
        self.errors = errors or []
        self._update_display()
        
    def _update_display(self) -> None:
        """Update the live display with current progress."""
        update_display(
            self.layout,
            self.progress,
            {"current": self.current, "total": self.total},
            self.file_path,
            f"Processing {self.current}/{self.total}",
            self.errors
        )
