"""Scan Reddit subs via public RSS feeds for pain-signal posts.

Reddit's `.json` endpoint is 403-blocked without OAuth; the `.rss`
endpoint is still open and requires no auth.
"""
from __future__ import annotations
import os, re, time
from typing import List, Dict
import feedparser

from ..config import REDDIT_SUBS, PAIN_PATTERNS
from ._util import clean_summary

UA = os.environ.get("REDDIT_USER_AGENT", "landhill-idea-radar/0.1")
_PAIN_RE = re.compile("|".join(PAIN_PATTERNS), re.IGNORECASE)


def scan(subs: List[str] = None, limit_per_sub: int = 25) -> List[Dict]:
    subs = subs or REDDIT_SUBS
    hits = []
    for sub in subs:
        url = f"https://www.reddit.com/r/{sub}/new.rss?limit={limit_per_sub}"
        try:
            d = feedparser.parse(url, agent=UA)
            if d.get("bozo") and not d.entries:
                print(f"[reddit] {sub}: no entries")
                continue
        except Exception as e:  # pragma: no cover
            print(f"[reddit] {sub}: {e}")
            continue
        for entry in d.entries:
            title = entry.get("title") or ""
            body = clean_summary(entry.get("summary"), limit=2000)
            if _PAIN_RE.search(f"{title}\n{body}"):
                hits.append({
                    "sub": sub,
                    "title": title,
                    "url": entry.get("link"),
                    "excerpt": clean_summary(entry.get("summary"), limit=280),
                    "published": entry.get("published"),
                })
        time.sleep(1.2)  # polite
    return hits
