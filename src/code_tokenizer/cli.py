"""Command-line interface for code tokenizer."""

import argparse
import logging
import os
import sys
import json
import yaml
from argparse import ArgumentParser, Namespace
from typing import List, Optional, Dict, Any

from . import __version__
from .models.model_config import DEFAULT_MODEL, MODEL_ENCODINGS, TokenizerConfig
from .services.filesystem_service import RealFileSystemService
from .services.tokenizer_service import TokenizerService

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def create_argument_parser() -> ArgumentParser:
    """Create the argument parser for the command-line interface.

    Returns:
        ArgumentParser: The configured argument parser
    """
    parser = argparse.ArgumentParser(
        description="Process and count tokens in code files.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Required arguments
    parser.add_argument("-d", "--directory", required=True, help="Directory to process")
    parser.add_argument("-o", "--output", required=True, help="Output file path")

    # Optional arguments
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        choices=list(MODEL_ENCODINGS.keys()),
        help="Model to use for tokenization",
    )
    parser.add_argument(
        "--max-tokens", type=int, help="Maximum tokens per file (default: model's context limit)"
    )
    parser.add_argument(
        "--format", choices=["markdown", "json"], default="markdown", help="Output format"
    )
    parser.add_argument("--bypass-gitignore", action="store_true", help="Bypass .gitignore rules")
    parser.add_argument("--no-metadata", action="store_true", help="Exclude metadata from output")

    # File filtering options
    parser.add_argument("--include", nargs="+", help="File extensions to include (e.g., py js ts)")
    parser.add_argument("--exclude", nargs="+", help="File extensions to exclude")

    # Display options
    parser.add_argument("--no-progress", action="store_true", help="Disable progress bar")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    # Add sanitization options
    parser.add_argument(
        "--no-sanitize",
        action="store_true",
        help="Disable content sanitization",
    )
    parser.add_argument(
        "--preserve-comments",
        action="store_true",
        help="Preserve code comments in output",
        default=True,
    )
    parser.add_argument(
        "--aggressive-whitespace",
        action="store_true",
        help="Aggressively minimize whitespace",
    )

    return parser


def parse_args(args: Optional[List[str]] = None) -> Namespace:
    """Parse command line arguments.

    Args:
        args: Command line arguments. Defaults to None.

    Returns:
        Namespace: Parsed arguments
    """
    parser = create_argument_parser()
    parsed_args = parser.parse_args(args)

    # Configure logging based on verbosity
    if parsed_args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    elif parsed_args.verbose:
        logging.getLogger().setLevel(logging.INFO)
    else:
        logging.getLogger().setLevel(logging.WARNING)

    return parsed_args


def format_output(stats: Dict[str, Any], output_format: str) -> str:
    """Format the output based on the specified format.

    Args:
        stats: Statistics from processing
        output_format: Output format (json, yaml, markdown)

    Returns:
        Formatted output string
    """
    if output_format == "json":
        return json.dumps(stats, indent=2)
    elif output_format == "yaml":
        return yaml.safe_dump(stats, default_flow_style=False)
    elif output_format == "markdown":
        lines = [
            "# Code Tokenization Report\n",
            "## Statistics\n",
            f"- Files processed: {stats['files_processed']}",
            f"- Total tokens: {stats['total_tokens']:,}",
            f"- Total size: {stats['total_size']:,} bytes\n",
            "## Languages\n"
        ]
        for lang, count in stats["languages"].items():
            lines.append(f"- {lang}: {count} files")
        if stats["failed_files"]:
            lines.extend(["\n## Failed Files\n"])
            for file in stats["failed_files"]:
                lines.append(f"- {file}")
        return "\n".join(lines)
    else:
        raise ValueError(f"Unsupported output format: {output_format}")


def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI.

    Args:
        args: Optional list of command line arguments

    Returns:
        Exit code (0 for success, non-zero for error)
    """
    try:
        # Parse arguments
        parsed_args = parse_args(args)

        # Initialize services
        fs_service = RealFileSystemService()
        
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(parsed_args.output)
        if output_dir:
            fs_service.create_directory(output_dir)

        # Initialize tokenizer service
        config = TokenizerConfig({
            "base_dir": parsed_args.directory,
            "model_name": parsed_args.model,
            "max_tokens": parsed_args.max_tokens,
            "output_format": parsed_args.format,
            "bypass_gitignore": parsed_args.bypass_gitignore,
            "sanitize_content": not parsed_args.no_sanitize,
            "no_progress": parsed_args.no_progress,
        })
        tokenizer = TokenizerService(config, fs_service)

        # Process directory
        result = tokenizer.process_directory(
            directory=parsed_args.directory,
            output_path=parsed_args.output
        )

        return 0

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
