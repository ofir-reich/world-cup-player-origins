# World Cup Player Origins 🌍⚽

A small, fun tool that visualizes a national team's starting XI by the **origins**
of its players — where each player was born and where each parent comes from —
rendered as **flag emojis**.

Prototype team: **Switzerland** (2026 FIFA World Cup).

## Run

```bash
python render.py            # defaults to switzerland
python render.py switzerland
```

No dependencies required. `pip install -r requirements.txt` (pycountry) is optional
and just extends country-name coverage for when you add more teams.

Output prints to the terminal and is also written to `output/<team>.txt`.

Example line:

```
🇨🇭  Granit Xhaka   MF    👨 🇽🇰   👩 🇽🇰
```

The first flag is the player's birthplace; 👨 / 👩 are the father's and mother's
origins. A `*` means low confidence, `?` medium, 🏳️ unknown.

## How it works

```
data/<team>.json  →  render.py (+ flags.py)  →  text with flag emojis
```

- **`data/<team>.json`** — the curated data: each player's birthplace and parents'
  origins, each with a `high`/`medium`/`low` confidence. This is the file you edit
  by hand to fix or extend things.
- **`flags.py`** — maps a country name → ISO alpha-2 code → flag emoji. Has a
  built-in map (incl. **Kosovo 🇽🇰**, which isn't a real ISO country) and falls back
  to `pycountry` if installed.
- **`render.py`** — formats and prints; layout lives in `format_player` / `render`
  so it's easy to tweak.
- **`sources/`** — the raw lineup and notes the data was built from.

## Add another team

1. Create `data/<team>.json` with the same shape as `data/switzerland.json`.
2. `python render.py <team>`.

## Data & caveats

Origins were gathered from Wikipedia and web search. Birthplaces are well
documented; **parents' origins are often not** — where a player has a plain Swiss
surname and no documented heritage, the parents are assumed Swiss and marked low
confidence (`*`). Surname-based guesses are never presented as fact.
