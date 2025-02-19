@echo off
setlocal EnableDelayedExpansion

:: Colors for output
set "RED=[91m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "NC=[0m"
set "BOLD=[1m"

:: Initialize error counter
set ERRORS=0

:: Function to print section headers
echo.
echo %YELLOW%%BOLD%=== Running Code Formatting Checks ===%NC%
echo.

:: Check black formatting
echo Running black check...
black --check . || set /a ERRORS+=1
if !ERRORLEVEL! EQU 0 (
    echo %GREEN%✓ Black formatting passed%NC%
) else (
    echo %RED%✗ Black formatting failed%NC%
)

:: Check isort
echo.
echo Running isort check...
isort --check-only . || set /a ERRORS+=1
if !ERRORLEVEL! EQU 0 (
    echo %GREEN%✓ Import sorting passed%NC%
) else (
    echo %RED%✗ Import sorting failed%NC%
)

echo.
echo %YELLOW%%BOLD%=== Running Linting Checks ===%NC%
echo.

:: Run flake8
echo Running flake8...
flake8 src/ tests/ || set /a ERRORS+=1
if !ERRORLEVEL! EQU 0 (
    echo %GREEN%✓ Flake8 linting passed%NC%
) else (
    echo %RED%✗ Flake8 linting failed%NC%
)

:: Run mypy
echo.
echo Running mypy...
mypy src/ || set /a ERRORS+=1
if !ERRORLEVEL! EQU 0 (
    echo %GREEN%✓ Type checking passed%NC%
) else (
    echo %RED%✗ Type checking failed%NC%
)

echo.
echo %YELLOW%%BOLD%=== Running Tests ===%NC%
echo.

:: Run smoke tests
echo Running smoke tests...
pytest -v -m "smoke" --cov=code_tokenizer --cov-report=term-missing || set /a ERRORS+=1
if !ERRORLEVEL! EQU 0 (
    echo %GREEN%✓ Smoke tests passed%NC%
) else (
    echo %RED%✗ Smoke tests failed%NC%
)

:: Run unit tests
echo.
echo Running unit tests...
pytest -v -m "unit" --cov=code_tokenizer --cov-report=term-missing || set /a ERRORS+=1
if !ERRORLEVEL! EQU 0 (
    echo %GREEN%✓ Unit tests passed%NC%
) else (
    echo %RED%✗ Unit tests failed%NC%
)

:: Run integration tests
echo.
echo Running integration tests...
pytest -v -m "integration" --cov=code_tokenizer --cov-report=term-missing || set /a ERRORS+=1
if !ERRORLEVEL! EQU 0 (
    echo %GREEN%✓ Integration tests passed%NC%
) else (
    echo %RED%✗ Integration tests failed%NC%
)

:: Run performance tests
echo.
echo Running performance tests...
pytest -v -m "performance" --cov=code_tokenizer --cov-report=term-missing || set /a ERRORS+=1
if !ERRORLEVEL! EQU 0 (
    echo %GREEN%✓ Performance tests passed%NC%
) else (
    echo %RED%✗ Performance tests failed%NC%
)

echo.
echo %YELLOW%%BOLD%=== Running Build Checks ===%NC%
echo.

:: Check if build works
echo Running build check...
python -m build || set /a ERRORS+=1
if !ERRORLEVEL! EQU 0 (
    echo %GREEN%✓ Build check passed%NC%
) else (
    echo %RED%✗ Build check failed%NC%
)

:: Verify package
echo.
echo Verifying package...
twine check dist/* || set /a ERRORS+=1
if !ERRORLEVEL! EQU 0 (
    echo %GREEN%✓ Package verification passed%NC%
) else (
    echo %RED%✗ Package verification failed%NC%
)

echo.
echo %YELLOW%%BOLD%=== Checking Dependencies ===%NC%
echo.

:: Check for outdated dependencies
echo Checking for outdated dependencies...
pip list --outdated

echo.
echo %YELLOW%%BOLD%=== Running Coverage Checks ===%NC%
echo.

:: Generate coverage report
echo Generating coverage report...
coverage combine
coverage report || set /a ERRORS+=1
coverage xml || set /a ERRORS+=1
if !ERRORLEVEL! EQU 0 (
    echo %GREEN%✓ Coverage report generation passed%NC%
) else (
    echo %RED%✗ Coverage report generation failed%NC%
)

:: Check minimum coverage threshold
for /f "tokens=4" %%i in ('coverage report ^| findstr "TOTAL"') do set COVERAGE=%%i
set COVERAGE=%COVERAGE:~0,-1%
if %COVERAGE% LSS 80 (
    echo %RED%✗ Coverage (%COVERAGE%%%) is below minimum threshold (80%%)%NC%
    set /a ERRORS+=1
) else (
    echo %GREEN%✓ Coverage (%COVERAGE%%%) meets minimum threshold%NC%
)

echo.
echo %YELLOW%%BOLD%=== Final Status ===%NC%
echo.

:: Print final status
if %ERRORS% EQU 0 (
    echo %GREEN%%BOLD%All checks passed successfully! ✨%NC%
    echo.
    echo Safe to commit! 🚀
) else (
    echo %RED%%BOLD%%ERRORS% check(s) failed! Please fix the issues before committing.%NC%
    echo.
    echo Commit blocked! 🛑
)

exit /b %ERRORS% 