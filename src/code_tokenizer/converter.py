import os
import codecs
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import tiktoken
from pygments.lexers import get_lexer_for_filename
from pygments.util import ClassNotFound
from rich.console import Console
from rich.progress import Progress
import pathspec

# Model context window sizes (in tokens)
MODEL_CONTEXT_SIZES = {
    # OpenAI Models
    "gpt-4o": 128000,      
    "gpt-4o-mini": 128000, 
    "o1": 200000,          
    "o1-mini": 128000,     
    "o3-mini": 200000,     
    "o1-preview": 128000,  
    
    # Anthropic Models (all Claude 3 models have 200K context)
    "claude-3-opus": 200000,   
    "claude-3-sonnet": 200000, 
    "claude-3-haiku": 200000,  
    
    # Google Models
    "gemini-2.0-flash": 1048576,          
    "gemini-2.0-flash-lite-preview": 1048576, 
    "gemini-1.5-pro": 2097152,             
    
    # DeepSeek Models
    "deepseek-r1": 128000,            
}

# Model encoding mappings
MODEL_ENCODINGS = {
    # OpenAI Models use cl100k_base encoding
    "gpt-4o": "cl100k_base",
    "gpt-4o-mini": "cl100k_base",
    "o1": "cl100k_base",
    "o1-mini": "cl100k_base",
    "o3-mini": "cl100k_base",
    "o1-preview": "cl100k_base",
    
    # Other models default to cl100k_base as it's similar to most modern tokenizers
    "claude-3-opus": "cl100k_base",
    "claude-3-sonnet": "cl100k_base",
    "claude-3-haiku": "cl100k_base",
    "gemini-2.0-flash": "cl100k_base",
    "gemini-2.0-flash-lite-preview": "cl100k_base",
    "gemini-1.5-pro": "cl100k_base",
    "deepseek-r1": "cl100k_base",
}

def count_tokens(text: str, model: str = "o3-mini") -> int:
    """
    Count the number of tokens in a text using tiktoken.
    While this uses tiktoken (OpenAI's tokenizer), it provides a good approximation
    for other models as most modern tokenizers are similar in token count.
    """
    try:
        # Try to get model-specific encoding
        encoding_name = MODEL_ENCODINGS.get(model, "cl100k_base")
        encoding = tiktoken.get_encoding(encoding_name)
        return len(encoding.encode(text))
    except KeyError:
        # Fallback to cl100k_base (GPT-4's encoding)
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))

def detect_language(filename: str) -> str:
    """Detect the programming language of a file using Pygments."""
    try:
        lexer = get_lexer_for_filename(filename)
        return lexer.name
    except ClassNotFound:
        return "text"

def truncate_text(text: str, max_tokens: int, model: str = "o3-mini") -> Tuple[str, int]:
    """Truncate text to a maximum number of tokens."""
    encoding_name = MODEL_ENCODINGS.get(model, "cl100k_base")
    encoding = tiktoken.get_encoding(encoding_name)
    tokens = encoding.encode(text)
    if len(tokens) <= max_tokens:
        return text, len(tokens)
    return encoding.decode(tokens[:max_tokens]), max_tokens

def read_file_content(file_path: str, console: Console) -> Tuple[str, str, bool]:
    """
    Read file content with advanced error handling and encoding detection.
    Returns: (content, encoding_used, is_truncated)
    """
    encodings_to_try = [
        'utf-8', 'utf-8-sig',  # UTF-8 with and without BOM
        'iso-8859-1',          # Latin-1
        'cp1252',              # Windows-1252
        'utf-16',              # UTF-16 with BOM
        'ascii'                # ASCII
    ]
    
    content = ""
    encoding_used = ""
    is_binary = False
    
    # First, try to detect if file is binary
    try:
        with open(file_path, 'rb') as file:
            chunk = file.read(1024)
            if b'\x00' in chunk:  # Simple binary check
                is_binary = True
    except Exception as e:
        console.print(f"[yellow]Warning: Could not read file {file_path}: {str(e)}[/yellow]")
        return "", "unknown", False
    
    if is_binary:
        console.print(f"[yellow]Warning: Skipping binary file {file_path}[/yellow]")
        return "", "binary", False
    
    # Try each encoding
    for encoding in encodings_to_try:
        try:
            with codecs.open(file_path, 'r', encoding=encoding) as file:
                content = file.read()
                encoding_used = encoding
                break
        except UnicodeDecodeError:
            continue
        except Exception as e:
            console.print(f"[yellow]Warning: Error reading {file_path} with {encoding}: {str(e)}[/yellow]")
            continue
    
    if not content:
        console.print(f"[yellow]Warning: Could not read {file_path} with any supported encoding[/yellow]")
        return "", "failed", False
    
    # Clean problematic characters
    try:
        # Replace or remove problematic control characters
        content = ''.join(char if ord(char) >= 32 or char in '\n\r\t' else ' ' for char in content)
        # Normalize line endings
        content = content.replace('\r\n', '\n').replace('\r', '\n')
        # Remove zero-width characters
        content = content.replace('\u200b', '').replace('\ufeff', '')
        # Ensure content ends with newline
        if content and not content.endswith('\n'):
            content += '\n'
    except Exception as e:
        console.print(f"[yellow]Warning: Error cleaning content of {file_path}: {str(e)}[/yellow]")
    
    return content, encoding_used, True

