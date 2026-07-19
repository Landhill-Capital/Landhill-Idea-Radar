"""Small helpers shared by feed-parsing sources."""
from __future__ import annotations
import re
from html import unescape

_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")


def clean_summary(html_or_text: str, limit: int = 240) -> str:
    """Strip HTML tags, collapse whitespace, truncate."""
    if not html_or_text:
        return ""
    text = _TAG_RE.sub(" ", unescape(html_or_text))
    text = _WS_RE.sub(" ", text).strip()
    if len(text) > limit:
        text = text[: limit - 1].rstrip() + "…"
    return text
