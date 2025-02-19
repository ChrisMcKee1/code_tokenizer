#!/bin/bash
set -e  # Exit on error

echo "🔄 Running CI checks locally..."

# Python Tests
echo "🐍 Running Python tests..."

echo "Running smoke tests..."
pytest -v -m "smoke" --cov=code_tokenizer --cov-report=xml || exit 1

echo "Running unit tests..."
pytest -v -m "unit" --cov=code_tokenizer --cov-report=xml || exit 1

echo "Running integration tests..."
pytest -v -m "integration" --cov=code_tokenizer --cov-report=xml || exit 1

echo "Running performance tests..."
pytest -v -m "performance" --cov=code_tokenizer --cov-report=xml || exit 1

# Node.js Tests
echo "📦 Running Node.js tests..."
npm ci
npm test || exit 1

# Python Linting
echo "🔍 Running Python linting..."
black --check . || exit 1
isort --check-only . || exit 1
mypy src/ || exit 1
flake8 src/ || exit 1

# Build Checks
echo "🏗️ Running build checks..."
python -m build || exit 1
twine check dist/* || exit 1

echo "✅ All CI checks passed!" 