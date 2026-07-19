"""Assemble the weekly markdown digest."""
from __future__ import annotations
from datetime import datetime
from pathlib import Path
from typing import List, Dict

from .sources import reddit, producthunt
from .config import DIGEST_TOP_PAIN


def build(week_label: str | None = None) -> str:
    week = week_label or datetime.utcnow().strftime("%Y-W%V")
    pain = reddit.scan()[:DIGEST_TOP_PAIN]
    launches = producthunt.scan(limit=10)

    out = [f"# Landhill Idea Radar — {week}",
           f"_generated {datetime.utcnow().isoformat(timespec='seconds')}Z_",
           "",
           "## 1. Top NZ pain signals (Reddit)",
           ""]
    if not pain:
        out.append("_no matches this week_")
    for h in pain:
        out.append(f"- **r/{h['sub']}** — [{h['title']}]({h['url']})  ")
        out.append(f"  score {h['score']} • {h['num_comments']} comments")
        if h["excerpt"]:
            out.append(f"  > {h['excerpt']}")
        out.append("")

    out += ["## 2. Product Hunt arbitrage candidates (last 7 days)", ""]
    for l in launches:
        out.append(f"- [{l['title']}]({l['url']})")
        if l["summary"]:
            out.append(f"  {l['summary']}")

    out += ["",
            "## 3. Rubric reminder",
            "Score each candidate on: pain intensity, willingness to pay,",
            "founder-market fit, unfair local advantage, distribution path,",
            "24-month defensibility. Ship at 14/18.",
            ""]
    return "\n".join(out)


def write(week_label: str | None = None, root: Path | None = None) -> Path:
    root = root or Path(__file__).resolve().parents[2] / "reports"
    root.mkdir(exist_ok=True)
    date = datetime.utcnow().strftime("%Y-%m-%d")
    path = root / f"{date}-digest.md"
    path.write_text(build(week_label))
    return path
