"""Language detection service for code files."""

from pygments.lexers import get_lexer_for_filename
from pygments.util import ClassNotFound


class LanguageDetector:
    """Service for detecting programming languages from file names."""

    # Special case mappings for common file types
    SPECIAL_CASES = {
        "dockerfile": "Docker",
        ".gitignore": "text",
        "requirements.txt": "text",
        "readme": "text",
        "license": "text",
        "makefile": "Makefile",
        ".env": "Dotenv",
        "package.json": "JSON",
        "tsconfig.json": "JSON",
        "composer.json": "JSON",
    }

    @classmethod
    def detect_language(cls, filename: str) -> str:
        """
        Detect the programming language of a file using Pygments.

        Args:
            filename: Name of the file to detect language for

        Returns:
            str: Detected language name or 'text' if unknown
        """
        # Convert to lowercase for consistent matching
        filename_lower = filename.lower()

        # Check special cases first
        for pattern, lang in cls.SPECIAL_CASES.items():
            if filename_lower == pattern or filename_lower.endswith("/" + pattern):
                return lang

        try:
            # Use Pygments for language detection
            lexer = get_lexer_for_filename(filename_lower)
            name = lexer.name

            # Normalize text-only file types to just "text"
            if name in ["Text only", "Plain Text"]:
                return "text"

            return name
        except ClassNotFound:
            return "text"
