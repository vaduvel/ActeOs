"""HTML → plain text normalization.

Strips tags, scripts, styles. Collapses whitespace. Preserves
structural line breaks (headings, paragraphs, list items, table rows).
No external dependencies — uses stdlib html.parser.
"""

from __future__ import annotations

import re
from html.parser import HTMLParser

# Tags that introduce a line break in the output
_BLOCK_TAGS = frozenset({
    "p", "div", "h1", "h2", "h3", "h4", "h5", "h6",
    "li", "tr", "td", "th", "blockquote", "section",
    "article", "header", "footer", "nav", "br", "hr",
    "dt", "dd", "figcaption", "pre",
})

# Tags whose content is completely removed
_SKIP_TAGS = frozenset({
    "script", "style", "noscript", "template", "svg",
})


class _TextExtractor(HTMLParser):
    """Extract text from HTML, preserving structural breaks."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._parts: list[str] = []
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in _SKIP_TAGS:
            self._skip_depth += 1
        if tag in _BLOCK_TAGS and self._parts and not self._parts[-1].endswith("\n"):
            self._parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in _SKIP_TAGS:
            self._skip_depth = max(0, self._skip_depth - 1)
        if tag in _BLOCK_TAGS and self._parts and not self._parts[-1].endswith("\n"):
            self._parts.append("\n")

    def handle_data(self, data: str) -> None:
        if self._skip_depth > 0:
            return
        # Collapse internal whitespace
        cleaned = re.sub(r"\s+", " ", data)
        self._parts.append(cleaned)

    def get_text(self) -> str:
        raw = "".join(self._parts)
        # Collapse multiple newlines
        raw = re.sub(r"\n{3,}", "\n\n", raw)
        # Strip leading/trailing whitespace per line
        lines = [line.strip() for line in raw.split("\n")]
        # Remove empty lines at start/end
        while lines and not lines[0]:
            lines.pop(0)
        while lines and not lines[-1]:
            lines.pop()
        return "\n".join(lines)


def normalize_html(html: str | bytes) -> str:
    """Convert HTML content to normalized plain text.

    Args:
        html: HTML string or bytes.

    Returns:
        Plain text with structural line breaks preserved.
    """
    if isinstance(html, bytes):
        html = html.decode("utf-8", errors="replace")

    extractor = _TextExtractor()
    try:
        extractor.feed(html)
        extractor.close()
    except Exception:
        # Malformed HTML: fall back to tag stripping
        text = re.sub(r"<[^>]+>", " ", html)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    return extractor.get_text()


def normalize_text(text: str) -> str:
    """Normalize plain text (collapse whitespace, strip)."""
    text = re.sub(r"\s+", " ", text)
    return text.strip()