def should_ignore_path(path: str, git_spec: Optional[pathspec.PathSpec], ignore_files: List[str]) -> Tuple[bool, str]:
    """
    Check if a path should be ignored based on gitignore patterns and ignore_files.
    Returns: (should_ignore, reason)
    """
    # Check gitignore patterns
    if git_spec and git_spec.match_file(path):
        return True, "matched gitignore pattern"
    
    # Check ignore_files patterns
    if ignore_files:
        ignore_spec = pathspec.PathSpec.from_lines(
            pathspec.patterns.GitWildMatchPattern,
            ignore_files
        )
        if ignore_spec.match_file(path):
            return True, "matched ignore pattern"
    
    return False, ""

def read_gitignore_patterns(codebase_dir: str, custom_gitignore: Optional[str] = None) -> List[str]:
    """Read patterns from .gitignore files and custom gitignore."""
    patterns = []
    
    # First try custom gitignore
    if custom_gitignore and os.path.exists(custom_gitignore):
        try:
            with open(custom_gitignore, 'r', encoding='utf-8') as f:
                patterns.extend([line.strip() for line in f if line.strip() and not line.startswith('#')])
        except Exception as e:
            print(f"Warning: Error reading custom gitignore {custom_gitignore}: {str(e)}")
    
    # Then try project's .gitignore
    gitignore_path = os.path.join(codebase_dir, '.gitignore')
    if os.path.exists(gitignore_path):
        try:
            with open(gitignore_path, 'r', encoding='utf-8') as f:
                patterns.extend([line.strip() for line in f if line.strip() and not line.startswith('#')])
        except Exception as e:
            print(f"Warning: Error reading project gitignore {gitignore_path}: {str(e)}")
    
    return patterns

def get_default_ignore_patterns() -> List[str]:
    """Get comprehensive default ignore patterns."""
    return [
        # .NET specific
        'bin/',
        'obj/',
        '*.dll',
        '*.exe',
        '*.pdb',
        '*.user',
        '*.aps',
        '*.pch',
        '*.vspscc',
        '*.vssscc',
        '*_i.c',
        '*_p.c',
        '*.ncb',
        '*.suo',
        '*.tlb',
        '*.tlh',
        '*.bak',
        '*.cache',
        '*.ilk',
        '*.log',
        '*.lib',
        '*.sbr',
        '.vs/',
        '_ReSharper*/',
        'packages/',
        'artifacts/',
        '**/bin/',
        '**/obj/',
        
        # Version Control
        '.git/',
        '.svn/',
        '.hg/',
        '.gitignore',  # Ignore .gitignore file by default
        
        # IDE
        '.idea/',
        '.vscode/',
        '*.swp',
        '*.swo',
        '*~',
        
        # Build output
        'dist/',
        'build/',
        'out/',
        'Debug/',
        'Release/',
        
        # Package managers
        'node_modules/',
        'jspm_packages/',
        'bower_components/',
        
        # Python
        '__pycache__/',
        '*.py[cod]',
        '*$py.class',
        '*.so',
        '.Python',
        'develop-eggs/',
        'downloads/',
        'eggs/',
        '.eggs/',
        'lib/',
        'lib64/',
        'parts/',
        'sdist/',
        'var/',
        'wheels/',
        '*.egg-info/',
        '.installed.cfg',
        '*.egg',
        'MANIFEST',
        
        # Virtual environments
        'venv/',
        'ENV/',
        'env/',
        '.env/',
        '.venv/',
        
        # Testing
        '.tox/',
        '.coverage',
        '.coverage.*',
        '.cache/',
        'nosetests.xml',
        'coverage.xml',
        '*.cover',
        '.hypothesis/',
        '.pytest_cache/',
        
        # Documentation
        'docs/_build/',
        'docs/build/',
        'site/',
        
        # Logs and databases
        '*.log',
        '*.sqlite',
        '*.sqlite3',
        '*.db',
        'logs/',
        
        # OS generated files
        '.DS_Store',
        '.DS_Store?',
        '._*',
        '.Spotlight-V100',
        '.Trashes',
        'ehthumbs.db',
        'Thumbs.db'
    ]

