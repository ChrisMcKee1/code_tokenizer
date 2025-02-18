"""Tests for language detector functionality."""

import pytest

from code_tokenizer.services.language_detector import (
    LanguageDetector,
    detect_language,
    detect_language_by_patterns,
    get_language_by_extension,
)


@pytest.mark.unit
def test_get_language_by_extension():
    """Test getting language by file extension."""
    # Test common extensions
    assert get_language_by_extension("py") == "Python"
    assert get_language_by_extension("js") == "JavaScript"
    assert get_language_by_extension("ts") == "TypeScript"
    assert get_language_by_extension("html") == "HTML"
    assert get_language_by_extension("css") == "CSS"
    assert get_language_by_extension("md") == "Markdown"
    assert get_language_by_extension("sh") == "Shell"
    assert get_language_by_extension("sql") == "SQL"

    # Test less common extensions
    assert get_language_by_extension("pyi") == "Python"
    assert get_language_by_extension("jsx") == "JavaScript"
    assert get_language_by_extension("tsx") == "TypeScript"
    assert get_language_by_extension("scss") == "SCSS"

    # Test unknown extension
    assert get_language_by_extension("xyz") == "Unknown"


@pytest.mark.unit
def test_detect_language_by_patterns():
    """Test language detection using pattern matching."""
    # Test Python patterns
    python_code = """
    def test_function():
        pass
    
    class TestClass:
        def method(self):
            pass
    """
    assert detect_language_by_patterns(python_code) == "Python"

    # Test JavaScript patterns
    js_code = """
    function test() {
        return true;
    }
    
    const x = 5;
    let y = 10;
    """
    assert detect_language_by_patterns(js_code) == "JavaScript"

    # Test HTML patterns
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test</title>
    </head>
    <body>
        <div>Content</div>
    </body>
    </html>
    """
    assert detect_language_by_patterns(html_code) == "HTML"

    # Test CSS patterns
    css_code = """
    .class {
        color: red;
    }
    
    @media screen {
        body {
            background: white;
        }
    }
    """
    assert detect_language_by_patterns(css_code) == "CSS"

    # Test empty content
    assert detect_language_by_patterns("") == "Text"

    # Test content with no clear patterns
    assert detect_language_by_patterns("Some random text") == "Text"


@pytest.mark.unit
def test_language_detector_resolve_conflicts():
    """Test language conflict resolution."""
    detector = LanguageDetector()

    # Test HTML vs JavaScript conflict
    mixed_content = """
    <html>
    <script>
        function test() {
            console.log('Hello');
        }
    </script>
    </html>
    """
    assert detector.detect_language(mixed_content, "test.html") == "HTML"
    assert detector.detect_language(mixed_content, "test.js") == "JavaScript"

    # Test Python vs JavaScript conflict
    mixed_py_js = """
    def python_func():
        pass
        
    function jsFunc() {
        return true;
    }
    """
    assert detector.detect_language(mixed_py_js, "test.py") == "Python"
    assert detector.detect_language(mixed_py_js, "test.js") == "JavaScript"


@pytest.mark.unit
def test_detect_by_simple_indicators():
    """Test detection using simple content indicators."""
    detector = LanguageDetector()

    # Test JSON detection
    json_content = '{"name": "test", "value": true}'
    assert detector._detect_by_simple_indicators(json_content) == "JSON"

    # Test invalid JSON
    invalid_json = '{"name": test"}'
    assert detector._detect_by_simple_indicators(invalid_json) is None

    # Test HTML detection
    html_content = "<!DOCTYPE html><html><body></body></html>"
    assert detector._detect_by_simple_indicators(html_content) == "HTML"

    # Test CSS detection
    css_content = ".class { color: red; margin: 0; }"
    assert detector._detect_by_simple_indicators(css_content) == "CSS"

    # Test unknown content
    unknown_content = "Some random text"
    assert detector._detect_by_simple_indicators(unknown_content) == "Unknown"


@pytest.mark.unit
def test_normalize_language_name():
    """Test language name normalization."""
    detector = LanguageDetector()

    # Test direct mappings
    assert detector.normalize_language_name("python") == "Python"
    assert detector.normalize_language_name("javascript") == "JavaScript"
    assert detector.normalize_language_name("typescript") == "TypeScript"

    # Test variations
    assert detector.normalize_language_name("py") == "Python"
    assert detector.normalize_language_name("js") == "JavaScript"
    assert detector.normalize_language_name("ts") == "TypeScript"

    # Test case variations
    assert detector.normalize_language_name("PYTHON") == "Python"
    assert detector.normalize_language_name("JavaScript") == "JavaScript"
    assert detector.normalize_language_name("HTML") == "HTML"

    # Test unknown language
    assert detector.normalize_language_name("unknown") == "Unknown"
    assert detector.normalize_language_name("xyz") == "Xyz"


@pytest.mark.unit
def test_get_file_extension():
    """Test getting file extension."""
    detector = LanguageDetector()

    # Test normal cases
    assert detector._get_file_extension("test.py") == ".py"
    assert detector._get_file_extension("path/to/file.js") == ".js"
    assert detector._get_file_extension("test.min.css") == ".css"

    # Test edge cases
    assert detector._get_file_extension("no_extension") == ""
    assert detector._get_file_extension(".hidden") == ".hidden"
    assert detector._get_file_extension("") == ""


@pytest.mark.unit
def test_detect_language_edge_cases():
    """Test language detection edge cases."""
    detector = LanguageDetector()

    # Test None content
    assert detector.detect_language(None) == "Text"
    assert detector.detect_language(None, "test.py") == "Text"

    # Test empty content
    assert detector.detect_language("") == "Text"
    assert detector.detect_language("", "test.py") == "Text"

    # Test content with only whitespace
    assert detector.detect_language("   \n\t  ") == "Text"

    # Test with invalid filename
    assert detector.detect_language("print('hello')", "") == "Text"
    assert detector.detect_language("print('hello')", None) == "Text"

    # Test with non-existent file extension
    assert detector.detect_language("print('hello')", "test.xyz") == "Text"


@pytest.mark.unit
def test_resolve_language_conflicts_edge_cases():
    """Test language conflict resolution edge cases."""
    detector = LanguageDetector()

    # Test empty candidates list
    assert detector._resolve_language_conflicts([], "content") == "Unknown"

    # Test single candidate
    assert detector._resolve_language_conflicts(["Python"], "content") == "Python"

    # Test HTML detection priority
    assert (
        detector._resolve_language_conflicts(
            ["JavaScript", "HTML", "Python"],
            "<html><body><script>var x = 5;</script></body></html>",
        )
        == "HTML"
    )

    # Test Python vs JavaScript scoring with more Python features
    mixed_code = """
    def test():
        pass
    class MyClass:
        pass
    import os
    from typing import List
    
    function test() {
        return true;
    }
    """
    assert detector._resolve_language_conflicts(["JavaScript", "Python"], mixed_code) == "Python"

    # Test Python vs JavaScript scoring with more JavaScript features
    js_heavy_code = """
    function test() {
        return true;
    }
    const x = 5;
    let y = 10;
    var z = 15;
    => {
        console.log('test');
    }
    
    def simple_func():
        pass
    """
    assert (
        detector._resolve_language_conflicts(["JavaScript", "Python"], js_heavy_code)
        == "JavaScript"
    )
