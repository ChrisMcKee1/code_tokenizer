import os
import codecs
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Union
import tiktoken
from pygments.lexers import get_lexer_for_filename
from pygments.util import ClassNotFound
from rich.console import Console
from rich.progress import Progressimport pathspec  # Add this import for gitignore pattern matching

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

# Model descriptions for better help output
MODEL_DESCRIPTIONS = {
    # OpenAI Models
    "gpt-4o": "GPT-4 Turbo",
    "gpt-4o-mini": "GPT-4 Turbo Mini",
    "o1": "GPT-4 Turbo",
    "o1-mini": "GPT-4 Turbo Mini",
    "o3-mini": "GPT-4 Turbo Mini",
    "o1-preview": "GPT-4 Turbo Preview",
    
    # Anthropic Models
    "claude-3-opus": "Most capable Claude model, highest quality",
    "claude-3-sonnet": "Balanced performance and speed",
    "claude-3-haiku": "Fast and efficient, shorter responses",
    
    # Google Models
    "gemini-2.0-flash": "Fastest Gemini model with 1M token context",
    "gemini-2.0-flash-lite-preview": "Preview of lightweight Gemini 2.0 Flash",
    "gemini-1.5-pro": "Most powerful Gemini model with 2M token context",
    
    # DeepSeek Models
    "deepseek-r1": "DeepSeek's latest model with 128K context",
}

def get_model_context_size(model: str) -> int:
    """Get the context window size for a given model."""
    return MODEL_CONTEXT_SIZES.get(model, 8192)  # Default to 8K if model not found

def get_model_description(model: str) -> str:
    """Get a human-readable description of the model."""
    return MODEL_DESCRIPTIONS.get(model, model)

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

