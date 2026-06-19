# Learnings — building this well (for future runs)

Captured from the Switzerland pilot. Read this before doing more teams.

## Pipeline that worked

1. **Lineup**: one `WebSearch` of `"<TEAM> starting lineup 2026 World Cup latest match"`
   returns a clean XI + formation. Save to `sources/lineup.txt`.
2. **Extract origins**: `WebFetch` `https://en.wikipedia.org/wiki/<Player_Name>` with a
   strict "return ONLY JSON" prompt (birth/father/mother + per-field confidence + a
   short quoted note). WebFetch already runs a small/fast model, so this *is* the
   "use a cheaper model for extraction" step — no separate Haiku subagent needed.
   This collapsed the planned steps 2+3 into one.
3. **Fill gaps**: for any `unknown` parent, one targeted `WebSearch`
   `"<player> parents heritage origin"` usually resolves it (bio sites, club profiles).
4. **Render**: data → `render.py` (terminal) / `render_html.py` (browser).

Cost per team ≈ **1 lineup search + 11 WebFetch + ~2–4 gap searches ≈ 13–16 tool calls.**

## Gotchas

- **Accented / common names 404 on Wikipedia.** `Ricardo_Rodríguez_(footballer,_born_1992)`
  failed (URL-encoding of `í`). Fix: when a WebFetch 404s, `WebSearch` the player and
  use the bio results, or grab the disambiguated title from the team's squad page first.
  Doing **all 11 WebFetches in parallel** is fine and fast; just expect 1–2 to need a retry.
- **Parents' origins are frequently absent** from the Wikipedia lead/infobox. WebFetch
  correctly returns `unknown` — don't let it guess. The follow-up search fills most.
- **Plain host-nation surname + no documented heritage** → assume host nation, mark
  **low confidence** (`*`). Never present surname inference as fact.
- **Flag rendering**: terminal emoji are unreliable (many Linux fonts lack flag glyphs →
  you see "CH"). Use **`render_html.py`**, which draws flags as `flagcdn.com` images keyed
  by ISO alpha-2. Renders identically everywhere.
- **Kosovo** is not an ISO country: it needs the `XK` override in `flags.py`, and emoji /
  Twemoji often omit it — `flagcdn.com/.../xk.png` exists, which is why the HTML path is
  preferred over emoji.

## Confidence conventions (keep honest)

- `high` — explicitly stated in a source ("born in X to a Nigerian father").
- `medium` — implied / from a less authoritative source.
- `low` — surname inference or assumed-same-as-birth-country. Renders faded + `*`.

## Doing all 48 teams (when we get there)

- One `data/<team>.json` per team; the renderers already take a team arg.
- Batch the 11 WebFetches per team in parallel; process a few teams per turn.
- Pre-resolve player Wikipedia URLs from each team's squad page to cut 404 retries.
- Heritage-rich teams (France, Morocco, Switzerland, Germany, Senegal) are the most
  interesting output; mono-origin teams will be mostly one flag — that's fine/expected.
- Consider a `render_html.py all` later that builds one combined page.
