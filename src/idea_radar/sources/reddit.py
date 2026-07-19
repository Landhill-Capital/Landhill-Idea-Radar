"""Scan Reddit subs via public JSON endpoints for pain-signal posts."""
from __future__ import annotations
import os, re, time
from typing import List, Dict
import httpx

from ..config import REDDIT_SUBS, PAIN_PATTERNS

UA = os.environ.get("REDDIT_USER_AGENT", "landhill-idea-radar/0.1")
_PAIN_RE = re.compile("|".join(PAIN_PATTERNS), re.IGNORECASE)


def scan(subs: List[str] = None, limit_per_sub: int = 50) -> List[Dict]:
    subs = subs or REDDIT_SUBS
    hits = []
    with httpx.Client(headers={"User-Agent": UA}, timeout=20) as c:
        for sub in subs:
            url = f"https://www.reddit.com/r/{sub}/new.json?limit={limit_per_sub}"
            try:
                r = c.get(url)
                r.raise_for_status()
                data = r.json()
            except Exception as e:
                print(f"[reddit] {sub}: {e}")
                continue
            for post in data.get("data", {}).get("children", []):
                p = post["data"]
                blob = f"{p.get('title','')}\n{p.get('selftext','')}"
                if _PAIN_RE.search(blob):
                    hits.append({
                        "sub": sub,
                        "title": p.get("title"),
                        "url": f"https://reddit.com{p.get('permalink')}",
                        "score": p.get("score", 0),
                        "num_comments": p.get("num_comments", 0),
                        "excerpt": (p.get("selftext") or "")[:280],
                    })
            time.sleep(1.2)  # polite
    hits.sort(key=lambda h: h["num_comments"] + h["score"] / 2, reverse=True)
    return hits