def read_gitignore(codebase_dir: str, custom_gitignore: Optional[str] = None) -> List[str]:
    """
    Read .gitignore file and return list of patterns.
    Handles multiple .gitignore files in subdirectories and custom gitignore path.
    
    Args:
        codebase_dir: Base directory of the codebase
        custom_gitignore: Optional path to a custom .gitignore file
    
    Returns:
        List of gitignore patterns
    """
    gitignore_patterns = []
    
    # First read custom gitignore if provided
    if custom_gitignore:
        try:
            with open(custom_gitignore, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # Normalize directory separators
                        line = line.replace(os.sep, '/')
                        gitignore_patterns.append(line)
        except Exception as e:
            print(f"Warning: Error reading custom gitignore {custom_gitignore}: {str(e)}")
    
    # Then read .gitignore files from the codebase
    for root, _, files in os.walk(codebase_dir):
        if '.gitignore' in files:
            gitignore_path = os.path.join(root, '.gitignore')
            try:
                with open(gitignore_path, 'r', encoding='utf-8') as f:
                    # Get relative path for nested .gitignore files
                    rel_root = os.path.relpath(root, codebase_dir)
                    
                    for line in f:
                        line = line.strip()
                        
                        # Skip empty lines and comments
                        if not line or line.startswith('#'):
                            continue
                            
                        # Handle negation patterns (starting with !)
                        is_negation = line.startswith('!')
                        if is_negation:
                            line = line[1:].strip()
                            
                        # Handle root directory patterns (starting with /)
                        is_root = line.startswith('/')
                        if is_root:
                            line = line[1:]
                            
                        # If it's a nested .gitignore, prefix patterns with the relative path
                        # unless it's a root pattern (starting with /)
                        if rel_root != '.' and not is_root:
                            line = os.path.join(rel_root, line)
                            
                        # Restore negation if present
                        if is_negation:
                            line = '!' + line
                            
                        # Normalize directory separators
                        line = line.replace(os.sep, '/')
                        
                        gitignore_patterns.append(line)
                        
            except Exception as e:
                print(f"Warning: Error reading {gitignore_path}: {str(e)}")
    
    return gitignore_patterns

def should_ignore_path(path: str, git_spec: Optional[pathspec.PathSpec], ignore_patterns: List[str]) -> Tuple[bool, str]:
    """
    Determine if a path should be ignored based on gitignore patterns and default ignore patterns.
    
    Args:
        path: The path to check
        git_spec: The gitignore spec from pathspec
        ignore_patterns: List of default ignore patterns
    
    Returns:
        Tuple of (should_ignore: bool, reason: str)
    """
    # Normalize path separators
    path = path.replace(os.sep, '/')
    
    # Check default ignore patterns first
    for pattern in ignore_patterns:
        # Handle different pattern types
        if pattern.endswith('/'):  # Directory pattern
            if path.startswith(pattern) or f"/{pattern}" in path:
                return True, f"matches directory pattern: {pattern}"
        elif pattern.startswith('**/'):  # Recursive pattern
            if path.endswith(pattern[3:]):
                return True, f"matches recursive pattern: {pattern}"
        elif '*' in pattern:  # Wildcard pattern
            import fnmatch
            if fnmatch.fnmatch(path, pattern):
                return True, f"matches wildcard pattern: {pattern}"
        else:  # Exact match
            if pattern in path:
                return True, f"matches exact pattern: {pattern}"
    
    # Check gitignore patterns
    if git_spec and git_spec.match_file(path):
        return True, "matches gitignore pattern"
    
    return False, ""

def convert_codebase_to_markdown(
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
    Convert a codebase to an LLM-friendly format with token counting and metadata.
    
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
    """
    ignore_dirs = ignore_dirs or []
    ignore_files = ignore_files or []
    console = Console()
    
    # Read .gitignore patterns
    gitignore_patterns = read_gitignore(codebase_dir, custom_gitignore)
    if gitignore_patterns:
        console.print(f"[green]Found {len(gitignore_patterns)} patterns in .gitignore file(s):[/green]")
        for pattern in gitignore_patterns:
            console.print(f"[blue]  - {pattern}[/blue]")
    
    # Create gitignore spec
    if gitignore_patterns:
        git_spec = pathspec.PathSpec.from_lines(
            pathspec.patterns.GitWildMatchPattern,
            gitignore_patterns
        )
    else:
        git_spec = None
    
    # Add default ignored directories and patterns
    default_ignore = [
        # Version Control
        '.git', '.svn', '.hg',
        
        # Package Managers
        'node_modules', 'bower_components', 'jspm_packages',
        'vendor', 'packages', 'composer',
        
        # Python
        '__pycache__', '*.pyc', '*.pyo', '*.pyd', '.Python',
        'env', 'venv', '.env', '.venv',
        'pip-log.txt', 'pip-delete-this-directory.txt',
        '.tox', '.coverage', '.coverage.*', '.cache',
        'nosetests.xml', 'coverage.xml', '*.cover',
        '.pytest_cache', '.mypy_cache', '.ruff_cache',
        
        # Build and Dist
        'dist', 'build', 'bin', 'obj',
        'Release', 'Debug', 'x64', 'x86',
        'target', 'out', 'output',
        '.nuget', 'packages',
        
        # IDE and Editor
        '.vscode', '.idea', '.vs',
        '*.swp', '*.swo', '*~',
        '.project', '.classpath', '.settings',
        
        # JavaScript/TypeScript Build
        '*.js.map', '*.css.map',
        '*.min.js', '*.min.css',
        'bundle.js', '*.bundle.js',
        '.next', '.nuxt',
        'public/build', 'public/dist',
        'static/build', 'static/dist',
        
        # Mobile Development
        'Pods', '.gradle',
        'platforms', 'plugins',
        'www/build', 'www/dist',
        
        # Docker
        '.docker', 'docker-compose*.yml',
        
        # Logs and Databases
        'logs', '*.log',
        '*.sqlite', '*.sqlite3',
        '*.db', '*.sql'
    ]
    ignore_dirs.extend(default_ignore)
    
    # Add default ignored file patterns
    default_ignore_files = [
        # Compiled Code
        '*.dll', '*.so', '*.dylib',
        '*.exe', '*.out', '*.app',
        '*.class', '*.jar', '*.war',
        '*.o', '*.obj', '*.lib',
        '*.a', '*.la', '*.lo',
        
        # Generated JavaScript (but keep config files)
        '**/dist/**/*.js', '**/build/**/*.js',  # Only ignore JS in build/dist
        '*.js.map',
        '*.min.js', '*.min.css',
        'bundle*.js', 'vendor*.js',
        
        # Generated CSS (but keep source files)
        '**/dist/**/*.css', '**/build/**/*.css',  # Only ignore CSS in build/dist
        '*.min.css', '*.css.map',
        
        # Package Files
        '*.zip', '*.tar.gz', '*.tgz',
        '*.rar', '*.7z', '*.gz',
        
        # System Files
        '.DS_Store', 'Thumbs.db',
        '*.pid', '*.seed',
        
        # Config and Lock Files
        'package-lock.json', 'yarn.lock',
        'composer.lock', 'Gemfile.lock',
        '.env.*', '*.env',
        
        # Documentation and Reports
        '*.pdf', '*.doc', '*.docx',
        '*.xls', '*.xlsx',
        '*.coverage', 'coverage.*',
        
        # Media Files
        '*.jpg', '*.jpeg', '*.png',
        '*.gif', '*.ico', '*.svg',
        '*.mp3', '*.mp4', '*.wav',
        '*.ttf', '*.eot', '*.woff',
        
        # Binary Data
        '*.bin', '*.dat', '*.bak',
        '*.swp', '*.swo', '*~'
    ]
    ignore_files.extend(default_ignore_files)
    
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
        "gitignore_patterns": len(gitignore_patterns) if gitignore_patterns else 0
    }
    
    # Collect all files first for progress bar
    all_files = []
    for root, dirs, files in os.walk(codebase_dir):
        # Get paths relative to codebase root for gitignore matching
        rel_root = os.path.relpath(root, codebase_dir)
        
        # Filter directories using both default patterns and gitignore
        if git_spec:
            dirs[:] = [d for d in dirs 
                      if d not in ignore_dirs 
                      and not any(d.startswith(p) for p in ignore_dirs)
                      and not git_spec.match_file(os.path.join(rel_root, d))]
        else:
            dirs[:] = [d for d in dirs 
                      if d not in ignore_dirs 
                      and not any(d.startswith(p) for p in ignore_dirs)]
        
        # Filter and collect files using both default patterns and gitignore
        for file in files:
            rel_path = os.path.join(rel_root, file).replace(os.sep, '/')
            
            # Check if file should be ignored
            should_ignore, reason = should_ignore_path(rel_path, git_spec, ignore_files)
            if should_ignore:
                console.print(f"[yellow]Ignoring {rel_path} ({reason})[/yellow]")
                continue
            
            file_path = os.path.join(root, file)
            try:
                if os.path.getsize(file_path) > 0:  # Skip empty files
                    all_files.append(file_path)
                    console.print(f"[green]Including {rel_path}[/green]")
            except OSError as e:
                stats["errors"].append(f"Error accessing {file_path}: {str(e)}")
                continue
    
    if output_format == "json":
        output_data = {
            "project_name": os.path.basename(codebase_dir),
            "generated_at": datetime.now().isoformat(),
            "files": []
        }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        if output_format == "markdown":
            f.write(f"# Codebase Documentation: {os.path.basename(codebase_dir)}\n")
            if include_metadata:
                f.write(f"Generated at: {datetime.now().isoformat()}\n")
                f.write(f"Total files: {len(all_files)}\n")
        
        with Progress() as progress:
            task = progress.add_task("[cyan]Processing files...", total=len(all_files))
            
            for file_path in all_files:
                rel_path = os.path.relpath(file_path, codebase_dir)
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
                    stats["total_files"] += 1
                    
                    if output_format == "markdown":
                        # Write file header with metadata
                        f.write(f"\n## {rel_path}")
                        if include_metadata:
                            f.write(f" ({language}, {encoding_used}, {file_size} bytes, {token_count} tokens)\n")
                        else:
                            f.write("\n")
                        
                        # Write file content with appropriate language tag
                        lang_tag = language.lower() if language != "text" else "text"
                        f.write(f"```{lang_tag}\n{content.strip()}\n```\n")
                    else:  # JSON format
                        output_data["files"].append({
                            "path": rel_path,
                            "language": language,
                            "encoding": encoding_used,
                            "size_bytes": file_size,
                            "tokens": token_count,
                            "content": content
                        })
                except Exception as e:
                    error_msg = f"Error processing {rel_path}: {str(e)}"
                    stats["errors"].append(error_msg)
                    stats["problematic_files"] += 1
                    console.print(f"[yellow]Warning: {error_msg}[/yellow]")
                
                progress.advance(task)
        
        if output_format == "json":
            json.dump(output_data, f, indent=2)
    
    return stats 