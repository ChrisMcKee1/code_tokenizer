"""Language detection for code files."""

import json
import re
from json.decoder import JSONDecodeError
from typing import Dict, List, Optional, Pattern

from pygments.lexers import guess_lexer_for_filename
from pygments.util import ClassNotFound

# Language detection patterns
LANGUAGE_PATTERNS: Dict[str, List[Pattern[str]]] = {
    "JavaScript": [
        re.compile(r"(const|let|var)\s+\w+\s*="),
        re.compile(r"function\s+\w+\s*\("),
        re.compile(r"class\s+\w+\s+(extends\s+\w+\s*)?{"),
        re.compile(r"import\s+.*\s+from\s+['\"]"),
        re.compile(r"export\s+(default\s+)?(function|class|const|let|var)"),
        re.compile(r"=>\s*{"),
        re.compile(r"async\s+function"),
        re.compile(r"React\.(Component|createClass|memo|useState|useEffect)"),
    ],
    "Python": [
        re.compile(r"def\s+\w+\s*\("),
        re.compile(r"class\s+\w+\s*(\(.*\))?\s*:"),
        re.compile(r"import\s+\w+"),
        re.compile(r"from\s+\w+\s+import"),
        re.compile(r"@\w+"),
        re.compile(r"print\s*\("),
        re.compile(r"if\s+__name__\s*==\s*['\"]__main__['\"]"),
    ],
    "HTML": [
        re.compile(r"<(!DOCTYPE\s+)?html.*?>"),
        re.compile(r"<(head|body|div|span|p|a|script|style|link|meta)[\s>]"),
        re.compile(r"</\w+>"),
    ],
    "CSS": [
        re.compile(r"[\.\#]?\w+\s*{[^}]*}"),
        re.compile(r"@media\s+"),
        re.compile(r"@import\s+url\("),
        re.compile(r"@keyframes"),
    ],
}

# File extension to language mapping
EXTENSION_LANGUAGE_MAP = {
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".py": "Python",
    ".html": "HTML",
    ".htm": "HTML",
    ".css": "CSS",
    ".scss": "SCSS",
    ".sass": "SASS",
    ".less": "LESS",
    ".md": "Markdown",
    ".markdown": "Markdown",
    ".json": "JSON",
    ".xml": "XML",
    ".yaml": "YAML",
    ".yml": "YAML",
    ".sh": "Shell",
    ".bash": "Shell",
    ".zsh": "Shell",
    ".sql": "SQL",
    ".php": "PHP",
    ".rb": "Ruby",
    ".rs": "Rust",
    ".go": "Go",
    ".java": "Java",
    ".kt": "Kotlin",
    ".swift": "Swift",
    ".c": "C",
    ".cpp": "C++",
    ".cs": "C#",
    ".fs": "F#",
    ".r": "R",
    ".m": "MATLAB",
    ".pl": "Perl",
    ".lua": "Lua",
    ".ex": "Elixir",
    ".exs": "Elixir",
    ".erl": "Erlang",
    ".hs": "Haskell",
    ".scala": "Scala",
    ".dart": "Dart",
    ".jl": "Julia",
}


