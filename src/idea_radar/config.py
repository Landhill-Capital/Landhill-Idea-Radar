"""Signal source registry and defaults."""
from __future__ import annotations

# NZ-flavoured Reddit subs to scan for recurring pain signals.
REDDIT_SUBS = [
    "newzealand",
    "PersonalFinanceNZ",
    "AucklandNZ",
    "wellington",
    "chch",
    "tradieNZ",
    "smallbusiness",
]

# Phrases that flag latent demand / pain in a Reddit post title or body.
PAIN_PATTERNS = [
    r"\bwhy is\b.*\bso (?:hard|expensive|annoying|slow)\b",
    r"\bdoes anyone know a good\b",
    r"\bI wish there was\b",
    r"\bhow do (?:you|kiwis|nzers)\b",
    r"\bwe still (?:use|do this in) (?:a )?(?:spreadsheet|fax|paper)\b",
    r"\brecommend(?:ation)? for\b",
    r"\bcan't believe\b.*\bstill\b",
]

# Product Hunt: recent-launch cutoff (days).
PH_LOOKBACK_DAYS = 7

# Weekly digest defaults.
DIGEST_TOP_PAIN = 5
DIGEST_TOP_ARBITRAGE = 3
DIGEST_TOP_BORING = 3
