# 📚 Code Tokenizer

> 🔄 Transform your codebase into LLM-ready tokens with intelligent processing!

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/ChrisMcKee1/code_tokenizer/releases)

<div align="center">

[⭐ Star](https://github.com/ChrisMcKee1/code_tokenizer) | 
[🍴 Fork](https://github.com/ChrisMcKee1/code_tokenizer/fork) 
| 
[🐛 Report Bug](https://github.com/chrismcChrisMcKee1kee/code_tokenizer/issues/new?template=bug_report.md&title=[BUG]) | 
[✨ Request Feature](https://github.com/ChrisMcKee1/code_tokenizer/issues/new?template=feature_request.md&title=[FEATURE])

</div>

If you find Code Tokenizer helpful, please consider:
- ⭐ Starring the repository to show your support
- 🍴 Forking it if you'd like to contribute or create your own version
- 📢 Sharing it with others who might find it useful

## 🌟 Features

- 🎯 **Smart File Processing**
  - Automatic language detection and syntax highlighting
  - Intelligent encoding detection and handling
  - Binary file detection and filtering
  - Support for custom `.gitignore` patterns

- 🤖 **LLM Optimization**
  - Token counting for various AI models
  - Configurable token limits per file
  - Support for major models:
    - OpenAI GPT-4 & variants
    - Anthropic Claude 3 family
    - Google Gemini models
    - DeepSeek models

- 📊 **Rich Metadata**
  - File size and token statistics
  - Language distribution analysis
  - Encoding information
  - Progress tracking with detailed logs

- 🎨 **Multiple Output Formats**
  - Markdown with syntax highlighting
  - JSON for programmatic processing
  - Customizable metadata inclusion

## 🚀 Quick Start

```bash
# Install from PyPI
pip install code-tokenizer

# Basic usage
code-tokenizer -d ./my-project -m output.md

# Use with specific model (e.g., Claude 3 Opus)
code-tokenizer -d ./my-project -m output.md --model claude-3-opus

# Use custom gitignore
code-tokenizer -d ./my-project -m output.md --gitignore ./custom/.gitignore
```

## 💡 Advanced Usage

<details>
<summary>Click to expand advanced options</summary>

### 🎛️ Command Line Options

```bash
code-tokenizer -h
```

| Option | Description | Default |
|--------|-------------|---------|
| `-d, --directory` | Source codebase directory | Required |
| `-m, --markdown` | Output file path | Required |
| `--model` | Target LLM model | gpt-4o |
| `--max-tokens` | Max tokens per file | 1000 |
| `--format` | Output format (markdown/json) | markdown |
| `--gitignore` | Custom .gitignore path | None |
| `--no-metadata` | Exclude file metadata | False |

### 🎯 Supported Models

<details>
<summary>OpenAI Models</summary>

- `gpt-4o` (128K tokens)
- `o1` (200K tokens)
- `o3-mini` (200K tokens)

</details>

<details>
<summary>Anthropic Models</summary>

- `claude-3-opus` (200K tokens)
- `claude-3-sonnet` (200K tokens)
- `claude-3-haiku` (200K tokens)

</details>

<details>
<summary>Google Models</summary>

- `gemini-2.0-flash` (1M tokens)
- `gemini-1.5-pro` (2M tokens)

</details>

</details>

## 📋 Example Output

<details>
<summary>Click to see example output</summary>

```markdown
# Codebase Documentation: my-project
Generated at: 2024-02-17T14:30:00
Total files: 42

## src/main.py (Python, utf-8, 1024 bytes, 256 tokens)

```python
def hello_world():
    print("Hello, World!")
```

## src/utils/helper.ts (TypeScript, utf-8, 512 bytes, 128 tokens)

```typescript
export const formatDate = (date: Date): string => {
    return date.toISOString();
};
```

</details>

## 🛠️ Development

```bash
# Clone the repository
git clone https://github.com/ChrisMcKee1/code_tokenizer.git

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. 🍴 Fork the repository
2. 🌿 Create your feature branch (`git checkout -b feature/amazing-feature`)
3. 💾 Commit your changes (`git commit -m 'Add amazing feature'`)
4. 📤 Push to the branch (`git push origin feature/amazing-feature`)
5. 🎁 Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2024 Chris McKee

The MIT License is a permissive license that is short and to the point. It lets people do anything they want with your code as long as they provide attribution back to you and don't hold you liable.

### What you can do with this project:
- ✅ Commercial use
- ✅ Modify and distribute
- ✅ Private use
- ✅ Sublicense

### What you must do:
- Keep the license and copyright notice included in LICENSE
- Include the same license when distributing

## 🌟 Support the Project

If you find Code Tokenizer useful, there are several ways you can support its development:

1. ⭐ **Star the Repository**: Show your support and help others discover the project
2. 🍴 **Fork & Contribute**: Add features, fix bugs, or improve documentation
3. 🐛 **Report Issues**: Help us improve by reporting bugs or suggesting enhancements
4. 📢 **Spread the Word**: Share your experience with others on social media
5. 💡 **Feature Requests**: Let us know what features would make your work easier

## 🙏 Acknowledgments

- Built with [Rich](https://github.com/Textualize/rich) for beautiful terminal output
- Powered by [Pygments](https://pygments.org/) for syntax highlighting

---

<div align="center">

Made with ❤️ by developers, for developers

⭐ If this tool helped you, please consider giving it a star!

[⭐ Star Code Tokenizer](https://github.com/ChrisMcKee1/code_tokenizer) | 
[🍴 Fork Code Tokenizer](https://github.com/ChrisMcKee1/code_tokenizer/fork) | 
[📝 Create Issue](https://github.com/ChrisMcKee1/code_tokenizer/issues/new/choose)

</div>
