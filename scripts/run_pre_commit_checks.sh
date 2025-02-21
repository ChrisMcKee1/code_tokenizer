#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Function to print section headers
print_section() {
    echo -e "\n${BOLD}${YELLOW}=== $1 ===${NC}\n"
}

# Function to check command status
check_status() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ $1 passed${NC}"
        return 0
    else
        echo -e "${RED}✗ $1 failed${NC}"
        return 1
    fi
}

# Initialize error counter
ERRORS=0

# Save current directory
CURRENT_DIR=$(pwd)

print_section "Running Code Formatting Checks"

# Check black formatting
echo "Running black check..."
black --check . || ((ERRORS++))
check_status "Black formatting"

# Check isort
echo -e "\nRunning isort check..."
isort --check-only . || ((ERRORS++))
check_status "Import sorting"

print_section "Running Linting Checks"

# Run flake8
echo "Running flake8..."
flake8 src/ tests/ || ((ERRORS++))
check_status "Flake8 linting"

# Run mypy
echo -e "\nRunning mypy..."
mypy src/ || ((ERRORS++))
check_status "Type checking"

print_section "Running Security Checks"

# Run bandit if installed
if command -v bandit &> /dev/null; then
    echo "Running bandit security check..."
    bandit -r src/ || ((ERRORS++))
    check_status "Security check"
else
    echo -e "${YELLOW}⚠ Bandit not installed. Skipping security check.${NC}"
fi

print_section "Running Tests"

# Run smoke tests
echo "Running smoke tests..."
pytest -v -m "smoke" --cov=code_tokenizer --cov-report=term-missing || ((ERRORS++))
check_status "Smoke tests"

# Run unit tests
echo -e "\nRunning unit tests..."
pytest -v -m "unit" --cov=code_tokenizer --cov-report=term-missing || ((ERRORS++))
check_status "Unit tests"

# Run integration tests
echo -e "\nRunning integration tests..."
pytest -v -m "integration" --cov=code_tokenizer --cov-report=term-missing || ((ERRORS++))
check_status "Integration tests"

# Run performance tests if they exist
echo -e "\nRunning performance tests..."
pytest -v -m "performance" --cov=code_tokenizer --cov-report=term-missing || ((ERRORS++))
check_status "Performance tests"

print_section "Running Build Checks"

# Check if build works
echo "Running build check..."
python -m build || ((ERRORS++))
check_status "Build check"

# Verify package
echo -e "\nVerifying package..."
twine check dist/* || ((ERRORS++))
check_status "Package verification"

print_section "Checking Dependencies"

# Check for outdated dependencies
echo "Checking for outdated dependencies..."
pip list --outdated || true

print_section "Running Coverage Checks"

# Generate coverage report
echo "Generating coverage report..."
coverage combine || true
coverage report || ((ERRORS++))
coverage xml || ((ERRORS++))
check_status "Coverage report generation"

# Check minimum coverage threshold (e.g., 80%)
COVERAGE=$(coverage report | grep "TOTAL" | awk '{print $4}' | sed 's/%//')
if (( $(echo "$COVERAGE < 80" | bc -l) )); then
    echo -e "${RED}✗ Coverage ($COVERAGE%) is below minimum threshold (80%)${NC}"
    ((ERRORS++))
else
    echo -e "${GREEN}✓ Coverage ($COVERAGE%) meets minimum threshold${NC}"
fi

print_section "Final Status"

# Print final status
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}${BOLD}All checks passed successfully! ✨${NC}"
    echo -e "\nSafe to commit! 🚀"
else
    echo -e "${RED}${BOLD}$ERRORS check(s) failed! Please fix the issues before committing.${NC}"
    echo -e "\nCommit blocked! 🛑"
fi

# Return to original directory
cd "$CURRENT_DIR"

# Exit with error if any checks failed
exit $ERRORS 