import argparse
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from .converter import (
    convert_codebase_to_markdown,
    MODEL_CONTEXT_SIZES,
    get_model_context_size,
    get_model_description,
)

def format_size(size_bytes):
    """Format size in bytes to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

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
            context_size = format_size(MODEL_CONTEXT_SIZES[model] * 4)  # Approximate bytes (4 bytes per token)
            description = get_model_description(model)
            model_info = f"{model:<20}"
            if description != model:
                model_info += f" ({description})"
            lines.append(f"  - {model_info:<40} {MODEL_CONTEXT_SIZES[model]:,} tokens / ~{context_size}")
    
    return "\n".join(lines)

def main():
    console = Console()
    
    # Create the argument parser with extended help
    parser = argparse.ArgumentParser(
        description='''
Convert codebase to LLM-friendly documentation.

This tool scans a codebase directory and creates a documentation file containing
the contents of all files, organized in a format suitable for LLMs. Features:
- Automatic language detection and syntax highlighting
- Token counting for various LLM models
- File size and metadata tracking
- Progress bar and statistics
- Multiple output formats (markdown, JSON)
- Configurable token limits per file

''' + format_model_list() + '''

Examples:
  # Basic usage - convert a codebase to markdown
  codebase-to-markdown -d ./my-project -m output.md

  # Use with Claude 3 Opus (200K context)
  codebase-to-markdown -d ./my-project -m output.md --model claude-3-opus --max-tokens 2000

  # Use custom gitignore file
  codebase-to-markdown -d ./my-project -m output.md --gitignore ./custom/.gitignore

  # Generate JSON output for programmatic processing
  codebase-to-markdown -d ./my-project -m output.json --format json

  # Ignore specific directories and files
  codebase-to-markdown -d ./my-project -m output.md --ignore-dirs build dist --ignore-files .env

  # Process large files without truncation
  codebase-to-markdown -d ./my-project -m output.md --max-tokens 0
''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('-d', '--directory', 
                       help='Path to the codebase directory to convert')
    parser.add_argument('-m', '--markdown', 
                       help='Path for the output file')
    parser.add_argument('--gitignore', 
                       help='Path to custom .gitignore file (default: looks for .gitignore in codebase directory)')
    parser.add_argument('--ignore-dirs', nargs='*', default=[], 
                       help='Additional directories to ignore (e.g., node_modules, __pycache__)')
    parser.add_argument('--ignore-files', nargs='*', default=[], 
                       help='Additional files to ignore (e.g., .env, .gitignore)')
    parser.add_argument('--max-tokens', type=int, default=1000,
                       help='Maximum tokens per file (0 for no limit)')
    parser.add_argument('--format', choices=['markdown', 'json'], default='markdown',
                       help='Output format (default: markdown)')
    parser.add_argument('--model', default='gpt-4o', choices=list(MODEL_CONTEXT_SIZES.keys()),
                       help='Target LLM model for token counting and limits (default: gpt-4o)')
    parser.add_argument('--no-metadata', action='store_true',
                       help='Exclude file metadata from output')
    
    # If no arguments are provided, print help and exit
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    
    args = parser.parse_args()
    
    # Check required arguments after help check
    if not args.directory or not args.markdown:
        parser.error("Both --directory and --markdown arguments are required")
    
    # Convert the codebase
    try:
        with console.status("[bold green]Converting codebase..."):
            stats = convert_codebase_to_markdown(
                args.directory,
                args.markdown,
                args.ignore_dirs,
                args.ignore_files,
                args.max_tokens,
                args.format,
                args.model,
                not args.no_metadata,
                args.gitignore
            )
        
        # Display statistics in a nice format
        console.print("\n[bold green]✓ Conversion completed![/bold green]\n")
        
        # Create statistics table
        table = Table(title="Conversion Statistics")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", justify="right", style="green")
        
        table.add_row("Total Files", str(stats["total_files"]))
        table.add_row("Total Tokens", f"{stats['total_tokens']:,}")
        table.add_row("Total Size", format_size(stats["total_size_bytes"]))
        table.add_row("Truncated Files", str(stats["truncated_files"]))
        table.add_row("Skipped Files", str(stats["skipped_files"]))
        
        console.print(table)
        
        # Display language statistics
        if stats["languages"]:
            lang_table = Table(title="\nLanguage Distribution")
            lang_table.add_column("Language", style="cyan")
            lang_table.add_column("Files", justify="right", style="green")
            
            for lang, count in sorted(stats["languages"].items(), key=lambda x: x[1], reverse=True):
                lang_table.add_row(lang, str(count))
            
            console.print(lang_table)
        
        # Display token usage warning if relevant
        model_context_size = get_model_context_size(args.model)
        if stats["total_tokens"] > model_context_size:
            console.print(Panel(
                f"[yellow]⚠️ Warning: Total token count ({stats['total_tokens']:,}) exceeds {args.model}'s context window ({model_context_size:,} tokens).\n"
                "Consider:\n"
                f"1. Using a model with larger context (e.g., {max(MODEL_CONTEXT_SIZES, key=MODEL_CONTEXT_SIZES.get)})\n"
                "2. Reducing the codebase size\n"
                "3. Increasing the truncation limit[/yellow]",
                title="Token Usage Warning"
            ))
        
        console.print(f"\nOutput saved to: [blue]{args.markdown}[/blue]")
        
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
        sys.exit(1)

if __name__ == '__main__':
    main() 