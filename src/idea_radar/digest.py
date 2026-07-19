"""Assemble the weekly markdown digest."""
from __future__ import annotations
from datetime import datetime
from pathlib import Path
from typing import List, Dict

from .sources import reddit, producthunt, ycombinator, google_trends, statsnz, companies_office, trademe
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
        out.append(f"- **r/{h['sub']}** — [{h['title']}]({h['url']})")
        if h.get("excerpt"):
            out.append(f"  > {h['excerpt']}")
        out.append("")

    out += ["## 2. Product Hunt arbitrage candidates (last 7 days)", ""]
    for l in launches:
        out.append(f"- [{l['title']}]({l['url']})")
        if l["summary"]:
            out.append(f"  {l['summary']}")

    yc = ycombinator.scan(limit=10)
    out += ["", "## 3. Show HN launches (YC-adjacent)", ""]
    if not yc:
        out.append("_no launches returned_")
    for l in yc:
        pts = f" · {l['points']}pts · {l['comments']} comments" if l.get("points") is not None else ""
        out.append(f"- [{l['title']}]({l['url']}){pts} · [HN]({l['hn_url']})")

    trends = google_trends.scan(limit=10)
    out += ["", "## 4. Google Trends NZ — rising queries", ""]
    if not trends:
        out.append("_no rising queries returned_")
    for t in trends:
        traffic = f" ({t['approx_traffic']})" if t.get("approx_traffic") else ""
        out.append(f"- **{t['query']}**{traffic}")

    releases = statsnz.scan(limit=8)
    out += ["", "## 5. StatsNZ — latest information releases", ""]
    if not releases:
        out.append("_no releases returned_")
    for rel in releases:
        out.append(f"- [{rel['title']}]({rel['url']})")
        if rel.get("summary"):
            out.append(f"  {rel['summary']}")

    regs = companies_office.scan(days=7, limit=10)
    out += ["", "## 6. Companies Office / NZBN — recent registrations", ""]
    for reg in regs:
        if reg.get("stub"):
            out.append(f"- _{reg['title']}_ — [enable]({reg['url']})")
            if reg.get("summary"):
                out.append(f"  {reg['summary']}")
        else:
            when = f" · registered {reg.get('registered')}" if reg.get("registered") else ""
            out.append(f"- [{reg['title']}]({reg['url']}) — {reg.get('type','')}{when}")

    tm = trademe.scan(limit=10)
    out += ["", "## 7. Trade Me — service/business categories", ""]
    for l in tm:
        if l.get("stub"):
            out.append(f"- _{l['title']}_ — [enable]({l['url']})")
            if l.get("summary"):
                out.append(f"  {l['summary']}")
        else:
            price = f" · {l['price']}" if l.get("price") else ""
            region = f" · {l['region']}" if l.get("region") else ""
            out.append(f"- [{l['title']}]({l['url']}) · {l.get('category','')}{region}{price}")

    out += ["",
            "## 8. Rubric reminder",
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