class LanguageDetector:
    """Detects programming languages in code files."""

    def __init__(self) -> None:
        """Initialize the language detector."""
        self.patterns = {
            "Python": [
                r"^def\s+\w+\s*\([^)]*\)\s*:",
                r"^class\s+\w+(\s*\([^)]*\))?\s*:",
                r"^import\s+\w+",
                r"^from\s+[\w.]+\s+import",
                r"@\w+(\s*\([^)]*\))?\s*$",
            ],
            "JavaScript": [
                r"^function\s+\w+\s*\([^)]*\)\s*{",
                r"^class\s+\w+\s*{",
                r"^const\s+\w+\s*=",
                r"^let\s+\w+\s*=",
                r"^var\s+\w+\s*=",
                r"^import\s+.*from\s+['\"]",
                r"^export\s+",
                r"=>\s*{",
            ],
            "HTML": [
                r"<!DOCTYPE\s+html",
                r"<html",
                r"<head",
                r"<body",
                r"<script",
                r"<style",
                r"<div",
                r"<p>",
            ],
            "CSS": [
                r"^[\w.-]+\s*{",
                r"@media\s+",
                r"@import\s+",
                r"@keyframes\s+",
            ],
        }

    def detect_language(self, content: Optional[str], filename: Optional[str] = None) -> str:
        """Detect the programming language of a file.

        Args:
            content: File content
            filename: Optional filename to help with detection

        Returns:
            str: Detected language name
        """
        if not content or (isinstance(content, str) and content.isspace()):
            return "Text"

        # Try extension-based detection first if filename is provided
        if filename and filename.strip():
            ext = self._get_file_extension(filename)
            if ext in EXTENSION_LANGUAGE_MAP:
                # For Python files, verify with content patterns
                if EXTENSION_LANGUAGE_MAP[ext] == "Python" and content.strip():
                    for pattern in LANGUAGE_PATTERNS["Python"]:
                        if pattern.search(content):
                            return "Python"
                return EXTENSION_LANGUAGE_MAP[ext] if content.strip() else "Text"

        # Try pattern-based detection
        language = self._detect_by_simple_indicators(content)
        if language and language != "Unknown":
            return language

        # Try lexer-based detection with filename hint
        try:
            if filename and filename.strip():
                lexer = guess_lexer_for_filename(filename, content)
                return self.normalize_language_name(lexer.name)
        except ClassNotFound:
            pass

        # Try JSON detection
        try:
            json.loads(content)
            return "JSON"
        except (JSONDecodeError, TypeError):
            pass

        # Return Text for unrecognized content
        return "Text"

    def _get_file_extension(self, filename: str) -> str:
        """Get the file extension from a filename.

        Args:
            filename: The filename to get the extension from

        Returns:
            str: The file extension (including the dot)
        """
        return filename[filename.rfind(".") :].lower() if "." in filename else ""

    def _detect_by_simple_indicators(self, content: str) -> str:
        """Detect language using simple content indicators.

        Args:
            content: The code content to analyze

        Returns:
            str: Detected language name
        """
        # Check for empty or whitespace-only content
        if not content or content.isspace():
            return "Text"

        # Check for JSON
        if content.strip().startswith("{") and content.strip().endswith("}"):
            try:
                json.loads(content)
                return "JSON"
            except json.JSONDecodeError:
                return None

        # Check for HTML
        if "<!DOCTYPE html" in content.lower() or "<html" in content.lower():
            return "HTML"

        # Check for CSS
        if re.search(r"[^{]*\s*{\s*[^}]*}", content):
            css_indicators = ["margin", "padding", "color", "background"]
            if any(indicator in content.lower() for indicator in css_indicators):
                return "CSS"

        # Return Unknown for unrecognized content
        return "Unknown"

    def _resolve_language_conflicts(self, candidates: List[str], content: str) -> str:
        """Resolve conflicts between multiple language candidates.

        Args:
            candidates: List of potential language matches
            content: The code content to analyze

        Returns:
            str: Most likely language
        """
        # If HTML is one of the candidates, check for specific indicators
        if "HTML" in candidates:
            if "<html" in content.lower() or "<!doctype html" in content.lower():
                return "HTML"

        # If JavaScript and Python are both candidates, look for specific features
        if "JavaScript" in candidates and "Python" in candidates:
            js_features = ["function", "var ", "let ", "const ", "=>", "};"]
            py_features = ["def ", "class ", "import ", "from ", ":"]

            js_score = sum(1 for feature in js_features if feature in content)
            py_score = sum(1 for feature in py_features if feature in content)

            return "JavaScript" if js_score > py_score else "Python"

        # Default to the first candidate
        return candidates[0] if candidates else "Unknown"

    def normalize_language_name(self, language: str) -> str:
        """Normalize language names to a standard format.

        Args:
            language: Language name to normalize

        Returns:
            str: Normalized language name
        """
        language = language.lower()

        # Common language name mappings
        mappings = {
            "python": "Python",
            "py": "Python",
            "javascript": "JavaScript",
            "js": "JavaScript",
            "typescript": "TypeScript",
            "ts": "TypeScript",
            "html": "HTML",
            "css": "CSS",
            "json": "JSON",
            "markdown": "Markdown",
            "md": "Markdown",
            "shell": "Shell",
            "bash": "Shell",
            "dockerfile": "Dockerfile",
            "yaml": "YAML",
            "yml": "YAML",
            "sql": "SQL",
            "text": "Text",
            "plain text": "Text",
        }

        # Try direct mapping
        if language in mappings:
            return mappings[language]

        # Handle variations
        if "python" in language:
            return "Python"
        if "javascript" in language or "js" in language:
            return "JavaScript"
        if "typescript" in language or "ts" in language:
            return "TypeScript"
        if "html" in language:
            return "HTML"
        if "css" in language or "stylesheet" in language:
            return "CSS"
        if "json" in language:
            return "JSON"
        if "markdown" in language or "md" in language:
            return "Markdown"
        if "shell" in language or "bash" in language:
            return "Shell"
        if "docker" in language:
            return "Dockerfile"
        if "yaml" in language or "yml" in language:
            return "YAML"
        if "sql" in language:
            return "SQL"

        # Default to original name if no mapping found
        return language.capitalize()