def process_codebase_to_docs(
    codebase_dir: str,
    output_file: str,
    ignore_dirs: Optional[List[str]] = None,
    ignore_files: Optional[List[str]] = None,
    max_tokens_per_file: int = 1000,
    output_format: str = "markdown",
    model: str = "o3-mini",
    include_metadata: bool = True,
    custom_gitignore: Optional[str] = None,
) -> Dict:
    """
    Process a codebase into documentation format with token counting and metadata.
    Supports both markdown and JSON output formats.
    
    Args:
        codebase_dir: Directory containing the codebase
        output_file: Path to the output file
        ignore_dirs: List of directories to ignore
        ignore_files: List of files to ignore
        max_tokens_per_file: Maximum tokens per file (0 for no limit)
        output_format: Output format ("markdown" or "json")
        model: Model to use for token counting
        include_metadata: Whether to include file metadata
        custom_gitignore: Optional path to a custom .gitignore file
    
    Returns:
        Dict containing statistics about the conversion
    
    Raises:
        ValueError: If the model is not supported
    """
    # Validate model
    if model not in MODEL_CONTEXT_SIZES:
        raise ValueError(f"Unsupported model: {model}. Supported models: {', '.join(MODEL_CONTEXT_SIZES.keys())}")
    
    # Get all ignore patterns
    ignore_dirs = ignore_dirs or []
    ignore_files = ignore_files or []
    console = Console()
    
    # Add default ignore patterns
    default_patterns = get_default_ignore_patterns()
    default_files = [p for p in default_patterns if not p.endswith('/')]
    default_dirs = [p for p in default_patterns if p.endswith('/')]
    
    # Combine default and custom patterns
    ignore_files = default_files + (ignore_files or [])
    ignore_dirs = default_dirs + (ignore_dirs or [])
    
    # Get gitignore patterns
    gitignore_patterns = read_gitignore_patterns(codebase_dir, custom_gitignore)
    
    # Create gitignore spec
    git_spec = None
    if gitignore_patterns:
        git_spec = pathspec.PathSpec.from_lines(
            pathspec.patterns.GitWildMatchPattern,
            gitignore_patterns
        )
    
    # Initialize statistics
    stats = {
        "total_files": 0,
        "total_tokens": 0,
        "total_size_bytes": 0,
        "truncated_files": 0,
        "skipped_files": 0,
        "problematic_files": 0,
        "languages": {},
        "encodings": {},
        "errors": [],
    }
    
    # Collect all files first for progress bar
    all_files = []
    for root, dirs, files in os.walk(codebase_dir):
        # Get paths relative to codebase root for gitignore matching
        rel_root = os.path.relpath(root, codebase_dir)
        
        # Filter directories using both default patterns and gitignore
        filtered_dirs = []
        for d in dirs:
            rel_dir_path = os.path.join(rel_root, d).replace(os.sep, '/')
            
            # Check if directory should be ignored
            should_ignore = False
            
            # Check against ignore_dirs patterns
            if any(rel_dir_path.startswith(p.rstrip('/')) for p in ignore_dirs):
                console.print(f"[yellow]Skipping directory: {rel_dir_path} (matched ignore pattern)[/yellow]")
                should_ignore = True
            
            # Check against gitignore patterns
            elif git_spec and git_spec.match_file(rel_dir_path + '/'):
                console.print(f"[yellow]Skipping directory: {rel_dir_path} (matched gitignore pattern)[/yellow]")
                should_ignore = True
            
            if not should_ignore:
                filtered_dirs.append(d)
        
        # Update dirs in place to skip ignored directories
        dirs[:] = filtered_dirs
        
        # Filter and collect files
        for file in files:
            rel_path = os.path.join(rel_root, file).replace(os.sep, '/')
            file_path = os.path.join(root, file)
            
            # Skip empty files
            try:
                if os.path.getsize(file_path) == 0:
                    continue
            except OSError as e:
                stats["errors"].append(f"Error accessing {file_path}: {str(e)}")
                continue
            
            # Skip output files
            if os.path.basename(file_path).endswith('.md'):
                continue
            
            # Debug: Print file and patterns
            console.print(f"[blue]Checking file: {rel_path}[/blue]")
            console.print(f"[blue]Ignore files: {ignore_files}[/blue]")
            
            # Check if file should be ignored
            should_ignore, reason = should_ignore_path(rel_path, git_spec, ignore_files)
            if should_ignore:
                console.print(f"[yellow]Ignoring {rel_path} ({reason})[/yellow]")
                stats["skipped_files"] += 1
                continue
            
            # Debug: Print accepted file
            console.print(f"[green]Accepting file: {rel_path}[/green]")
            
            # Add file to processing list
            all_files.append((file_path, rel_path))
    
    if output_format == "json":
        output_data = {
            "project_name": os.path.basename(codebase_dir),
            "generated_at": datetime.now().isoformat(),
            "files": []
        }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        if output_format == "markdown":
            # Write header
            f.write(f"# Codebase Documentation: {os.path.basename(codebase_dir)}\n")
            if include_metadata:
                f.write(f"Generated at: {datetime.now().isoformat()}\n")
                f.write(f"Total files: {len(all_files)}\n")
            f.write("\n")
        
        with Progress() as progress:
            task = progress.add_task("[cyan]Processing files...", total=len(all_files))
            
            for file_path, rel_path in all_files:
                try:
                    language = detect_language(file_path)
                    content, encoding_used, success = read_file_content(file_path, console)
                    
                    if not success:
                        stats["skipped_files"] += 1
                        progress.advance(task)
                        continue
                    
                    file_size = len(content.encode('utf-8'))
                    stats["total_size_bytes"] += file_size
                    stats["languages"][language] = stats["languages"].get(language, 0) + 1
                    stats["encodings"][encoding_used] = stats["encodings"].get(encoding_used, 0) + 1
                    
                    # Truncate if needed
                    if max_tokens_per_file > 0:
                        content, token_count = truncate_text(content, max_tokens_per_file, model)
                        if token_count == max_tokens_per_file:
                            stats["truncated_files"] += 1
                    else:
                        token_count = count_tokens(content, model)
                    
                    stats["total_tokens"] += token_count
                    
                    if output_format == "markdown":
                        # Write file section header
                        f.write(f"\n## {rel_path}\n")
                        
                        # Write metadata only if requested
                        if include_metadata:
                            f.write(f"- Language: {language}\n")
                            f.write(f"- Encoding: {encoding_used}\n")
                            f.write(f"- Size: {file_size} bytes\n")
                            f.write(f"- Tokens: {token_count}\n\n")
                        
                        # Write file content with appropriate language tag
                        lang_tag = language.lower() if language != "text" else "text"
                        f.write(f"```{lang_tag}\n{content.strip()}\n```\n")
                    else:  # JSON format
                        output_data["files"].append({
                            "path": rel_path,
                            "language": language,
                            "encoding": encoding_used,
                            "size": file_size,
                            "tokens": token_count,
                            "content": content.strip()
                        })
                    
                    # Increment total files only after successful processing
                    stats["total_files"] += 1
                except Exception as e:
                    error_msg = f"Error processing {rel_path}: {str(e)}"
                    stats["errors"].append(error_msg)
                    stats["problematic_files"] += 1
                    console.print(f"[yellow]Warning: {error_msg}[/yellow]")
                
                progress.advance(task)
        
        if output_format == "json":
            json.dump(output_data, f, indent=2)
    
    return stats

