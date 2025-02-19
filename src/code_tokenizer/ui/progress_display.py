"""UI components for displaying progress and statistics."""

import os
import sys
import time
from typing import Any, Dict, List, Optional, Union
from collections import defaultdict

from rich import box
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TaskID, TextColumn
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


def create_display_layout(
    progress: Optional[Progress] = None,
    stats: Optional[Union[Table, str]] = None
) -> Layout:
    """Create the main display layout.

    Args:
        progress: Optional progress component
        stats: Optional stats table component

    Returns:
        Layout: The configured display layout
    """
    layout = Layout()

    # Create layout sections
    layout.split(
        Layout(name="header", size=3),
        Layout(name="body"),
        Layout(name="footer", size=10)
    )

    # Split body into progress and stats
    layout["body"].split_row(
        Layout(name="progress", ratio=2),
        Layout(name="stats", ratio=1)
    )

    # Add components
    if progress:
        layout["progress"].update(progress)
    if stats:
        layout["stats"].update(stats)

    return layout


def update_display(
    layout: Layout,
    progress: Progress,
    stats: Dict[str, Any],
    current_file: str = "",
    status: str = "",
    errors: Optional[List[str]] = None,
) -> None:
    """Update the display with current progress and stats.

    Args:
        layout: Layout to update
        progress: Progress component
        stats: Statistics to display
        current_file: Current file being processed
        status: Current status message
        errors: Optional list of error messages
    """
    if not isinstance(layout, Layout):
        return

    # Update header
    header = layout.get("header")
    if header:
        header.update(
            Panel(
                f"Processing: {current_file}",
                title="Code Tokenizer",
                border_style="blue"
            )
        )

    # Update progress
    progress_section = layout.get("progress")
    if progress_section and progress:
        progress_section.update(progress)

    # Update stats
    stats_section = layout.get("stats")
    if stats_section:
        stats_section.update(create_stats_table(stats))

    # Update footer with errors
    footer = layout.get("footer")
    if footer and errors:
        error_text = "\n".join(f"• {error}" for error in errors[-5:])
        footer.update(
            Panel(error_text, title="Errors", border_style="red")
        )


class ProgressDisplay:
    """Display progress and statistics for code tokenization."""

    def __init__(self, test_mode: bool = False) -> None:
        """Initialize progress display.

        Args:
            test_mode: Whether to run in test mode
        """
        self.test_mode = test_mode
        self.display_mode = DisplayMode()
        self.console = self.display_mode.console
        self.progress: Optional[Progress] = None
        self.layout: Optional[Layout] = None
        self.task_id: Optional[TaskID] = None
        self.current_file: Optional[str] = None
        self.current: int = 0
        self.total: int = 0
        self.language_stats: Dict[str, int] = defaultdict(int)
        self.errors: List[str] = []

        if not test_mode:
            self.progress = create_progress_group()
            self.layout = create_display_layout(self.progress)
            if self.progress:
                self.task_id = self.progress.add_task("Processing...", total=0)

    def create_display_component(
        self, component_type: str, data: Any = None
    ) -> Optional[Union[Table, Panel, Progress]]:
        """Create a display component based on the type.

        Args:
            component_type: Type of component to create
            data: Data to display in the component

        Returns:
            Optional display component
        """
        if component_type == "table":
            table = Table(show_header=False, box=box.SIMPLE)
            table.add_column("Metric", style="bold cyan")
            table.add_column("Value")
            if isinstance(data, dict):
                for key, value in data.items():
                    table.add_row(str(key), str(value))
            return table
        elif component_type == "progress":
            if isinstance(data, dict):
                file_path = data.get("file", "")
                current = data.get("current", 0)
                total = data.get("total", 0)
                self.update_display(file_path, current, total)
            return self.progress
        elif component_type == "panel":
            if isinstance(data, str):
                return Panel(data, border_style="blue")
            return Panel(str(data), border_style="blue")
        return None

    def update_display(
        self,
        file_path: Optional[str] = None,
        current: Optional[int] = None,
        total: Optional[int] = None,
        errors: Optional[List[str]] = None,
    ) -> None:
        """Update the display with current progress and stats.

        Args:
            file_path: Optional path of the current file being processed
            current: Optional current progress value
            total: Optional total number of items to process
            errors: Optional list of error messages
        """
        if not self.test_mode:
            if file_path:
                self.current_file = file_path
            if current is not None:
                self.current = current
            if total is not None:
                self.total = total

            # Update progress
            if self.progress and self.task_id:
                self.progress.update(
                    task_id=self.task_id,
                    completed=self.current,
                    total=self.total,
                    description=self.current_file or ""
                )

            # Update display
            if self.layout and self.progress:
                update_display(
                    self.layout,
                    self.progress,
                    self.language_stats,
                    self.current_file or "",
                    "",
                    errors
                )

    def update_language_stats(self, language: str) -> None:
        """Update language statistics.

        Args:
            language: Detected language
        """
        self.language_stats[language] = self.language_stats.get(language, 0) + 1

    def add_error(self, file_path: str, error_message: str) -> None:
        """Add an error message for a file.

        Args:
            file_path: Path to the file with the error
            error_message: The error message
        """
        self.errors.append(error_message)

    def get_stats_display(self) -> str:
        """Get a string representation of the current statistics.

        Returns:
            str: Statistics display string
        """
        stats = []
        stats.append(f"Files Processed: {self.current}")

        if self.language_stats:
            lang_stats = ", ".join(
                f"{lang}: {count}" for lang, count in sorted(self.language_stats.items())
            )
            stats.append(lang_stats)

        if self.errors:
            stats.append(f"Skipped Files: {len(self.errors)}")

        return "\n".join(stats)

    def set_total(self, total: int) -> None:
        """Set the total number of files to process.

        Args:
            total: Total number of files
        """
        self.total = total
        if not self.test_mode and self.progress and self.task_id:
            self.progress.update(task_id=self.task_id, total=total)

    def finish(self) -> None:
        """Complete the progress display."""
        if not self.test_mode and self.progress:
            self.progress.stop()

    def error(self, message: str) -> None:
        """Display an error message.

        Args:
            message: Error message to display
        """
        if not self.test_mode and self.console:
            self.console.print(f"[red]Error: {message}[/red]")

    def warning(self, message: str) -> None:
        """Display a warning message.

        Args:
            message: Warning message to display
        """
        if not self.test_mode and self.console:
            self.console.print(f"[yellow]Warning: {message}[/yellow]")

    def info(self, message: str) -> None:
        """Display an info message.

        Args:
            message: Info message to display
        """
        if not self.test_mode and self.console:
            self.console.print(f"[blue]Info: {message}[/blue]")

    def success(self, message: str) -> None:
        """Display a success message.

        Args:
            message: Success message to display
        """
        if not self.test_mode and self.console:
            self.console.print(f"[green]Success: {message}[/green]")

    def update_progress(self, current: int, total: int) -> None:
        """Update the progress bar with current progress."""
        if self.progress and self.task_id:
            self.progress.update(
                task_id=self.task_id,
                completed=current,
                total=total
            )
