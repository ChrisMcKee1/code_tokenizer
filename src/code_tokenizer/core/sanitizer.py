"""Content sanitization for code files."""

import re
from typing import Dict, List, Optional, Pattern, Tuple

from ..core.tokenizer import CodeTokenizer

# Language-specific comment patterns
COMMENT_PATTERNS: Dict[str, List[Pattern[str]]] = {
    "Python": [
        re.compile(r"#.*$", re.MULTILINE),  # Single line comments
        re.compile(r'"""[\s\S]*?"""'),  # Triple quote docstrings
        re.compile(r"'''[\s\S]*?'''"),  # Triple quote docstrings
    ],
    "JavaScript": [
        re.compile(r"//.*$", re.MULTILINE),  # Single line comments
        re.compile(r"/\*[\s\S]*?\*/"),  # Multi-line comments
    ],
    "TypeScript": [
        re.compile(r"//.*$", re.MULTILINE),  # Single line comments
        re.compile(r"/\*[\s\S]*?\*/"),  # Multi-line comments
    ],
    "HTML": [
        re.compile(r"<!--[\s\S]*?-->"),  # HTML comments
    ],
    "CSS": [
        re.compile(r"/\*[\s\S]*?\*/"),  # CSS comments
    ],
    "Java": [
        re.compile(r"//.*$", re.MULTILINE),  # Single line comments
        re.compile(r"/\*[\s\S]*?\*/"),  # Multi-line comments
        re.compile(r"/\*\*[\s\S]*?\*/"),  # JavaDoc comments
    ],
    "C#": [
        re.compile(r"//.*$", re.MULTILINE),  # Single line comments
        re.compile(r"/\*[\s\S]*?\*/"),  # Multi-line comments
        re.compile(r"///.*$", re.MULTILINE),  # XML documentation comments
    ],
    "Ruby": [
        re.compile(r"#.*$", re.MULTILINE),  # Single line comments
        re.compile(r"=begin[\s\S]*?=end", re.MULTILINE),  # Multi-line comments
    ],
    "PHP": [
        re.compile(r"//.*$", re.MULTILINE),  # Single line comments
        re.compile(r"#.*$", re.MULTILINE),  # Shell-style comments
        re.compile(r"/\*[\s\S]*?\*/"),  # Multi-line comments
    ],
    "Go": [
        re.compile(r"//.*$", re.MULTILINE),  # Single line comments
        re.compile(r"/\*[\s\S]*?\*/"),  # Multi-line comments
    ],
    "Rust": [
        re.compile(r"//.*$", re.MULTILINE),  # Single line comments
        re.compile(r"/\*[\s\S]*?\*/"),  # Multi-line comments
        re.compile(r"//!.*$", re.MULTILINE),  # Doc comments
        re.compile(r"///.*$", re.MULTILINE),  # Doc comments
    ],
    "SQL": [
        re.compile(r"--.*$", re.MULTILINE),  # Single line comments
        re.compile(r"/\*[\s\S]*?\*/"),  # Multi-line comments
    ],
    "YAML": [
        re.compile(r"#.*$", re.MULTILINE),  # Single line comments
    ],
    "Markdown": [
        re.compile(r"<!--[\s\S]*?-->"),  # HTML comments
    ],
    "Shell": [
        re.compile(r"#.*$", re.MULTILINE),  # Single line comments
    ],
    "PowerShell": [
        re.compile(r"#.*$", re.MULTILINE),  # Single line comments
        re.compile(r"<#[\s\S]*?#>"),  # Multi-line comments
    ],
}

# Language-specific whitespace rules
LANGUAGE_WHITESPACE_RULES: Dict[str, Dict[str, bool]] = {
    "Python": {"preserve_indentation": True, "collapse_empty_lines": True},
    "JavaScript": {"preserve_indentation": True, "collapse_empty_lines": True},
    "TypeScript": {"preserve_indentation": True, "collapse_empty_lines": True},
    "HTML": {"preserve_indentation": False, "collapse_empty_lines": False},
    "CSS": {"preserve_indentation": True, "collapse_empty_lines": True},
    "Java": {"preserve_indentation": True, "collapse_empty_lines": True},
    "C#": {"preserve_indentation": True, "collapse_empty_lines": True},
    "Ruby": {"preserve_indentation": True, "collapse_empty_lines": True},
    "Go": {"preserve_indentation": True, "collapse_empty_lines": True},
    "Rust": {"preserve_indentation": True, "collapse_empty_lines": True},
    "SQL": {"preserve_indentation": False, "collapse_empty_lines": True},
    "YAML": {"preserve_indentation": True, "collapse_empty_lines": False},
    "Markdown": {"preserve_indentation": True, "collapse_empty_lines": False},
}

# Common whitespace patterns
WHITESPACE_PATTERNS = [
    (re.compile(r"\s+$", re.MULTILINE), ""),  # Trailing whitespace
    (re.compile(r"^\s+$", re.MULTILINE), ""),  # Empty lines with whitespace
    (re.compile(r"\n{3,}", re.MULTILINE), "\n\n"),  # Multiple blank lines
    (re.compile(r"[ \t]+(?=\n)", re.MULTILINE), ""),  # Trailing spaces before newlines
]


