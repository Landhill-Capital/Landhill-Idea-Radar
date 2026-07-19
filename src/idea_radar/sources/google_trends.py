"""Google Trends NZ — rising queries via the public daily-trends RSS."""
from __future__ import annotations
from typing import List, Dict
import feedparser
from ._util import clean_summary

FEED = "https://trends.google.com/trending/rss?geo=NZ"


def scan(limit: int = 20) -> List[Dict]:
    d = feedparser.parse(FEED)
    out = []
    for e in d.entries[:limit]:
        approx = ""
        for k, v in e.items():
            if k.endswith("approx_traffic"):
                approx = v
                break
        out.append({
            "query": e.get("title"),
            "url": e.get("link"),
            "approx_traffic": approx,
            "summary": clean_summary(e.get("summary")),
            "published": e.get("published"),
        })
    return out
