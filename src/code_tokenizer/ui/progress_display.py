"""UI components for displaying progress and statistics."""

import os
import sys
import time
from typing import Any, Dict, List, Optional, Union

from rich import box
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, TaskID
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
    """Display progress for code tokenization tasks."""

    def __init__(self, test_mode: bool = False) -> None:
        """Initialize the progress display.

        Args:
            test_mode: Whether to run in test mode (disables rich output)
        """
        self.test_mode = test_mode
        self.current = 0
        self.total = 0
        self.file_path = None
        self.language_stats: Dict[str, int] = {}
        self.errors: List[str] = []
        self.console = Console(record=test_mode, force_terminal=not test_mode)
        self.progress = create_progress_group()
        self.layout = create_display_layout()

    def create_display_component(self, component_type: str, data: Any = None) -> Optional[Union[Table, Panel, Progress]]:
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

    def update_display(self, file_path: Optional[str] = None, current: Optional[int] = None, 
                      total: Optional[int] = None, errors: Optional[List[str]] = None) -> None:
        """Update the display with current progress.

        Args:
            file_path: Current file being processed
            current: Current progress value
            total: Total progress value
            errors: List of error messages
        """
        if file_path:
            self.file_path = file_path
        if current is not None:
            self.current = current
        if total is not None:
            self.total = total
        if errors:
            self.errors.extend(errors)

        if self.test_mode:
            self.console.print(f"Processing: {self.file_path}")
            self.console.print(f"Progress: {self.current}/{self.total}")
            if self.errors:
                self.console.print("Errors:", style="red")
                for error in self.errors:
                    self.console.print(f"• {error}", style="red")
            return

        stats = {
            "files_processed": self.current,
            "total_files": self.total,
            "languages": self.language_stats
        }

        update_display(
            self.layout,
            self.progress,
            stats,
            self.file_path,
            f"Processing file {self.current} of {self.total}",
            self.errors
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
                f"{lang}: {count}" 
                for lang, count in sorted(self.language_stats.items())
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
        if not self.test_mode and self.progress:
            self.progress.update(self.progress.tasks[0], total=total)

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