class ContentSanitizer:
    """Sanitizes code content for optimal LLM processing."""

    def __init__(self, preserve_comments: bool = True, aggressive_whitespace: bool = False):
        """Initialize the content sanitizer.

        Args:
            preserve_comments: Whether to preserve code comments
            aggressive_whitespace: Whether to aggressively minimize whitespace
        """
        self.preserve_comments = preserve_comments
        self.aggressive_whitespace = aggressive_whitespace
        self.tokenizer = CodeTokenizer()

    def clean_whitespace(self, content: str, language: Optional[str] = None) -> str:
        """Clean whitespace from content.

        Args:
            content: Content to clean
            language: Optional programming language for language-specific rules

        Returns:
            str: Content with cleaned whitespace
        """
        if not content:
            return content

        result = content
        rules = LANGUAGE_WHITESPACE_RULES.get(language or "", {
            "preserve_indentation": True,
            "collapse_empty_lines": True
        })

        if self.aggressive_whitespace:
            # More aggressive whitespace reduction
            # First normalize newlines
            result = result.replace("\r\n", "\n")
            # Replace newlines with placeholders in braces
            result = result.replace("\n", "{NEWLINE}")
            # Collapse all whitespace to single space
            result = re.sub(r"\s+", " ", result)
            # Remove space around brackets
            result = re.sub(r"\s*([{}()[\]<>])\s*", r"\1", result)
            # Space after but not before punctuation
            result = re.sub(r"\s*([;,])\s*", r"\1 ", result)
            # Clean up newlines in braces
            result = result.replace("{NEWLINE}", "")
            # Clean up any remaining multiple spaces
            result = re.sub(r"\s+", " ", result)
            return result.strip()
        else:
            # Split into lines for line-by-line processing
            lines = result.split("\n")
            cleaned_lines = []
            for line in lines:
                # Convert tabs to spaces
                line = line.expandtabs(4)
                # Remove trailing whitespace
                line = line.rstrip()
                # Preserve indentation based on language rules
                if not rules["preserve_indentation"]:
                    line = line.lstrip()
                # Collapse multiple spaces
                line = re.sub(r" +", " ", line)
                # Handle empty lines
                if not line.strip():
                    line = ""
                cleaned_lines.append(line)

            # Join lines and handle empty line collapsing
            result = "\n".join(cleaned_lines)
            if rules["collapse_empty_lines"]:
                result = re.sub(r"\n{3,}", "\n\n", result)
            # Ensure single newline at end
            return result.rstrip("\n") + "\n"

    def normalize_newlines(self, content: str) -> str:
        """Normalize line endings and remove excessive blank lines.

        Args:
            content: Content to normalize

        Returns:
            str: Content with normalized line endings
        """
        if not content:
            return content

        # Convert all line endings to \n
        result = content.replace("\r\n", "\n").replace("\r", "\n")

        # Remove multiple blank lines
        result = re.sub(r"\n{3,}", "\n\n", result)

        # Ensure file ends with single newline
        result = result.rstrip("\n") + "\n"

        return result

    def clean_comments(self, content: str, language: str) -> str:
        """Clean comments from content based on language.

        Args:
            content: Content to clean
            language: Programming language

        Returns:
            str: Content with cleaned comments
        """
        if not content or not language or self.preserve_comments:
            return content

        result = content
        patterns = COMMENT_PATTERNS.get(language, [])

        for pattern in patterns:
            result = pattern.sub("", result)

        return result

    def truncate_to_token_limit(
        self, content: str, max_tokens: int, language: Optional[str] = None
    ) -> Tuple[str, int]:
        """Truncate content to fit within token limit while preserving code structure.

        Args:
            content: Content to truncate
            max_tokens: Maximum number of tokens allowed
            language: Optional programming language for smarter truncation

        Returns:
            Tuple[str, int]: (truncated_content, token_count)
        """
        if not content:
            return content, 0

        # First clean the content
        cleaned = self.clean_content(content, language)
        token_count = self.tokenizer.count_tokens(cleaned)

        if token_count <= max_tokens:
            return cleaned, token_count

        # Try to find natural break points
        lines = cleaned.split("\n")
        current_tokens = 0
        truncated_lines = []

        for line in lines:
            line_tokens = self.tokenizer.count_tokens(line)
            if current_tokens + line_tokens > max_tokens:
                break
            truncated_lines.append(line)
            current_tokens += line_tokens

        # If we have lines, join them
        if truncated_lines:
            result = "\n".join(truncated_lines)
            # Add truncation indicator
            result += "\n# Content truncated to fit token limit\n"
            return result, self.tokenizer.count_tokens(result)

        # If we can't preserve full lines, do character-based truncation
        result = self.tokenizer.truncate_to_token_limit(cleaned, max_tokens)
        return result, self.tokenizer.count_tokens(result)

    def clean_content(self, content: str, language: Optional[str] = None) -> str:
        """Clean and optimize content for LLM processing.

        Args:
            content: Content to clean
            language: Optional programming language for language-specific cleaning

        Returns:
            str: Cleaned content
        """
        if not content:
            return content

        result = content

        # Normalize line endings first
        result = self.normalize_newlines(result)

        # Clean comments if language is specified and not preserving
        if language and not self.preserve_comments:
            result = self.clean_comments(result, language)

        # Clean whitespace last
        result = self.clean_whitespace(result, language)

        return result

    def get_language_patterns(self, language: str) -> List[Pattern[str]]:
        """Get comment patterns for a specific language.

        Args:
            language: Programming language

        Returns:
            List[Pattern[str]]: List of regex patterns for the language
        """
        return COMMENT_PATTERNS.get(language, [])
