"""Language detection utilities."""

from typing import Optional, cast, List

from pygments.lexer import Lexer
from pygments.lexers import guess_lexer, guess_lexer_for_filename
from pygments.util import ClassNotFound


def detect_language(content: str, filename: Optional[str] = None) -> str:
    """
    Detect the programming language of a code snippet.

    Args:
        content: The code content to analyze
        filename: Optional filename to help with detection

    Returns:
        str: The detected language name
    """
    try:
        if filename:
            lexer = cast(Lexer, guess_lexer_for_filename(filename, content))
        else:
            lexer = cast(Lexer, guess_lexer(content))

        # Get the language name from the lexer's aliases
        aliases: List[str] = getattr(lexer, "aliases", [])
        if aliases:
            return aliases[0]

        # Fallback to the class name if no aliases
        return lexer.__class__.__name__.replace("Lexer", "")

    except ClassNotFound:
        # Default to plaintext if we can't detect the language
        return "text"
