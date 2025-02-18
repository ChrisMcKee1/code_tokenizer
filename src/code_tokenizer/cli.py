import argparse
import sys
from pathlib import Path
from rich.console import Console
from .models.model_config import MODEL_CONTEXT_SIZES
from .services.tokenizer_service import TokenizerService
import json


def format_model_list() -> str:
    """Format the list of supported models with their context sizes."""
    lines = ["Supported Models:"]

    # Group models by provider
    providers = {
        "OpenAI": [m for m in MODEL_CONTEXT_SIZES.keys() if m.startswith(("gpt-", "o"))],
        "Anthropic": [m for m in MODEL_CONTEXT_SIZES.keys() if "claude" in m],
        "Google": [m for m in MODEL_CONTEXT_SIZES.keys() if "gemini" in m],
        "DeepSeek": [m for m in MODEL_CONTEXT_SIZES.keys() if "deepseek" in m],
    }

    for provider, models in providers.items():
        if not models:
            continue
        lines.append(f"\n{provider} Models:")
        for model in sorted(models):
            context_size = f"{MODEL_CONTEXT_SIZES[model]:,}"
            lines.append(f"  - {model:<25} {context_size} tokens")

    return "\n".join(lines)


def main() -> None:
    """Main entry point for the CLI."""
    console = Console()

    parser = argparse.ArgumentParser(
        description="""
Code Tokenizer - Transform your codebase into LLM-ready tokens with intelligent processing.

This tool analyzes your codebase and generates documentation with token counts and statistics,
making it easy to prepare your code for LLM analysis while respecting .gitignore rules.
""",
        epilog=format_model_list(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "-d", "--directory", required=True, help="Directory containing the codebase to analyze"
    )

    parser.add_argument(
        "-o", "--output", required=True, help="Output directory for generated files"
    )

    parser.add_argument(
        "--model",
        default="claude-3-sonnet",
        choices=list(MODEL_CONTEXT_SIZES.keys()),
        help="LLM model to use for token counting (default: claude-3-sonnet)",
    )

    parser.add_argument(
        "--max-tokens",
        type=int,
        default=2000,
        help="Maximum tokens per file (default: 2000, 0 for no limit)",
    )

    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format (default: markdown)",
    )

    parser.add_argument(
        "--bypass-gitignore",
        action="store_true",
        help="Bypass all .gitignore rules and process all files",
    )

    parser.add_argument(
        "--no-metadata", action="store_true", help="Exclude file metadata from output"
    )

    try:
        args = parser.parse_args()

        # Create output directory if it doesn't exist
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate output filenames
        base_name = Path(args.directory).name
        docs_ext = "json" if args.format == "json" else "markdown"
        docs_file = output_dir / f"{base_name}_docs.{docs_ext}"
        analysis_file = output_dir / f"{base_name}_analysis.md"

        console.print(f"\nProcessing {args.directory}...")

        # Initialize and run tokenizer service
        config = {
            "base_dir": args.directory,
            "model_name": args.model,
            "max_tokens_per_file": args.max_tokens,
            "output_format": args.format,
            "output_dir": str(output_dir),
            "include_metadata": not args.no_metadata,
            "bypass_gitignore": args.bypass_gitignore
        }
        
        tokenizer = TokenizerService(config)
        stats = tokenizer.process_directory()

        # Write documentation file
        if args.format == "json":
            docs_content = {
                "project_name": base_name,
                "model": args.model,
                "max_tokens": args.max_tokens,
                "files": stats.get("processed_files", []),
                "stats": {
                    k: v for k, v in stats.items() 
                    if k != "processed_files"
                }
            }
            with open(docs_file, "w") as f:
                json.dump(docs_content, f, indent=2)
        else:
            with open(docs_file, "w") as f:
                f.write(f"# {base_name} Documentation\n\n")
                f.write(f"Generated with Code Tokenizer using {args.model}\n\n")
                
                # Write statistics
                f.write("## Statistics\n\n")
                for key, value in stats.items():
                    if key == "processed_files":
                        continue
                    if isinstance(value, dict):
                        f.write(f"### {key.title()}\n")
                        for k, v in value.items():
                            f.write(f"- {k}: {v}\n")
                    else:
                        f.write(f"- {key.replace('_', ' ').title()}: {value}\n")
                
                # Write file contents
                if processed_files := stats.get("processed_files"):
                    f.write("\n## Files\n\n")
                    for file_info in processed_files:
                        f.write(f"### {file_info['path']}\n\n")
                        f.write(f"- Language: {file_info['language']}\n")
                        f.write(f"- Tokens: {file_info['tokens']}\n")
                        f.write(f"- Size: {file_info['size']} bytes\n\n")
                        f.write("```" + file_info['language'].lower() + "\n")
                        f.write(file_info['content'])
                        f.write("\n```\n\n")

        # Write analysis file
        with open(analysis_file, "w") as f:
            f.write(f"# {base_name} Analysis\n\n")
            f.write("## Processing Statistics\n\n")
            f.write(f"- Files Processed: {stats['files_processed']}\n")
            f.write(f"- Total Tokens: {stats['total_tokens']:,}\n")
            f.write(f"- Total Size: {stats['total_size']:,} bytes\n")
            if stats.get("skipped_files"):
                f.write(f"- Skipped Files: {stats['skipped_files']}\n")
            if stats.get("truncated_files"):
                f.write(f"- Truncated Files: {stats['truncated_files']}\n")
            
            if languages := stats.get("languages"):
                f.write("\n## Language Distribution\n\n")
                for lang, count in languages.items():
                    f.write(f"- {lang}: {count} files\n")

        # Print success message
        console.print(f"\n[green]✓ Documentation written to:[/green] {docs_file}")
        console.print(f"[green]✓ Analysis written to:[/green] {analysis_file}")

        # Print summary
        console.print(f"\n[bold cyan]Summary:[/bold cyan]")
        console.print(f"- Processed {stats['files_processed']} files")
        console.print(f"- Total tokens: {stats['total_tokens']:,}")
        console.print(f"- Languages: {', '.join(stats['languages'].keys())}")

        if stats.get("errors"):
            console.print(
                f"\n[yellow]⚠️ {len(stats['errors'])} errors occurred. Check the analysis file for details.[/yellow]"
            )

    except ValueError as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
