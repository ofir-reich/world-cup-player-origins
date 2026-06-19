#!/usr/bin/env python3
"""Render a team's player-origins data file as a standalone HTML page.

Usage:
    python render_html.py [team]      # team defaults to "switzerland"

Why HTML instead of the terminal: flag *emoji* only render if the OS/terminal
font ships flag glyphs (many Linux setups don't, so you see "CH" instead of 🇨🇭).
This page draws each flag as an <img> from flagcdn.com keyed by ISO alpha-2 code,
so flags render identically in any browser — and it includes Kosovo (xk), which
most emoji fonts omit.

Writes output/<team>.html. Open it in any web browser (needs internet for the
flag images).
"""

from __future__ import annotations

import html
import json
import sys
from pathlib import Path

from flags import name_to_codes, code_to_flag

ROOT = Path(__file__).parent

CONF_TITLE = {"high": "high confidence", "medium": "medium confidence", "low": "low confidence"}


def _img(code: str, label: str) -> str:
    return (
        f'<img loading="lazy" src="https://flagcdn.com/h40/{code.lower()}.png" '
        f'srcset="https://flagcdn.com/h80/{code.lower()}.png 2x" alt="{label}">'
    )


def flag_img(field: str, confidence: str = "high") -> str:
    """One or more <img> flags for an origin field, or a 🏳️ chip if unknown."""
    codes = name_to_codes(field)
    label = html.escape(field)
    if not codes:
        return '<span class="flag unknown" title="unknown">🏳️</span>'
    dim = " low" if confidence == "low" else ""
    marker = {"low": " *", "medium": " ?"}.get(confidence, "")
    imgs = "".join(_img(c, label) for c in codes)
    return (
        f'<span class="flag{dim}" title="{label} ({CONF_TITLE.get(confidence, confidence)})">'
        f'{imgs}<span class="marker">{marker}</span></span>'
    )


def player_row(p: dict) -> str:
    conf = p.get("confidence", {})
    name = html.escape(p["name"])
    pos = html.escape(p.get("position", ""))
    return f"""    <tr>
      <td class="birth">{flag_img(p['birth_country'], conf.get('birth', 'low'))}</td>
      <td class="name">{name}</td>
      <td class="pos">{pos}</td>
      <td class="parent">{flag_img(p['father_origin'], conf.get('father', 'low'))}</td>
      <td class="parent">{flag_img(p['mother_origin'], conf.get('mother', 'low'))}</td>
    </tr>"""


def render(team: str) -> str:
    data = json.loads((ROOT / "data" / f"{team}.json").read_text(encoding="utf-8"))
    players = data["players"]
    title = html.escape(f"{data['team']} — {data.get('tournament', '')}")
    lineup = html.escape(data.get("lineup_source", ""))

    # Distinct origins represented (deduped by ISO code).
    codes: list[str] = []
    for p in players:
        for key in ("birth_country", "father_origin", "mother_origin"):
            for code in name_to_codes(p[key]):
                if code not in codes:
                    codes.append(code)
    origins_html = "".join(
        f'<span class="flag">{_img(c, c)}</span>' for c in codes
    )

    rows = "\n".join(player_row(p) for p in players)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
  :root {{ color-scheme: light dark; }}
  body {{ font-family: system-ui, sans-serif; max-width: 720px; margin: 2rem auto;
         padding: 0 1rem; line-height: 1.5; }}
  h1 {{ font-size: 1.5rem; margin-bottom: .2rem; }}
  .sub {{ color: #888; font-size: .9rem; margin-bottom: 1.5rem; }}
  table {{ border-collapse: collapse; width: 100%; }}
  td {{ padding: .45rem .5rem; border-bottom: 1px solid #8884; vertical-align: middle; }}
  .name {{ font-weight: 600; width: 100%; }}
  .pos {{ color: #888; font-variant: small-caps; text-align: center; }}
  th {{ text-align: left; color: #888; font-weight: 500; font-size: .8rem;
        text-transform: uppercase; letter-spacing: .04em; padding: .3rem .5rem; }}
  .flag img {{ height: 1.4em; vertical-align: -0.25em; border-radius: 2px;
               box-shadow: 0 0 0 1px #0002; }}
  .flag.low {{ opacity: .55; }}
  .flag .marker {{ color: #c33; font-weight: 700; }}
  .flag.unknown {{ opacity: .5; }}
  .origins {{ margin: 1.5rem 0; font-size: 1.3rem; }}
  .origins .flag img {{ height: 1.3em; margin: 0 .1em; }}
  .legend {{ color: #888; font-size: .85rem; margin-top: 1.5rem; }}
</style>
</head>
<body>
  <h1>{title}</h1>
  <div class="sub">Lineup: {lineup}</div>
  <table>
    <thead><tr><th>Born</th><th>Player</th><th>Pos</th><th>👨 Father</th><th>👩 Mother</th></tr></thead>
    <tbody>
{rows}
    </tbody>
  </table>
  <div class="origins">Origins represented ({len(codes)}): {origins_html}</div>
  <div class="legend">
    First flag = birthplace · 👨 father's origin · 👩 mother's origin.<br>
    <b>*</b> = low confidence (faded), <b>?</b> = medium, 🏳️ = unknown.
  </div>
</body>
</html>
"""


def main() -> None:
    team = sys.argv[1] if len(sys.argv) > 1 else "switzerland"
    out_dir = ROOT / "output"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / f"{team}.html"
    out_path.write_text(render(team), encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