def format_size(size_bytes: int) -> str:
    """Format size in bytes to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

def generate_stats_markdown(stats: Dict, project_dir: str, model: str) -> str:
    """Generate detailed statistics in markdown format."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        f"# Code Tokenizer Analysis Report",
        f"Generated on: {now}",
        "",
        f"## Project Information",
        f"- **Project Directory**: `{project_dir}`",
        f"- **Model Used**: `{model}`",
        "",
        f"## Summary Statistics",
        f"- **Total Files**: {stats['total_files']}",
        f"- **Total Tokens**: {stats['total_tokens']:,}",
        f"- **Total Size**: {format_size(stats['total_size_bytes'])}",
        f"- **Truncated Files**: {stats['truncated_files']}",
        f"- **Skipped Files**: {stats['skipped_files']}",
        f"- **Problematic Files**: {stats['problematic_files']}",
        "",
        "## Language Distribution",
        "| Language | File Count |",
        "|----------|------------|",
    ]
    
    # Add language statistics
    for lang, count in sorted(stats['languages'].items(), key=lambda x: x[1], reverse=True):
        lines.append(f"| {lang} | {count} |")
    
    # Add encoding statistics
    lines.extend([
        "",
        "## Encoding Distribution",
        "| Encoding | File Count |",
        "|----------|------------|",
    ])
    for encoding, count in sorted(stats['encodings'].items(), key=lambda x: x[1], reverse=True):
        lines.append(f"| {encoding} | {count} |")
    
    # Add errors if any
    if stats['errors']:
        lines.extend([
            "",
            "## Processing Errors",
            "The following errors were encountered during processing:",
            "",
        ])
        for error in stats['errors']:
            lines.append(f"- {error}")
    
    return "\n".join(lines)

def write_stats_file(stats: Dict, project_dir: str, model: str, output_file: str):
    """Write detailed statistics to a markdown file."""
    stats_md = generate_stats_markdown(stats, project_dir, model)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(stats_md) 