def get_language_by_extension(ext: str) -> str:
    """Get language name from file extension.

    Args:
        ext: File extension (without dot)

    Returns:
        str: Language name
    """
    ext = ext.lower()

    # Extension to language mappings
    mappings = {
        # Python
        "py": "Python",
        "pyi": "Python",
        "pyx": "Python",
        "pxd": "Python",
        # JavaScript
        "js": "JavaScript",
        "jsx": "JavaScript",
        "mjs": "JavaScript",
        # TypeScript
        "ts": "TypeScript",
        "tsx": "TypeScript",
        # Web
        "html": "HTML",
        "htm": "HTML",
        "css": "CSS",
        "scss": "SCSS",
        "sass": "Sass",
        "less": "Less",
        # Data formats
        "json": "JSON",
        "yaml": "YAML",
        "yml": "YAML",
        "xml": "XML",
        "toml": "TOML",
        # Documentation
        "md": "Markdown",
        "markdown": "Markdown",
        "rst": "reStructuredText",
        "txt": "Text",
        # Shell scripts
        "sh": "Shell",
        "bash": "Shell",
        "zsh": "Shell",
        "fish": "Shell",
        # Configuration
        "ini": "INI",
        "cfg": "INI",
        "conf": "INI",
        "dockerfile": "Dockerfile",
        # Database
        "sql": "SQL",
        "mysql": "SQL",
        "pgsql": "SQL",
        # Other
        "c": "C",
        "cpp": "C++",
        "cs": "C#",
        "java": "Java",
        "go": "Go",
        "rs": "Rust",
        "rb": "Ruby",
        "php": "PHP",
        "swift": "Swift",
        "kt": "Kotlin",
        "scala": "Scala",
        "r": "R",
        "lua": "Lua",
        "pl": "Perl",
        "ex": "Elixir",
        "exs": "Elixir",
        "erl": "Erlang",
        "hs": "Haskell",
    }

    return mappings.get(ext, "Unknown")


def detect_language(content: str, filename: Optional[str] = None) -> str:
    """Detect the programming language of code content.

    Args:
        content: The code content to analyze
        filename: Optional filename to help with detection

    Returns:
        str: Detected language name
    """
    detector = LanguageDetector()
    result = detector.detect_language(content, filename)
    return "Text" if result == "Text only" else result


def detect_language_by_patterns(content: str, filename: Optional[str] = None) -> str:
    """Detect language using pattern matching.

    Args:
        content: The code content to analyze
        filename: Optional filename to help with detection

    Returns:
        str: Detected language name
    """
    # Try to detect by filename first
    if filename:
        try:
            lexer = guess_lexer_for_filename(filename, content)
            return lexer.name
        except ClassNotFound:
            pass

    # Common language patterns
    patterns = {
        "Python": [
            (r"def\s+\w+\s*\([^)]*\)\s*:", 3),
            (r"class\s+\w+(\s*\([^)]*\))?\s*:", 3),
            (r"import\s+[\w.]+", 2),
            (r"from\s+[\w.]+\s+import", 2),
        ],
        "JavaScript": [
            (r"function\s+\w+\s*\([^)]*\)\s*{", 3),
            (r"class\s+\w+\s*{", 3),
            (r"const\s+\w+\s*=", 2),
            (r"let\s+\w+\s*=", 2),
            (r"var\s+\w+\s*=", 2),
            (r'import\s+.*from\s+[\'"]', 2),
        ],
        "HTML": [
            (r"<!DOCTYPE\s+html", 3),
            (r"<html", 2),
            (r"<head", 1),
            (r"<body", 1),
        ],
        "CSS": [
            (r"[\w-]+\s*{\s*[\w-]+\s*:", 3),
            (r"@media\s+", 2),
            (r"@import\s+", 2),
            (r"@keyframes\s+", 2),
        ],
    }

    scores = {lang: 0 for lang in patterns}

    for lang, pattern_list in patterns.items():
        for pattern, weight in pattern_list:
            if re.search(pattern, content, re.MULTILINE):
                scores[lang] += weight

    max_score = max(scores.values())
    if max_score > 0:
        for lang, score in scores.items():
            if score == max_score:
                return lang

    return "Text"
