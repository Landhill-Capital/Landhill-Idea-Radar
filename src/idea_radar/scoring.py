"""6-dimension scoring rubric (0-3 each, ship >= 14/18)."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict

DIMENSIONS = [
    "pain_intensity",
    "willingness_to_pay",
    "founder_market_fit",
    "unfair_local_advantage",
    "distribution_path",
    "defensibility_24mo",
]

SHIP_THRESHOLD = 14
KEEP_THRESHOLD = 12


@dataclass
class Idea:
    name: str
    source: str
    summary: str
    scores: Dict[str, int] = field(default_factory=dict)
    notes: str = ""

    @property
    def total(self) -> int:
        return sum(self.scores.get(d, 0) for d in DIMENSIONS)

    @property
    def verdict(self) -> str:
        t = self.total
        if t >= SHIP_THRESHOLD:
            return "SHIP"
        if t >= KEEP_THRESHOLD:
            return "KEEP"
        return "KILL"

    def render(self) -> str:
        lines = [f"### {self.name}  [{self.verdict} — {self.total}/18]",
                 f"_Source:_ {self.source}",
                 "",
                 self.summary,
                 "",
                 "| Dimension | Score |",
                 "| --- | ---: |"]
        for d in DIMENSIONS:
            lines.append(f"| {d.replace('_', ' ').title()} | {self.scores.get(d, 0)} |")
        if self.notes:
            lines.extend(["", f"_Notes:_ {self.notes}"])
        return "\n".join(lines)
