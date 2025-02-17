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

## ✨ Why Code Tokenizer?

- 🎯 **Smart Processing**: Automatically detects languages, handles encodings, and respects `.gitignore` rules
- 🤖 **LLM-Ready**: Optimized for popular AI models with accurate token counting
- 📊 **Rich Analysis**: Get detailed stats about your codebase
- 🎨 **Multiple Formats**: Output as Markdown or JSON

## 🚀 Quick Start

```bash
# Install with pip
pip install code-tokenizer

# Basic usage
code-tokenizer -d ./my-project -o ./output

# Use with specific model
code-tokenizer -d ./my-project -o ./output --model claude-3-opus

# Generate JSON output
code-tokenizer -d ./my-project -o ./output --format json
```

## 📋 Features

### 🎯 Smart File Processing
- ✓ Automatic language detection
- ✓ Intelligent encoding handling
- ✓ Binary file filtering
- ✓ Full `.gitignore` support

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

### Custom Settings
```bash
# Increase token limit
code-tokenizer -d ./my-project -o ./output --max-tokens 5000

# Use custom gitignore
code-tokenizer -d ./my-project -o ./output --gitignore ./custom/.gitignore

# Generate JSON for API use
code-tokenizer -d ./my-project -o ./output --format json
```

## 📋 Command Options

| Option | Description | Default |
|--------|-------------|---------|
| `-d, --directory` | Source directory | Required |
| `-o, --output` | Output directory | Required |
| `--model` | LLM model | claude-3-sonnet |
| `--max-tokens` | Tokens per file | 2000 |
| `--format` | Output format | markdown |
| `--gitignore` | Custom .gitignore | None |
| `--no-metadata` | Skip metadata | False |

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
