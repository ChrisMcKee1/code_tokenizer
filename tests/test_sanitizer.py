"""Tests for content sanitization."""

import pytest

from code_tokenizer.core.sanitizer import ContentSanitizer


@pytest.fixture
def sanitizer():
    """Create a ContentSanitizer instance."""
    return ContentSanitizer()


@pytest.fixture
def aggressive_sanitizer():
    """Create a ContentSanitizer with aggressive whitespace cleaning."""
    return ContentSanitizer(preserve_comments=False, aggressive_whitespace=True)


class TestContentSanitizer:
    """Test content sanitization functionality."""

    def test_clean_whitespace_basic(self, sanitizer):
        """Test basic whitespace cleaning."""
        content = "  def test():  \n    print('hello')  \n\n\n"
        expected = "def test():\n    print('hello')\n"
        assert sanitizer.clean_whitespace(content) == expected

    def test_clean_whitespace_aggressive(self, aggressive_sanitizer):
        """Test aggressive whitespace cleaning."""
        content = "def test():\n    print('hello')\n"
        expected = "def test(){print('hello')}"
        result = aggressive_sanitizer.clean_whitespace(content.replace("\n", "{"))
        assert result == expected

    def test_normalize_newlines(self, sanitizer):
        """Test newline normalization."""
        content = "line1\r\nline2\rline3\nline4\n\n\n\nline5"
        expected = "line1\nline2\nline3\nline4\n\nline5\n"
        assert sanitizer.normalize_newlines(content) == expected

    @pytest.mark.parametrize(
        "language,content,expected",
        [
            (
                "Python",
                '# Comment\ndef test(): # Inline\n    """Docstring"""\n    pass',
                "def test(): \n    \n    pass",
            ),
            (
                "JavaScript",
                "// Comment\nfunction test() { // Inline\n    /* Multi\n    line */\n}",
                "function test() { \n    \n}",
            ),
            ("HTML", "<!-- Comment --><div>Test</div><!-- End -->", "<div>Test</div>"),
            ("CSS", "/* Comment */\nbody { /* Style */ color: red; }", "body {  color: red; }"),
            (
                "Java",
                "/** JavaDoc */\npublic class Test { // Comment\n    /* Multi\n    line */\n}",
                "public class Test { \n    \n}",
            ),
            (
                "C#",
                "/// XML Doc\npublic class Test { // Comment\n    /* Multi\n    line */\n}",
                "public class Test { \n    \n}",
            ),
            (
                "Ruby",
                "# Comment\n=begin\nMulti\nline\n=end\ndef test\n  puts 'hi'\nend",
                "def test\n  puts 'hi'\nend",
            ),
            (
                "PHP",
                "<?php\n# Shell style\n// Line comment\n/* Multi\nline */\necho 'hi';",
                "<?php\necho 'hi';",
            ),
            (
                "Go",
                "// Comment\nfunc test() {\n    /* Multi\n    line */\n}",
                "func test() {\n    \n}",
            ),
            (
                "Rust",
                "//! Doc comment\n/// Function doc\n// Comment\nfn test() {\n    /* Multi\n    line */\n}",
                "fn test() {\n    \n}",
            ),
            (
                "SQL",
                "-- Comment\nSELECT * /* Multi\nline */\nFROM table;",
                "SELECT * \nFROM table;",
            ),
            (
                "YAML",
                "# Comment\nkey: value\n# Another comment\nlist:\n  - item",
                "key: value\nlist:\n  - item",
            ),
            (
                "PowerShell",
                "# Comment\n<#\nMulti\nline\n#>\nWrite-Host 'hi'",
                "Write-Host 'hi'",
            ),
        ],
    )
    def test_clean_comments_all_languages(self, aggressive_sanitizer, language, content, expected):
        """Test comment cleaning for all supported languages."""
        result = aggressive_sanitizer.clean_comments(content, language)
        # Normalize whitespace for comparison
        result = " ".join(result.split())
        expected = " ".join(expected.split())
        assert result == expected

    def test_clean_content_full(self, aggressive_sanitizer):
        """Test full content cleaning pipeline."""
        content = '''
        def test():  # Function
            """
            Docstring
            """
            x = 1   # Value
            
            
            return x  # Return
        '''
        expected = "def test():x=1 return x"
        result = aggressive_sanitizer.clean_content(content, "Python")
        # Normalize whitespace for comparison
        result = "".join(result.split())
        expected = "".join(expected.split())
        assert result == expected

    def test_preserve_comments(self, sanitizer):
        """Test comment preservation."""
        content = "# Header\ndef test(): # Function\n    pass # End"
        result = sanitizer.clean_content(content, "Python")
        assert "# Header" in result
        assert "# Function" in result
        assert "# End" in result

    def test_empty_content(self, sanitizer):
        """Test handling of empty content."""
        assert sanitizer.clean_content("") == ""
        assert sanitizer.clean_content(None) == None
        assert sanitizer.clean_whitespace("") == ""
        assert sanitizer.normalize_newlines("") == ""
        assert sanitizer.clean_comments("", "Python") == ""

    def test_unknown_language(self, sanitizer):
        """Test handling of unknown language."""
        content = "// Comment\ncode\n/* Multi-line */"
        result = sanitizer.clean_content(content, "UnknownLang")
        assert "// Comment" in result
        assert "/* Multi-line */" in result

    def test_get_language_patterns(self, sanitizer):
        """Test getting language-specific patterns."""
        python_patterns = sanitizer.get_language_patterns("Python")
        assert len(python_patterns) == 3  # Single line, triple double, triple single

        js_patterns = sanitizer.get_language_patterns("JavaScript")
        assert len(js_patterns) == 2  # Single line, multi-line

        unknown_patterns = sanitizer.get_language_patterns("UnknownLang")
        assert len(unknown_patterns) == 0

    def test_mixed_content(self, sanitizer):
        """Test handling of mixed content types."""
        content = '''
        def test():
            # Python comment
            html = """
            <!-- HTML comment -->
            <div>Test</div>
            """
            css = """
            /* CSS comment */
            body { color: red; }
            """
        '''
        result = sanitizer.clean_content(content, "Python")
        assert "def test():" in result
        assert "# Python comment" in result  # Preserved by default
        assert "<div>Test</div>" in result
        assert "body { color: red; }" in result

    @pytest.mark.parametrize(
        "input_content,expected",
        [
            ("no_whitespace", "no_whitespace"),
            ("  leading_space", "leading_space"),
            ("trailing_space  ", "trailing_space"),
            ("\ttabbed\t", "tabbed"),
            ("multiple    spaces", "multiple spaces"),
            ("line1\n  line2", "line1\nline2"),
        ],
    )
    def test_whitespace_variations(self, sanitizer, input_content, expected):
        """Test various whitespace patterns."""
        assert sanitizer.clean_whitespace(input_content).strip() == expected.strip()

    def test_truncate_to_token_limit(self, sanitizer):
        """Test token-aware content truncation."""
        # Test content that doesn't need truncation
        content = "def test():\n    pass"
        result, tokens = sanitizer.truncate_to_token_limit(content, 100)
        assert result == content + "\n"  # clean_content adds newline
        assert tokens < 100

        # Test content that needs truncation
        long_content = "def test():\n" + "    print('test')\n" * 50
        result, tokens = sanitizer.truncate_to_token_limit(long_content, 20)
        assert tokens <= 20
        assert result.endswith("# Content truncated to fit token limit\n")
        assert "def test():" in result

        # Test empty content
        result, tokens = sanitizer.truncate_to_token_limit("", 100)
        assert result == ""
        assert tokens == 0

        # Test content with comments
        content_with_comments = """
        # Header comment
        def test():
            # Function comment
            pass
        """
        result, tokens = sanitizer.truncate_to_token_limit(content_with_comments, 20)
        assert tokens <= 20
        if sanitizer.preserve_comments:
            assert "# Header" in result
        assert "def test()" in result

    def test_truncate_with_language(self, sanitizer):
        """Test language-aware truncation."""
        python_code = """
        def function1():
            # First function
            pass

        def function2():
            # Second function
            pass
        """
        result, tokens = sanitizer.truncate_to_token_limit(python_code, 20, "Python")
        assert tokens <= 20
        assert "def function1()" in result
        assert "function2" not in result  # Should be truncated

        js_code = """
        function test1() {
            // First function
            return true;
        }

        function test2() {
            // Second function
            return false;
        }
        """
        result, tokens = sanitizer.truncate_to_token_limit(js_code, 20, "JavaScript")
        assert tokens <= 20
        assert "function test1" in result
        assert "test2" not in result  # Should be truncated

    def test_truncate_edge_cases(self, sanitizer):
        """Test truncation edge cases."""
        # Test with exactly matching token count
        content = "x = 1"
        result, tokens = sanitizer.truncate_to_token_limit(content, 3)
        assert result == content + "\n"
        assert tokens <= 3

        # Test with very small token limit
        content = "def test(): pass"
        result, tokens = sanitizer.truncate_to_token_limit(content, 1)
        assert tokens <= 1
        assert result  # Should contain something, even if just a partial token

        # Test with None language
        result, tokens = sanitizer.truncate_to_token_limit(content, 5, None)
        assert tokens <= 5
        assert result  # Should handle None language gracefully

    @pytest.mark.parametrize(
        "language,content,preserve_indentation,collapse_empty_lines",
        [
            ("Python", "    def test():\n        pass\n\n\n", True, True),
            ("JavaScript", "    function test() {\n        return;\n    }\n\n\n", True, True),
            ("HTML", "    <div>\n        <p>Test</p>\n    </div>\n\n\n", False, False),
            ("YAML", "    key:\n      - value\n\n\n", True, False),
            ("SQL", "    SELECT *\n        FROM table\n\n\n", False, True),
            ("Markdown", "    # Header\n    - List item\n\n\n", True, False),
        ],
    )
    def test_language_specific_whitespace(
        self, sanitizer, language, content, preserve_indentation, collapse_empty_lines
    ):
        """Test language-specific whitespace handling."""
        result = sanitizer.clean_whitespace(content, language)
        lines = result.split("\n")

        # Check indentation preservation
        if preserve_indentation:
            assert any(line.startswith("    ") for line in lines if line.strip())
        else:
            assert not any(line.startswith("    ") for line in lines if line.strip())

        # Check empty line handling
        if collapse_empty_lines:
            assert result.count("\n\n\n") == 0
        else:
            assert result.count("\n\n\n") > 0

    def test_language_specific_edge_cases(self, sanitizer):
        """Test edge cases with language-specific handling."""
        # Test unknown language (should use defaults)
        content = "    def test():\n        pass\n\n\n"
        result = sanitizer.clean_whitespace(content, "UnknownLang")
        assert result.startswith("    ")  # Default preserves indentation
        assert "\n\n\n" not in result  # Default collapses empty lines

        # Test None language
        result = sanitizer.clean_whitespace(content, None)
        assert result.startswith("    ")
        assert "\n\n\n" not in result

        # Test empty content with language
        assert sanitizer.clean_whitespace("", "Python") == ""
        assert sanitizer.clean_whitespace("", "HTML") == ""
