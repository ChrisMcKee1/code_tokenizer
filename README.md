# 📚 Code Tokenizer

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/ChrisMcKee1/code_tokenizer/releases)

[⭐ Star](https://github.com/ChrisMcKee1/code_tokenizer) | 
[🍴 Fork](https://github.com/ChrisMcKee1/code_tokenizer/fork) | 
[🐛 Report Bug](https://github.com/ChrisMcKee1/code_tokenizer/issues/new?template=bug_report.md&title=[BUG]) | 
[✨ Request Feature](https://github.com/ChrisMcKee1/code_tokenizer/issues/new?template=feature_request.md&title=[FEATURE])

</div>

## 🔄 Your AI-Powered Code Analysis Companion
> Transform any codebase into LLM-ready tokens!

<div align="center">

### ⚡ One Command = LLM-Ready Code Context

```bash
code-tokenizer -d ./your-project -o ./context.md
```



### 🆚 Manual Copying vs Code Tokenizer

| Without Code Tokenizer | With Code Tokenizer |
|----------------------|-------------------|
| ❌ Manually copy each file | ✅ One command for entire codebase |
| ❌ Hit token limits constantly | ✅ Automatically fits context window |
| ❌ Miss important code context | ✅ Preserves all critical relationships |
| ❌ Include test/build noise | ✅ Smart filtering of irrelevant files |
| ❌ Waste time formatting | ✅ Perfect LLM-ready format instantly |
| ❌ Inconsistent results | ✅ Consistent, reproducible output |

</div>

## 📄 What You Get: Perfect LLM Input

- **A Single Markdown/JSON File**: Contains your entire codebase context, perfectly formatted for any LLM
- **Token-Optimized**: Automatically fits within your LLM's context window (GPT-4, Claude, etc.)
- **Ready to Copy & Paste**: Just copy the output file directly into ChatGPT, Claude, or any other LLM
- **Smart Filtering**: Excludes tests, builds, and other noise that confuses LLMs
- **Context Preservation**: Maintains critical relationships between code components

> [!IMPORTANT]
> Stop wasting time manually copying files or hitting token limits. Get your entire codebase into LLMs instantly!

<details open>
<summary><h3 style="display: inline-block; margin: 0;">👀 Example Output (context.md)</h3></summary>

Here's what you get in your output file:

````
# 📁 Project Overview
Your entire codebase, perfectly formatted for LLMs:

## API Components
```typescript
// UserController.ts
export class UserController {
    async getUser(id: string): Promise<User> {
        // Your actual implementation
    }
}
```

## Business Logic
```typescript
// UserService.ts
export class UserService {
    // Your actual business rules
}
```

## Data Models
```typescript
// User.ts
export interface User {
    id: string;
    // Your actual model
}
```

## 🔗 Relationships
- Controllers → Services → Models
- Security & Auth flows
- Business rules & validation
````

</details>

> [!TIP]
> Just copy the entire contents of context.md and paste into any LLM. No formatting needed!

## 🚀 Installation & Quick Start

<details open>
<summary>📥 Get Started in Seconds</summary>

```bash
# Using pipx (recommended)
pipx install code-tokenizer

# Or using pip
pip install --user code-tokenizer

# Basic usage
code-tokenizer -d ./your-project -o ./context.md
```

</details>

## 🎮 Usage Examples

<details open>
<summary>Powerful Options for Any Workflow</summary>

```bash
# Generate context from your project
code-tokenizer -d ./your-project -o ./context.md

# Export as JSON for automation
code-tokenizer -d ./your-project -o ./context.json --format json

# Generate context with specific LLM token counting
code-tokenizer -d ./src -o ./context.md --model gpt-4o      # OpenAI's gpt-4o
code-tokenizer -d ./src -o ./context.md --model claude-3   # Anthropic's Claude
code-tokenizer -d ./src -o ./context.md --model gemini-pro # Google's Gemini

# Process multiple directories
code-tokenizer -d ./frontend/src -o ./frontend-context.md
code-tokenizer -d ./backend/src -o ./backend-context.md

# Target specific file types
code-tokenizer -d ./src -o ./typescript-context.md --include "*.ts"
code-tokenizer -d ./src -o ./react-context.md --include "*.tsx"

# Exclude specific patterns
code-tokenizer -d . -o ./context.md --exclude "test/**/*"
code-tokenizer -d . -o ./context.md --exclude "*.test.ts"

# Combine multiple options
code-tokenizer -d ./src \
    -o ./context.md \
    --model gpt-4o \
    --include "*.{ts,tsx}" \
    --exclude "test/**/*" \
    --format markdown \
    --max-tokens 4000
```

</details>

## 🎯 Features & Benefits

### 🤖 LLM Integration
- Perfect for copying code directly into ChatGPT, Claude, or other LLMs
- Formats code to fit any LLM's context window
- Optimized for OpenAI's Models (GPT-4o, o1, o3-mini), Anthropic's (Claude 3.5 Sonnet), Google's (Gemini 1.5 Pro), and more!
- Prevents token limit issues automatically
- Manages token counts to stay within model limits

### 🎨 Smart Processing
- Auto-detects programming languages and encodings
- Respects `.gitignore` rules to exclude irrelevant files
- Handles large codebases efficiently

### 📊 Analysis & Export
- Provides detailed codebase statistics
- Exports as Markdown or JSON
- Tracks token usage across your project

## 📋 Command Options

| Option | Description | Default |
|--------|-------------|---------|
| `-d, --directory` | Source directory | Required |
| `-o, --output` | Output file | Required |
| `--model` | LLM model | claude-3-sonnet |
| `--format` | Output format | markdown |
| `--max-tokens` | Token limit per file | 2000 |

## 🎯 Project Examples

<details open>
<summary><h3 style="display: inline-block; margin: 0;">⚛️ Next.js/React Project</h3></summary>

#### 📟 CLI Commands

```bash
# Extract context from frontend codebase
code-tokenizer -d ./nextjs-app/src -o ./context/frontend.md --model claude-3

# Process component directory for LLM
code-tokenizer -d ./nextjs-app/src/components -o ./context/components.md --include "*.tsx"
```

#### 📁 Project Structure

```plaintext
nextjs-app/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components/
│   │   ├── ui/
│   │   └── features/
│   └── lib/
├── public/
├── node_modules/
├── package.json
└── .gitignore  # Critical for excluding node_modules
```

#### 📝 Example .gitignore

```gitignore
# Example .gitignore
node_modules/
.next/
out/
build/
.env*.local
*.log
.DS_Store
```

</details>

<details open>
<summary><h3 style="display: inline-block; margin: 0;">🐍 Python FastAPI Project</h3></summary>

#### 📟 CLI Commands

```bash
# Extract context from API codebase
code-tokenizer -d ./python-api/src -o ./context/api.md --model gpt-4o

# Process route handlers for LLM
code-tokenizer -d ./python-api/src/api/routes -o ./context/routes.md
```

#### 📁 Project Structure

```plaintext
python-api/
├── src/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   └── users.py
│   │   └── middleware/
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   └── models/
│       ├── user.py
│       └── base.py
├── tests/
│   └── api/
├── .env
├── requirements.txt
└── .gitignore  # Important for excluding env files & pycache
```

#### 📝 Example .gitignore

```gitignore
__pycache__/
*.py[cod]
*$py.class
.env
.venv
venv/
.pytest_cache/
.coverage
```

</details>

<details open>
<summary><h3 style="display: inline-block; margin: 0;">🎯 C# API with Blazor</h3></summary>

#### 📟 CLI Commands

```bash
# Extract context from backend codebase
code-tokenizer -d ./dotnet-app/src/Api -o ./context/api.md

# Process Blazor UI components for LLM
code-tokenizer -d ./dotnet-app/src/Client/Pages -o ./context/ui.md

# Extract context from shared models
code-tokenizer -d ./dotnet-app/src/Shared/Models -o ./context/models.md
```

#### 📁 Project Structure

```plaintext
dotnet-app/
├── src/
│   ├── Api/
│   │   ├── Controllers/
│   │   ├── Services/
│   │   └── Program.cs
│   ├── Client/
│   │   ├── Pages/
│   │   └── Shared/
│   └── Shared/
│       └── Models/
├── tests/
├── .gitignore
└── global.json
```

#### 📝 Example .gitignore

```gitignore
bin/
obj/
.vs/
*.user
appsettings.*.json
wwwroot/
node_modules/
```

</details>

## 🔧 Troubleshooting

> [!IMPORTANT]
> Common issues and quick fixes:

- **Command not found**: Restart terminal or use `python -m code_tokenizer`
- **Files skipped**: Check file size (<1MB) and `.gitignore` rules
- **Permission issues**: Ensure write access to output directory
- **Installation problems**: Try using a virtual environment

## 🤝 Contributing

1. Fork the repo
2. Create a branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

Made with ❤️ by developers, for developers

[⭐ Star Code Tokenizer](https://github.com/ChrisMcKee1/code_tokenizer)
</div>

## Development Setup

### Prerequisites
- Python 3.12+
- Node.js 20.x+
- npm 10.x+

### Initial Setup

1. Clone the repository:
```bash
git clone https://github.com/ChrisMcKee1/code_tokenizer.git
cd code_tokenizer
```

2. Set up Python environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
python -m pip install -e ".[dev]"
```

3. Set up Node.js environment:
```bash
npm install
```

### Running Tests Locally

To run all CI checks locally (matches GitHub Actions workflow):

```bash
./scripts/run_ci_checks.sh
```

Or run individual checks:

#### Python Tests
```bash
# Smoke tests
pytest -v -m "smoke" --cov=code_tokenizer --cov-report=xml

# Unit tests
pytest -v -m "unit" --cov=code_tokenizer --cov-report=xml

# Integration tests
pytest -v -m "integration" --cov=code_tokenizer --cov-report=xml

# Performance tests
pytest -v -m "performance" --cov=code_tokenizer --cov-report=xml
```

#### Node.js Tests
```bash
npm test
npm run test:coverage
```

#### Linting
```bash
# Python
black --check .
isort --check-only .
mypy src/
flake8 src/

# TypeScript
npm run lint
npm run type-check
```

#### Build Checks
```bash
python -m build
twine check dist/*
```

### CI/CD Pipeline

Our GitHub Actions workflow runs the following checks:
1. Node.js tests with Jest
2. Python smoke tests
3. Python unit tests
4. Python integration tests
5. Python performance tests
6. Coverage reporting to Codecov
7. Linting (Python and TypeScript)
8. Build verification

All these checks must pass locally before pushing to avoid CI failures.
