"""Companies Office / NZBN signals.

There is no public real-time feed for newly-registered companies.
Options:

  1. NZBN bulk-data monthly CSVs (requires signed application,
     no anonymous download).
  2. Companies Office monthly bulk CSVs — same story.
  3. NZBN Primary Business API — free but requires a token issued
     to a registered organisation. Set NZBN_ACCESS_TOKEN in .env
     to enable.

This module implements (3) when the token is present, and otherwise
returns a soft-stubbed note so the digest still renders.
"""
from __future__ import annotations
import os
from datetime import datetime, timedelta
from typing import List, Dict
import httpx

_TOKEN = os.environ.get("NZBN_ACCESS_TOKEN", "").strip()
_CA = (os.environ.get("REQUESTS_CA_BUNDLE")
       or os.environ.get("SSL_CERT_FILE")
       or "/etc/ssl/certs/ca-certificates.crt")
_VERIFY = _CA if os.path.exists(_CA) else True

API = "https://api.business.govt.nz/services/v5/nzbn/entities"


def scan(days: int = 7, limit: int = 20) -> List[Dict]:
    if not _TOKEN:
        return [{
            "title": "NZBN API token not configured",
            "url": "https://www.nzbn.govt.nz/using-the-nzbn/nzbn-services/nzbn-api-services/",
            "summary": ("Set NZBN_ACCESS_TOKEN in .env to enable recent-registration "
                        "signals. Free after registering your organisation on the NZBN "
                        "developer portal."),
            "stub": True,
        }]
    since = (datetime.utcnow() - timedelta(days=days)).date().isoformat()
    try:
        r = httpx.get(API,
                      params={"registration-date-from": since, "page-size": limit},
                      headers={"Ocp-Apim-Subscription-Key": _TOKEN,
                               "Accept": "application/json"},
                      timeout=30, verify=_VERIFY)
        r.raise_for_status()
        data = r.json()
    except Exception as e:  # pragma: no cover
        print(f"[nzbn] {e}")
        return []
    out = []
    for item in (data.get("items") or [])[:limit]:
        out.append({
            "title": item.get("entityName") or item.get("name"),
            "nzbn": item.get("nzbn"),
            "url": f"https://www.nzbn.govt.nz/mynzbn/nzbndetails/{item.get('nzbn')}/",
            "type": item.get("entityTypeDescription"),
            "registered": item.get("registrationDate"),
        })
    return out
