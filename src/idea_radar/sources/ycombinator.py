"""YC/HN launch signals via Algolia's Hacker News API.

The old YC `/launches/rss` endpoint 404s. Instead we surface fresh
"Show HN" stories from Algolia's HN index — this is a broader but
higher-signal feed of new launches, many of which are YC-backed.
"""
from __future__ import annotations
import os
from typing import List, Dict
import httpx

API = "https://hn.algolia.com/api/v1/search_by_date"
_CA = (os.environ.get("REQUESTS_CA_BUNDLE")
       or os.environ.get("SSL_CERT_FILE")
       or "/etc/ssl/certs/ca-certificates.crt")
_VERIFY = _CA if os.path.exists(_CA) else True


def scan(limit: int = 15, min_points: int = 5) -> List[Dict]:
    params = {"tags": "show_hn", "hitsPerPage": limit * 3}
    try:
        r = httpx.get(API, params=params, timeout=20, verify=_VERIFY)
        r.raise_for_status()
        data = r.json()
    except Exception as e:  # pragma: no cover
        print(f"[hn/show] {e}")
        return []
    out = []
    for hit in data.get("hits", []):
        if (hit.get("points") or 0) < min_points:
            continue
        out.append({
            "title": (hit.get("title") or "").removeprefix("Show HN: "),
            "url": hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}",
            "hn_url": f"https://news.ycombinator.com/item?id={hit.get('objectID')}",
            "points": hit.get("points"),
            "comments": hit.get("num_comments"),
            "author": hit.get("author"),
        })
        if len(out) >= limit:
            break
    return out
