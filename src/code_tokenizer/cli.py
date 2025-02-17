import argparse
import sys
from pathlib import Path
from rich.console import Console
from .converter import (
    process_codebase_to_docs,
    write_stats_file,
    MODEL_CONTEXT_SIZES,
)

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

def main():
    console = Console()
    
    parser = argparse.ArgumentParser(
        description="""
Code Tokenizer - Transform your codebase into LLM-ready tokens with intelligent processing.

This tool analyzes your codebase and generates documentation with token counts and statistics,
making it easy to prepare your code for LLM analysis while respecting .gitignore rules.
""",
        epilog=format_model_list(),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "-d", "--directory",
        required=True,
        help="Directory containing the codebase to analyze"
    )
    
    parser.add_argument(
        "-o", "--output",
        required=True,
        help="Output directory for generated files"
    )
    
    parser.add_argument(
        "--model",
        default="claude-3-sonnet",
        choices=list(MODEL_CONTEXT_SIZES.keys()),
        help="LLM model to use for token counting (default: claude-3-sonnet)"
    )
    
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=2000,
        help="Maximum tokens per file (default: 2000, 0 for no limit)"
    )
    
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format (default: markdown)"
    )
    
    parser.add_argument(
        "--gitignore",
        help="Path to custom .gitignore file"
    )
    
    parser.add_argument(
        "--no-metadata",
        action="store_true",
        help="Exclude file metadata from output"
    )
    
    try:
        args = parser.parse_args()
        
        # Validate model (this is redundant with choices, but keeping for clarity)
        if args.model not in MODEL_CONTEXT_SIZES:
            console.print(f"[bold red]Error: Invalid model '{args.model}'[/bold red]")
            console.print("Supported models:")
            console.print(format_model_list())
            sys.exit(1)
        
        # Create output directory if it doesn't exist
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate output filenames
        base_name = Path(args.directory).name
        docs_file = output_dir / f"{base_name}_docs.{args.format}"
        stats_file = output_dir / f"{base_name}_analysis.md"
        
        console.print(f"\n[bold green]Processing {args.directory}...[/bold green]")
        
        # Convert codebase
        stats = process_codebase_to_docs(
            args.directory,
            str(docs_file),
            max_tokens_per_file=args.max_tokens,
            output_format=args.format,
            model=args.model,
            include_metadata=not args.no_metadata,
            custom_gitignore=args.gitignore
        )
        
        # Write statistics
        write_stats_file(stats, args.directory, args.model, str(stats_file))
        
        # Print success message
        console.print(f"\n[green]✓ Documentation written to:[/green] {docs_file}")
        console.print(f"[green]✓ Analysis written to:[/green] {stats_file}")
        
        # Print summary
        console.print(f"\n[bold cyan]Summary:[/bold cyan]")
        console.print(f"- Processed {stats['total_files']} files")
        console.print(f"- Total tokens: {stats['total_tokens']:,}")
        console.print(f"- Languages: {', '.join(stats['languages'].keys())}")
        
        if stats['errors']:
            console.print(f"\n[yellow]⚠️ {len(stats['errors'])} errors occurred. Check the analysis file for details.[/yellow]")
        
    except ValueError as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
        sys.exit(1)

if __name__ == "__main__":
    main() 