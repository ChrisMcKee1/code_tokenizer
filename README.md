# 📚 Code Tokenizer

> 🔄 Transform your codebase into LLM-ready tokens with intelligent processing!

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/ChrisMcKee1/code_tokenizer/releases)

[⭐ Star](https://github.com/ChrisMcKee1/code_tokenizer) | 
[🍴 Fork](https://github.com/ChrisMcKee1/code_tokenizer/fork) | 
[🐛 Report Bug](https://github.com/ChrisMcKee1/code_tokenizer/issues/new?template=bug_report.md&title=[BUG]) | 
[✨ Request Feature](https://github.com/ChrisMcKee1/code_tokenizer/issues/new?template=feature_request.md&title=[FEATURE])

</div>

Code Tokenizer helps you prepare your codebase for Large Language Models (LLMs) by intelligently processing and tokenizing your code. Perfect for developers working with AI models like GPT-4, Claude, and Gemini! 🚀

> [!NOTE]
> Code Tokenizer automatically handles encoding detection, language identification, and token counting for all major LLM models. Just point it at your codebase and let it do the work!

## ✨ Why Code Tokenizer?

- 🎯 **Smart Processing**: Automatically detects languages, handles encodings, and respects `.gitignore` rules
- 🤖 **LLM-Ready**: Optimized for popular AI models with accurate token counting
- 📊 **Rich Analysis**: Get detailed stats about your codebase
- 🎨 **Multiple Formats**: Output as Markdown or JSON

## 🚀 Quick Start

### Installation

Choose one of these installation methods:

> [!TIP]
> Method 1 (using pipx) is recommended as it handles all PATH configuration automatically and keeps your Python environment clean!

#### Method 1: Recommended (Using pipx)
```bash
# Install pipx if you haven't already
python -m pip install --user pipx
python -m pipx ensurepath

# Install code-tokenizer globally
pipx install code-tokenizer
```

#### Method 2: Using pip
```bash
# Install with pip (might require PATH configuration)
pip install --user code-tokenizer

# Add to PATH if needed:
# Windows (PowerShell Admin):
[Environment]::SetEnvironmentVariable(
    "Path",
    [Environment]::GetEnvironmentVariable("Path", "User") + ";%APPDATA%\Python\Python313\Scripts",
    "User"
)

# Linux/Mac (add to ~/.bashrc or ~/.zshrc):
export PATH="$HOME/.local/bin:$PATH"
```

### Usage

The `code-tokenizer` command will be available globally after installation:

```bash
# View help and options
code-tokenizer --help

# Basic usage
code-tokenizer -d ./my-project -o ./output

# Use with specific model
code-tokenizer -d ./my-project -o ./output --model claude-3-opus

# Generate JSON output
code-tokenizer -d ./my-project -o ./output --format json
```

> [!IMPORTANT]
> Always ensure you have sufficient token allowance in your target LLM model. Use the `--max-tokens` option to control file splitting and prevent token limit issues.

## 📋 Features

### 🎯 Smart File Processing
- ✓ Automatic language detection
- ✓ Intelligent encoding handling
- ✓ Binary file filtering
- ✓ Full `.gitignore` support

> [!WARNING]
> Large binary files and certain encodings can significantly impact token counts. Use the `--no-metadata` flag if you encounter processing issues with complex files.

### 🤖 LLM Support
- ✓ Token counting for major models
- ✓ Configurable token limits
- ✓ Support for:
  - OpenAI (GPT-4 & variants)
  - Anthropic (Claude 3 family)
  - Google (Gemini models)
  - DeepSeek models

### 📊 Analysis
- ✓ Comprehensive statistics
- ✓ Language distribution
- ✓ Token usage analysis
- ✓ Error reporting

## 💡 Usage Examples

### Basic Analysis
```bash
code-tokenizer -d ./my-project -o ./output
```
Creates:
- `my-project_docs.md`: Code documentation
- `my-project_analysis.md`: Statistical analysis

> [!CAUTION]
> The output directory will be created if it doesn't exist, and existing files will be overwritten. Always verify your output path to avoid data loss.

### Custom Settings
```bash
# Increase token limit
code-tokenizer -d ./my-project -o ./output --max-tokens 5000

# Process all files (bypass .gitignore)
code-tokenizer -d ./my-project -o ./output --bypass-gitignore

# Generate JSON for API use
code-tokenizer -d ./my-project -o ./output --format json
```

> [!TIP]
> Use `--bypass-gitignore` when you need to process all files in a directory, regardless of .gitignore rules.

### Understanding `.gitignore` Behavior

> [!NOTE]
> By default, Code Tokenizer respects your project's existing `.gitignore` file. Use `--bypass-gitignore` to process all files without any ignore rules.

> [!IMPORTANT]
> When using `--bypass-gitignore`, be aware that:
> - All files will be processed, including build artifacts and dependencies
> - Processing time may increase significantly
> - Token counts will include everything in the directory
> - Large binary files and dependencies may cause issues

## 📋 Command Options

| Option | Description | Default |
|--------|-------------|---------|
| `-d, --directory` | Source directory | Required |
| `-o, --output` | Output directory | Required |
| `--model` | LLM model | claude-3-sonnet |
| `--max-tokens` | Tokens per file | 2000 |
| `--format` | Output format | markdown |
| `--bypass-gitignore` | Process all files | False |
| `--no-metadata` | Skip metadata | False |

> [!TIP]
> Use `--format json` when integrating with other tools or APIs. The JSON output includes detailed metadata and is easier to parse programmatically.

## 📦 Output Files

### 📝 Documentation (`*_docs.md/json`)
- Source code with syntax highlighting
- File metadata (optional):
  - Language
  - Encoding
  - Size
  - Token count

### 📊 Analysis (`*_analysis.md`)
- Project summary
- Language stats
- Token distribution
- Processing logs

## 🛠️ Development

```bash
# Clone the repo
git clone https://github.com/ChrisMcKee1/code_tokenizer.git
cd code_tokenizer

# Set up environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dev version
pip install -e .

# Run tests
pytest
```

## 🤝 Contributing

We love contributions! Here's how:

1. 🍴 Fork the repo
2. 🌿 Create a branch (`git checkout -b feature/amazing`)
3. 💾 Commit changes (`git commit -m 'Add amazing feature'`)
4. 📤 Push to branch (`git push origin feature/amazing`)
5. 🎁 Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ❤️ Support

If you find Code Tokenizer helpful:
- ⭐ Star the repository
- 🐛 Report issues
- 🤝 Contribute
- 📢 Share with others

---

<div align="center">

Made with ❤️ by developers, for developers

[⭐ Star Code Tokenizer](https://github.com/ChrisMcKee1/code_tokenizer)

</div>
