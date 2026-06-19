#!/usr/bin/env python3
"""Render a team's player-origins data file as text with flag emojis.

Usage:
    python render.py [team]      # team defaults to "switzerland"

Reads data/<team>.json, prints one line per player showing birthplace and each
parent's origin as flag emojis, and also writes the result to output/<team>.txt.

Everything about the layout lives in `format_player` / `render` so it's easy to
tweak. The data file is the thing you edit to add players or fix origins; add a
new team by dropping in data/<team>.json with the same shape.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from flags import country_to_flag

ROOT = Path(__file__).parent

# Markers appended after a flag to convey how sure we are of that origin.
CONFIDENCE_MARKER = {"high": "", "medium": "?", "low": "*"}


def origin_cell(country: str, confidence: str) -> str:
    """Flag emoji + a confidence marker (e.g. '🇰🇴' or '🇩🇪*')."""
    return country_to_flag(country) + CONFIDENCE_MARKER.get(confidence, "")


def format_player(player: dict, name_width: int) -> str:
    conf = player.get("confidence", {})
    birth = origin_cell(player["birth_country"], conf.get("birth", "low"))
    father = origin_cell(player["father_origin"], conf.get("father", "low"))
    mother = origin_cell(player["mother_origin"], conf.get("mother", "low"))
    name = player["name"].ljust(name_width)
    pos = player.get("position", "").ljust(3)
    return f"{birth}  {name} {pos}   👨 {father}   👩 {mother}"


def render(team: str) -> str:
    data = json.loads((ROOT / "data" / f"{team}.json").read_text(encoding="utf-8"))
    players = data["players"]
    name_width = max(len(p["name"]) for p in players)

    lines = []
    header_flag = country_to_flag(data["team"])
    lines.append(f"{header_flag}  {data['team']} — {data.get('tournament', '')}".rstrip())
    if data.get("lineup_source"):
        lines.append(f"   Lineup: {data['lineup_source']}")
    lines.append("")

    for p in players:
        lines.append(format_player(p, name_width))

    # Fun summary: every distinct origin (birth + both parents) represented.
    origins = []
    for p in players:
        for key in ("birth_country", "father_origin", "mother_origin"):
            c = p[key]
            if c.lower() not in {"unknown", ""} and c not in origins:
                origins.append(c)
    lines.append("")
    lines.append("Origins represented: " + " ".join(country_to_flag(c) for c in origins))
    lines.append(f"   ({len(origins)} countries: {', '.join(origins)})")

    lines.append("")
    lines.append("Legend: 1st flag = birthplace · 👨 father's origin · 👩 mother's origin")
    lines.append("        * = low confidence · ? = medium · 🏳️ = unknown")
    return "\n".join(lines)


def main() -> None:
    team = sys.argv[1] if len(sys.argv) > 1 else "switzerland"
    text = render(team)
    print(text)
    out_dir = ROOT / "output"
    out_dir.mkdir(exist_ok=True)
    (out_dir / f"{team}.txt").write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
