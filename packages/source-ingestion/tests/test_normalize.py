"""Tests for HTML normalization."""

from __future__ import annotations

from pathlib import Path

from wb_ingestion.normalize import normalize_html, normalize_text

FIXTURES = Path(__file__).parent / "fixtures"


class TestNormalizeHtml:
    def test_basic_html(self) -> None:
        html = "<p>Hello <b>world</b></p>"
        text = normalize_html(html)
        assert "Hello" in text
        assert "world" in text
        assert "<" not in text

    def test_strips_scripts(self) -> None:
        html = '<p>Before</p><script>var x = 1;</script><p>After</p>'
        text = normalize_html(html)
        assert "Before" in text
        assert "After" in text
        assert "var x" not in text

    def test_strips_styles(self) -> None:
        html = '<style>body { color: red; }</style><p>Content</p>'
        text = normalize_html(html)
        assert "Content" in text
        assert "color" not in text

    def test_preserves_headings(self) -> None:
        html = "<h1>Title</h1><h2>Subtitle</h2><p>Body</p>"
        text = normalize_html(html)
        lines = text.split("\n")
        assert "Title" in lines
        assert "Subtitle" in lines

    def test_preserves_list_items(self) -> None:
        html = "<ul><li>Item 1</li><li>Item 2</li></ul>"
        text = normalize_html(html)
        assert "Item 1" in text
        assert "Item 2" in text

    def test_collapses_whitespace(self) -> None:
        html = "<p>  Multiple   spaces   here  </p>"
        text = normalize_html(html)
        assert "  " not in text.split("\n")[0]  # no double spaces

    def test_bytes_input(self) -> None:
        html = b"<p>Bytes input</p>"
        text = normalize_html(html)
        assert "Bytes input" in text

    def test_malformed_html_fallback(self) -> None:
        html = "<p>Unclosed<div>Nested"
        text = normalize_html(html)
        assert "Unclosed" in text
        assert "Nested" in text

    def test_empty_html(self) -> None:
        assert normalize_html("") == ""

    def test_fixture_sample_page(self) -> None:
        html = (FIXTURES / "sample_page.html").read_text()
        text = normalize_html(html)
        assert "18 ani" in text
        assert "68 lei" in text
        assert "10 ani" in text
        assert "Carte de identitate" in text
        # Script and style content should be gone
        assert "tracking" not in text
        assert "font-size" not in text

    def test_fixture_malformed(self) -> None:
        html = (FIXTURES / "malformed.html").read_text()
        text = normalize_html(html)
        assert len(text) > 0
        assert "Unclosed" in text


class TestNormalizeText:
    def test_collapses_whitespace(self) -> None:
        assert normalize_text("  hello   world  ") == "hello world"

    def test_newlines_become_spaces(self) -> None:
        assert normalize_text("hello\nworld") == "hello world"

    def test_empty(self) -> None:
        assert normalize_text("") == ""
