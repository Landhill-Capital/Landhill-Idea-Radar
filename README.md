# Landhill Idea Radar

A small internal tool that helps [Landhill Capital](https://landhillcap.com)
generate feasible business ideas **continuously** rather than by lucky
brainstorm. It ingests weak signals from public sources, ranks anomalies,
and produces a weekly markdown digest that plugs into the Landhill weekly
cadence (see the *"How to Generate Good Business Ideas"* guide in Drive).

## Why

Ideas are cheap. Observed pain, moving money, and unfair founder-market
fit are rare. The Radar filters signals for the rare three, not the
cheap one.

## Signals ingested

| Source | Signal | Status |
| --- | --- | --- |
| Reddit (r/newzealand, r/PersonalFinanceNZ, r/AucklandNZ, r/wellington, industry subs) | Recurring complaints / "does anyone know a good X" | v0.1 |
| Product Hunt | Daily launches, upvote velocity | v0.1 |
| Y Combinator | Recent batch launches | v0.2 |
| Google Trends NZ | Rising queries (NZ region) | v0.2 |
| StatsNZ business demography | Sector growth deltas | v0.3 |
| IRD BIC | Industry activity | v0.3 |
| Companies Office | Recent registrations | v0.3 |
| Trade Me | Persistent unfilled categories | v0.3 |

## Weekly output

`reports/YYYY-MM-DD-digest.md` — a curated 1-page markdown digest with:

1. **Top 5 pain signals** this week (with citations).
2. **Top 3 arbitrage candidates** (NZ gap vs global product).
3. **Top 3 "boring but moving money"** signals.
4. **Scoring rubric applied** to any candidate ≥ 12/18 (rubric in guide).

The digest is optionally piped into the Wednesday-Scan email delivered
by the Hermes cron job.

## Layout

```
Landhill-Idea-Radar/
├── README.md
├── LICENSE
├── pyproject.toml
├── src/
│   └── idea_radar/
│       ├── __init__.py
│       ├── cli.py               # `idea-radar run --week`
│       ├── config.py            # signal source registry
│       ├── digest.py            # markdown digest writer
│       ├── scoring.py           # 6-dim rubric
│       └── sources/
│           ├── __init__.py
│           ├── reddit.py
│           ├── producthunt.py
│           ├── ycombinator.py
│           ├── google_trends.py
│           └── statsnz.py
├── reports/                     # generated digests (git-tracked)
│   └── .gitkeep
└── tests/
```

## Usage

```bash
# Install (editable)
pip install -e .

# Configure secrets — copy .env.example to .env
cp .env.example .env

# Run the weekly digest
idea-radar run --week 2026-W29

# Latest digest
idea-radar latest
```

## The scoring rubric (0–3 per dimension, ship ≥ 14/18)

1. Pain intensity
2. Willingness to pay
3. Founder-market fit
4. Unfair local advantage (NZ-specific)
5. Distribution path clarity
6. 24-month defensibility

## Status

**v0.1 scaffold** — Reddit + Product Hunt live; other sources
stubbed. Contributions from anyone at Landhill welcome.

## License

MIT — see `LICENSE`.
