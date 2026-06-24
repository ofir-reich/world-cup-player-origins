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

## Batch 2 learnings (France, Morocco, Germany, Senegal, Croatia)

**The pipeline scaled cleanly** — 55 players, ~5 needed a retry. Confirmed: do all 11
WebFetches per team in parallel, expect a couple of misses, mop up with WebSearch.

**Three distinct "origin" patterns** — worth knowing what a team's chart will *mean*:
- *Immigrant-heritage hosts* (France, Germany, Switzerland): players born in the country,
  parents from many others → colourful **parent** flags. France hit 15 origin countries.
- *Diaspora representing the homeland* (Morocco, Senegal): many players **born abroad**
  (Europe/Canada) playing for the ancestral nation → the **birth** flag differs from the team.
- *Ethnically homogeneous* (Croatia): everyone is the same ethnicity, but birthplaces still
  scatter across the diaspora (Germany, Switzerland, Bosnia) — so birth-country variety is
  NOT ethnic variety. Croatia = only 4 origins. Don't over-read these charts.

**Data-shape realities:**
- Bios often say only "to Moroccan parents" / "of Senegalese descent" with no per-parent
  detail → set **both** parents to that country at **medium** confidence. Faithful, not invented.
- **Dual heritage is common** (Franco-Algerian, Mauritanian-Senegalese, Nigerian-British).
  `flags.py` now supports **multiple flags per field** — store e.g. `"Mauritania / Senegal"`
  (separators: ` / `, ` and `, `,`). Use it for genuinely dual origins; keep nationality-only
  notes (e.g. "Nigerian-British") in the `note`, single flag.
- **Birthplace can be disputed** (Nicolas Jackson: Gambia vs Senegal) → mark `medium` + note.

**URL gotchas confirmed & how to dodge:**
- Accented titles sometimes 404 (`Ismaël_Saibari` failed; `Ismael_Saibari` worked). Retry
  without diacritics.
- Common names land on **disambiguation pages** (Issa Diop) or need a qualifier
  (`Nathaniel_Brown` vs `..._(footballer)`). When WebFetch returns a disambiguation/404,
  fall back to WebSearch — it resolves both the right person and the heritage in one call.

**New flag cases handled in `flags.py`:** overseas territories (French Guiana `GF`,
Guadeloupe `GP`), UK home nations (England `GB-ENG` via Unicode tag sequence / flagcdn
`gb-eng`), and parenthetical stripping (`"Croatia (Zadar)"` → Croatia).

## Doing all 48 teams (when we get there)

- One `data/<team>.json` per team; the renderers already take a team arg.
- Batch the 11 WebFetches per team in parallel; process a few teams per turn.
- Pre-resolve player Wikipedia URLs from each team's squad page to cut 404 retries.
- Heritage-rich teams (France, Morocco, Switzerland, Germany, Senegal) are the most
  interesting output; mono-origin teams will be mostly one flag — that's fine/expected.
- Consider a `render_html.py all` later that builds one combined page.

## All 48 teams — DONE. How the full run actually went

**One Sonnet subagent per team, run in parallel waves**, each agent doing the entire
lineup-search → 11×WebFetch → write-`data/<team>.json` pipeline and returning only a
2-line summary. This keeps the orchestrator's context tiny (no raw bios in the main thread)
and is the single biggest win for doing many teams. The orchestrator only validates +
commits. ~40–65k subagent tokens / team; matches the earlier "~13–16 tool calls" estimate.

**Pacing against the account session limit was the real constraint, not money.**
- Firing **8 agents at once repeatedly trips the session rate limit** — whole waves came
  back with "you've hit your session limit · resets <time>" and wrote nothing.
- The limit is **time-based, not credit-based**: more credits don't lift it; you wait for
  the reset. But it also **eases within minutes** after a burst — a single-agent *probe*
  reliably told us whether to resume.
- **What worked: batches of 3.** Launch 3 → validate → commit+push → launch next 3.
  Gentle enough to avoid re-tripping, still parallel. Always `git push` each batch so a
  mid-wave limit never loses committed work (the working tree was always clean on resume —
  killed agents wrote nothing partial).

**Subagent prompt rules that mattered:**
- Web tools are **intermittently permission-denied for subagents**; tell each agent to
  **retry a denied WebSearch/WebFetch up to ~5×** (denials are transient) and to fall back
  to a **Bash heredoc if `Write` is denied**. Without this, agents bailed on the first deny.
- Restate the **parent-must-be-foreign-*born*** rule in every prompt. Agents otherwise
  flag grandparent-level ancestry/citizenship-by-descent. Caught & corrected by hand:
  Aiden O'Neill (AUS, NI *citizenship* via father → kept Australia). Good catches the
  agents made unprompted: Rice/Gordon (ENG), Gyökeres (SWE), Schick (CZE) — descent only.

**Flag overrides added during the run** (pycountry misses these): `Palestine`→`PS`,
`Russia`→`RU` (pycountry only knows "Russian Federation"), `Northern Ireland`→`GB-NIR`
(flagcdn serves `gb-nir.png`; no NI emoji exists so terminal shows white flag — HTML is
the canonical renderer). **Always run a full-sweep `name_to_codes` check over all teams
before the final commit** — that's how these surfaced.

**Validation harness per batch** (cheap, catches everything):
`for each new team: assert 11 players; every birth/father/mother resolves via name_to_codes
(excluding the intentional "unknown" sentinel).` Then `python summary.py` + commit.
