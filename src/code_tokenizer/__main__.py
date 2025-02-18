"""Main entry point for code tokenizer."""

import argparse
import os
import sys
from typing import List

from rich.console import Console

from .models.model_config import DEFAULT_MODEL, MODEL_ENCODINGS, MODEL_TOKEN_LIMITS
from .services.tokenizer_service import TokenizerService


def parse_args() -> argparse.Namespace:
    """
    Parse command line arguments.

    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(description="Process and count tokens in code files.")

    parser.add_argument("directory", help="Directory to process")

    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        choices=list(MODEL_ENCODINGS.keys()),
        help=f"Model to use for tokenization (default: {DEFAULT_MODEL})",
    )

    parser.add_argument(
        "--max-tokens", type=int, help="Maximum tokens per file (default: model's context limit)"
    )

    parser.add_argument("--ignore-file", help="File containing ignore patterns (e.g. .gitignore)")

    return parser.parse_args()


def read_ignore_patterns(ignore_file: str) -> List[str]:
    """
    Read ignore patterns from a file.

    Args:
        ignore_file: Path to file containing ignore patterns

    Returns:
        List[str]: List of ignore patterns
    """
    if not os.path.exists(ignore_file):
        return []

    with open(ignore_file, "r") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


def main() -> int:
    """
    Main entry point.

    Returns:
        int: Exit code
    """
    console = Console()

    try:
        args = parse_args()

        # Validate directory
        if not os.path.isdir(args.directory):
            console.print(f"[red]Error: {args.directory} is not a directory[/]")
            return 1

        # Read ignore patterns
        ignore_patterns = []
        if args.ignore_file:
            ignore_patterns = read_ignore_patterns(args.ignore_file)

        # Create and run tokenizer service
        config = {
            "base_dir": args.directory,
            "model_name": args.model,
            "ignore_patterns": ignore_patterns,
            "max_tokens_per_file": args.max_tokens,
        }
        tokenizer = TokenizerService(config)

        stats = tokenizer.process_directory()

        # Print summary
        console.print("\n[bold green]Processing complete![/]")
        console.print(f"\nProcessed {stats['files_processed']} files:")
        console.print(f"• Total tokens: {stats['total_tokens']:,}")
        console.print(f"• Total size: {stats['total_size'] / 1024:.2f} KB")
        console.print(f"• Skipped files: {stats['skipped_files']}")
        console.print(f"• Truncated files: {stats['truncated_files']}")

        if stats["languages"]:
            console.print("\n[bold]Language breakdown:[/]")
            for lang, count in stats["languages"].items():
                console.print(f"• {lang}: {count} files")

        return 0

    except KeyboardInterrupt:
        console.print("\n[yellow]Processing interrupted by user[/]")
        return 130

    except Exception as e:
        console.print(f"\n[red]Error: {str(e)}[/]")
        return 1


if __name__ == "__main__":
    sys.exit(main())
