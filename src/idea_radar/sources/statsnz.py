"""Scrape StatsNZ information-releases index for latest release headlines.

Stats NZ retired their open-data API (Aug 2024) and does not publish
an RSS feed. Their information-releases index page embeds recent
releases as inline data — cheap to parse and reasonably stable.
"""
from __future__ import annotations
import os, re, html as htmllib
from typing import List, Dict
import httpx

INDEX = "https://www.stats.govt.nz/information-releases/"
_CA = (os.environ.get("REQUESTS_CA_BUNDLE")
       or os.environ.get("SSL_CERT_FILE")
       or "/etc/ssl/certs/ca-certificates.crt")
_VERIFY = _CA if os.path.exists(_CA) else True

# StatsNZ inlines the release list as HTML-entity-encoded JSON, so
# quotes appear as &quot; and slashes as \/. Match against the decoded
# text for robustness.
_SLUG_RE = re.compile(
    r'information-releases/([a-z0-9][a-z0-9-]{6,120})/'
    r'[^{}]{0,400}?"MetaDescription"\s*:\s*"([^"\\]{5,320})',
    re.IGNORECASE,
)


def scan(limit: int = 12) -> List[Dict]:
    try:
        r = httpx.get(INDEX, timeout=25, verify=_VERIFY,
                      headers={"User-Agent": "landhill-idea-radar/0.3"})
        r.raise_for_status()
    except Exception as e:  # pragma: no cover
        print(f"[statsnz] {e}")
        return []
    # Decode &quot; -> " and \/ -> / before matching.
    text = htmllib.unescape(r.text).replace("\\/", "/")
    seen = set()
    out = []
    for slug, meta in _SLUG_RE.findall(text):
        if slug in seen:
            continue
        seen.add(slug)
        title = slug.replace("-", " ").title()
        out.append({
            "title": title,
            "slug": slug,
            "url": f"https://www.stats.govt.nz/information-releases/{slug}/",
            "summary": meta.strip()[:280],
        })
        if len(out) >= limit:
            break
    return out
