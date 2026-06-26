#!/usr/bin/env python3
"""Build combined summaries across all teams in data/.

For each team: a title (flag + name) and a grid of flag-only rows. Player columns
line up across rows, so each column is one player. Three variants are produced:

  summary           — rows labelled "Born / Fathers / Mothers" (the original)
  summary_emoji     — same three rows, but labelled with 👶 / 👨 / 👩 + a legend
  summary_born      — only the "Born" row (parents omitted)
  summary_born_emoji — only the "Born" row, labelled with 👶 + a legend

Each variant is written as both .html (flagcdn images) and .txt (flag emoji):
  output/summary.html / .txt
  output/summary_emoji.html / .txt
  output/summary_born.html / .txt
  output/summary_born_emoji.html / .txt

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

# Row sets: (label, json_key). Label is what's shown in the left gutter.
ROWS_FULL = [("Born", "birth_country"), ("Fathers", "father_origin"), ("Mothers", "mother_origin")]
ROWS_EMOJI = [("👶", "birth_country"), ("👨", "father_origin"), ("👩", "mother_origin")]
ROWS_BORN = [("Born", "birth_country")]
ROWS_BORN_EMOJI = [("👶", "birth_country")]

# Legends (plain text and HTML) per variant.
_LEGEND_FULL_TXT = ("Each column is one starter. Rows: where players were born, and "
                    "where their fathers and mothers are from.")
_LEGEND_FULL_HTML = ('Each column is one starter. Rows: where players were <b>born</b>, '
                     'and where their <b>fathers</b> and <b>mothers</b> are from. Flags '
                     'only — see the per-team pages for names, notes and confidence.')
_LEGEND_EMOJI_TXT = ("Legend:  👶 = where the player was born   👨 = father's origin   "
                     "👩 = mother's origin.   Each column is one starter.")
_LEGEND_EMOJI_HTML = ('Legend: <b>👶</b> = where the player was born &nbsp;·&nbsp; '
                      '<b>👨</b> = father’s origin &nbsp;·&nbsp; '
                      '<b>👩</b> = mother’s origin. Each column is one starter. '
                      'Flags only — see the per-team pages for names and confidence.')
_LEGEND_BORN_TXT = ("Each column is one starter, shown by where they were born. "
                    "(Parents' origins omitted — see the full summary for those.)")
_LEGEND_BORN_HTML = ('Each column is one starter, shown by where they were <b>born</b>. '
                     'Parents’ origins are omitted here — see the full summary for those.')
_LEGEND_BORN_EMOJI_TXT = ("Legend:  👶 = where the player was born.   Each column is one "
                          "starter.   (Parents' origins omitted.)")
_LEGEND_BORN_EMOJI_HTML = ('Legend: <b>👶</b> = where the player was born. Each column is '
                           'one starter. Parents’ origins are omitted here — see the full '
                           'summary for those.')

# name, rows, plain-text legend, html legend, compact-text
# compact=True trims the .txt output (emoji label glued to flags, no spaces between
# flags) so a team fits on one line — handy for pasting into WhatsApp/chat.
VARIANTS = [
    ("summary", ROWS_FULL, _LEGEND_FULL_TXT, _LEGEND_FULL_HTML, False),
    ("summary_emoji", ROWS_EMOJI, _LEGEND_EMOJI_TXT, _LEGEND_EMOJI_HTML, True),
    ("summary_born", ROWS_BORN, _LEGEND_BORN_TXT, _LEGEND_BORN_HTML, False),
    ("summary_born_emoji", ROWS_BORN_EMOJI, _LEGEND_BORN_EMOJI_TXT, _LEGEND_BORN_EMOJI_HTML, True),
]


def team_files() -> list[Path]:
    files = {p.stem: p for p in DATA.glob("*.json")}
    ordered = [files.pop(t) for t in PREFERRED if t in files]
    ordered += [files[k] for k in sorted(files)]
    return ordered


def load_teams() -> list[dict]:
    return [json.loads(p.read_text(encoding="utf-8")) for p in team_files()]


# --- terminal ------------------------------------------------------------------

def render_text(teams: list[dict], rows: list[tuple[str, str]], legend: str,
                compact: bool = False) -> str:
    lines = [legend, ""]
    for data in teams:
        sep = " " if compact else "  "
        lines.append(f"{country_to_flags(data['team'])}{sep}{data['team'].upper()}")
        for label, key in rows:
            if compact:  # glue label to flags, no spaces — fits one chat line
                flags = "".join(country_to_flags(p[key]) for p in data["players"])
                lines.append(f"{label}{flags}")
            else:
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


def team_html(data: dict, rows: list[tuple[str, str]]) -> str:
    title_flag = "".join(_img(c) for c in name_to_codes(data["team"]))
    head = (f'<h2><span class="title-flag">{title_flag}</span> {html.escape(data["team"])} '
            f'<span class="tour">{html.escape(data.get("tournament", ""))}</span></h2>')
    body = []
    for label, key in rows:
        cells = "".join(cell_html(p[key]) for p in data["players"])
        body.append(f'<tr><th>{html.escape(label)}</th>{cells}</tr>')
    return f'{head}\n<table class="grid"><tbody>\n' + "\n".join(body) + "\n</tbody></table>"


def render_html(teams: list[dict], rows: list[tuple[str, str]], legend_html: str) -> str:
    blocks = "\n".join(team_html(t, rows) for t in teams)
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
  table.grid th {{ text-align: right; color: #888; font-weight: 500; font-size: .9rem;
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
  <p class="legend">{legend_html}</p>
{blocks}
</body>
</html>
"""


def main() -> None:
    teams = load_teams()
    out = ROOT / "output"
    out.mkdir(exist_ok=True)
    for name, rows, legend_txt, legend_html, compact in VARIANTS:
        (out / f"{name}.html").write_text(render_html(teams, rows, legend_html), encoding="utf-8")
        (out / f"{name}.txt").write_text(
            render_text(teams, rows, legend_txt, compact) + "\n", encoding="utf-8")
    names = ", ".join(name for name, *_ in VARIANTS)
    print(f"Wrote {len(VARIANTS)} variants ({names}) "
          f"× (.html + .txt) to {out}/ for {len(teams)} teams.")


if __name__ == "__main__":
    main()
