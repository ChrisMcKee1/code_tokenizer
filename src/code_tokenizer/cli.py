"""Command-line interface for code tokenizer."""

import argparse
import logging
import os
import sys
from argparse import ArgumentParser, Namespace
from typing import List, Optional

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


def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the code tokenizer.

    Args:
        args: Command line arguments. Defaults to None.

    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    try:
        if args is None:
            args = sys.argv[1:]

        parsed_args = parse_args(args)
        fs_service = RealFileSystemService()

        # Log startup information
        logger.info(f"Starting code-tokenizer v{__version__}")
        logger.debug(f"Arguments: {parsed_args}")

        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(parsed_args.output)
        if output_dir:
            fs_service.create_directory(output_dir)
            logger.debug(f"Created output directory: {output_dir}")

        # Process file extensions
        file_extensions = set(ext.strip(".") for ext in (parsed_args.include or []))
        skip_extensions = set(ext.strip(".") for ext in (parsed_args.exclude or []))

        # Create tokenizer config
        config = TokenizerConfig(
            {
                "model_name": parsed_args.model,
                "max_tokens": parsed_args.max_tokens,
                "bypass_gitignore": parsed_args.bypass_gitignore,
                "base_dir": parsed_args.directory,
                "output_format": parsed_args.format,
                "output_dir": output_dir,
                "include_metadata": not parsed_args.no_metadata,
                "file_extensions": file_extensions if file_extensions else None,
                "skip_extensions": skip_extensions if skip_extensions else None,
                "show_progress": not parsed_args.no_progress,
            }
        )

        # Create tokenizer service
        tokenizer = TokenizerService(config, fs_service)
        logger.info(f"Processing directory: {parsed_args.directory}")

        # Process the directory
        result = tokenizer.process_directory(
            directory=parsed_args.directory, output_path=parsed_args.output
        )

        # Log results
        stats = result["stats"]
        logger.info(f"Processed {stats['files_processed']} files")
        logger.info(f"Total tokens: {stats['total_tokens']:,}")

        if stats["files_processed"] == 0:
            logger.warning(
                "No files were processed. Check your directory path and gitignore settings."
            )
            return 0

        if result["failed_files"]:
            failed_count = len(result["failed_files"])
            logger.error(f"Failed to process {failed_count} files")
            if parsed_args.verbose:
                for file in result["failed_files"]:
                    logger.error(f"Failed file: {file}")
            return 1

        logger.info("Processing completed successfully")
        return 0

    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        return 130
    except Exception as e:
        logger.exception(f"Error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
