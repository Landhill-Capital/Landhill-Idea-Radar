"""Trade Me signals — persistent unfilled listings by category.

Trade Me's API requires OAuth1 with a consumer key/secret issued to a
Trade Me member. Commercial use additionally requires written approval.

We ship the code path but keep it disabled unless the four env vars
(TRADEME_CONSUMER_KEY / _SECRET / TRADEME_OAUTH_TOKEN / _SECRET) are
present. Without keys, the source returns a stub so the digest still
renders and the user knows how to enable it.
"""
from __future__ import annotations
import os
from typing import List, Dict
import httpx

_CK = os.environ.get("TRADEME_CONSUMER_KEY", "")
_CS = os.environ.get("TRADEME_CONSUMER_SECRET", "")
_TK = os.environ.get("TRADEME_OAUTH_TOKEN", "")
_TS = os.environ.get("TRADEME_OAUTH_TOKEN_SECRET", "")
_CA = (os.environ.get("REQUESTS_CA_BUNDLE")
       or os.environ.get("SSL_CERT_FILE")
       or "/etc/ssl/certs/ca-certificates.crt")
_VERIFY = _CA if os.path.exists(_CA) else True

# Broad "services" categories are the best pain-signal proxy: recurring
# demand for local providers who can't be found.
DEFAULT_CATEGORIES = [
    ("Services", "5349"),   # top-level Services
    ("Business for sale", "6379"),
]


def _oauth_header() -> str:
    """Minimal OAuth1 for a two-legged request. Real deployments should
    use requests_oauthlib; this stub only fires when all four keys are
    set, so we defer to that library if available."""
    try:
        from requests_oauthlib import OAuth1
        return "REQUESTS_OAUTHLIB_AVAILABLE"
    except ImportError:
        return ""


def scan(limit: int = 15) -> List[Dict]:
    if not all([_CK, _CS, _TK, _TS]):
        return [{
            "title": "Trade Me API not configured",
            "url": "https://developer.trademe.co.nz/api-overview/authentication",
            "summary": ("Set TRADEME_CONSUMER_KEY / _SECRET / OAUTH_TOKEN / "
                        "OAUTH_TOKEN_SECRET in .env to enable Trade Me signals. "
                        "Personal-use keys are free from developer.trademe.co.nz. "
                        "Commercial use needs written approval from Trade Me."),
            "stub": True,
        }]
    try:
        from requests_oauthlib import OAuth1
    except ImportError:
        return [{"title": "requests_oauthlib not installed", "url": "", "stub": True,
                 "summary": "pip install requests-oauthlib to enable Trade Me signals."}]
    auth = OAuth1(_CK, _CS, _TK, _TS, signature_type="auth_header")
    out = []
    for label, cat in DEFAULT_CATEGORIES:
        url = f"https://api.trademe.co.nz/v1/Search/General.json"
        try:
            # httpx doesn't accept requests-oauthlib auth objects; use their
            # header prep manually via a requests fallback.
            import requests
            r = requests.get(url, params={"category": cat, "sort_order": "ExpiryDesc",
                                          "rows": limit}, auth=auth, timeout=25,
                             verify=_VERIFY)
            r.raise_for_status()
            data = r.json()
        except Exception as e:  # pragma: no cover
            print(f"[trademe/{label}] {e}")
            continue
        for listing in (data.get("List") or [])[:limit]:
            out.append({
                "title": listing.get("Title"),
                "category": label,
                "url": f"https://www.trademe.co.nz/a/marketplace/listing/{listing.get('ListingId')}",
                "region": listing.get("Region"),
                "price": listing.get("PriceDisplay"),
            })
    return out
