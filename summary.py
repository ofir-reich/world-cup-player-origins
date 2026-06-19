#!/usr/bin/env python3
"""Build one combined summary across all teams in data/.

For each team: a title (flag + name) and a 3-row grid — players' birth countries,
fathers' origins, mothers' origins — shown as flags only (no player names). Player
columns line up across the three rows, so each column is one player.

Outputs:
  - output/summary.html  (open in a browser; flags as flagcdn images)
  - output/summary.txt   (terminal version with flag emoji)

Run: python summary.py
"""

from __future__ import annotations

import html
import json
from pathlib import Path

from flags import country_to_flags, name_to_codes, code_to_flag

ROOT = Path(__file__).parent
DATA = ROOT / "data"

# Preferred display order; any other team files are appended alphabetically.
PREFERRED = ["switzerland", "france", "morocco", "germany", "senegal", "croatia"]
ROWS = [("Born", "birth_country"), ("Fathers", "father_origin"), ("Mothers", "mother_origin")]


def team_files() -> list[Path]:
    files = {p.stem: p for p in DATA.glob("*.json")}
    ordered = [files.pop(t) for t in PREFERRED if t in files]
    ordered += [files[k] for k in sorted(files)]
    return ordered


def load_teams() -> list[dict]:
    return [json.loads(p.read_text(encoding="utf-8")) for p in team_files()]


# --- terminal ------------------------------------------------------------------

def render_text(teams: list[dict]) -> str:
    lines = []
    for data in teams:
        title = f"{country_to_flags(data['team'])}  {data['team'].upper()}"
        lines.append(title)
        for label, key in ROWS:
            flags = " ".join(country_to_flags(p[key]) for p in data["players"])
            lines.append(f"  {label:<8} {flags}")
        lines.append("")
    return "\n".join(lines)


# --- html ----------------------------------------------------------------------

def _img(code: str) -> str:
    return (f'<img loading="lazy" src="https://flagcdn.com/h40/{code.lower()}.png" '
            f'srcset="https://flagcdn.com/h80/{code.lower()}.png 2x" alt="{code}">')


def cell_html(field: str) -> str:
    codes = name_to_codes(field)
    if not codes:
        return '<td class="flagcell"><span class="unknown">🏳️</span></td>'
    return '<td class="flagcell">' + "".join(_img(c) for c in codes) + "</td>"


def team_html(data: dict) -> str:
    title_flag = "".join(_img(c) for c in name_to_codes(data["team"]))
    head = (f'<h2><span class="title-flag">{title_flag}</span> {html.escape(data["team"])} '
            f'<span class="tour">{html.escape(data.get("tournament", ""))}</span></h2>')
    rows = []
    for label, key in ROWS:
        cells = "".join(cell_html(p[key]) for p in data["players"])
        rows.append(f'<tr><th>{label}</th>{cells}</tr>')
    return f'{head}\n<table class="grid"><tbody>\n' + "\n".join(rows) + "\n</tbody></table>"


def render_html(teams: list[dict]) -> str:
    blocks = "\n".join(team_html(t) for t in teams)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>World Cup Player Origins — Summary</title>
<style>
  :root {{ color-scheme: light dark; }}
  body {{ font-family: system-ui, sans-serif; margin: 2rem auto; max-width: 1100px;
         padding: 0 1rem; }}
  h1 {{ font-size: 1.6rem; }}
  h2 {{ font-size: 1.2rem; margin: 1.8rem 0 .5rem; display: flex; align-items: center;
        gap: .5rem; flex-wrap: wrap; }}
  .title-flag img {{ height: 1.2em; vertical-align: -0.2em; border-radius: 2px;
                     box-shadow: 0 0 0 1px #0003; }}
  .tour {{ color: #888; font-size: .8rem; font-weight: 400; }}
  table.grid {{ border-collapse: collapse; }}
  table.grid th {{ text-align: right; color: #888; font-weight: 500; font-size: .8rem;
                   text-transform: uppercase; letter-spacing: .03em; padding-right: .6rem;
                   white-space: nowrap; }}
  td.flagcell {{ padding: .2rem .22rem; text-align: center; white-space: nowrap; }}
  td.flagcell img {{ height: 1.35em; border-radius: 2px; box-shadow: 0 0 0 1px #0002;
                     margin: 0 1px; vertical-align: middle; }}
  td.flagcell .unknown {{ opacity: .5; }}
  .legend {{ color: #888; font-size: .85rem; margin-top: 2rem; }}
</style>
</head>
<body>
  <h1>🌍 World Cup Player Origins — all teams</h1>
  <p class="legend">Each column is one starter. Rows: where players were <b>born</b>,
     and where their <b>fathers</b> and <b>mothers</b> are from. Flags only — see the
     per-team pages for names, notes and confidence.</p>
{blocks}
</body>
</html>
"""


def main() -> None:
    teams = load_teams()
    out = ROOT / "output"
    out.mkdir(exist_ok=True)
    (out / "summary.html").write_text(render_html(teams), encoding="utf-8")
    text = render_text(teams)
    (out / "summary.txt").write_text(text + "\n", encoding="utf-8")
    print(text)
    print(f"Wrote {out/'summary.html'} and {out/'summary.txt'} ({len(teams)} teams)")


if __name__ == "__main__":
    main()
