"""Pull recent Product Hunt launches via their public RSS."""
from __future__ import annotations
from typing import List, Dict
import feedparser
from ._util import clean_summary

FEED = "https://www.producthunt.com/feed"


def scan(limit: int = 30) -> List[Dict]:
    d = feedparser.parse(FEED)
    out = []
    for e in d.entries[:limit]:
        out.append({
            "title": e.get("title"),
            "url": e.get("link"),
            "summary": clean_summary(e.get("summary")),
            "published": e.get("published"),
        })
    return out
