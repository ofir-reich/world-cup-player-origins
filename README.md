# World Cup Player Origins 🌍⚽

A small, fun tool that visualizes a national team's starting XI by the **origins**
of its players — where each player was born and where each parent comes from —
rendered as **flag emojis**.

Teams: **all 48 of the 2026 FIFA World Cup** — see `data/` (one `<team>.json` each).

## Run

```bash
python render.py            # defaults to switzerland
python render.py france     # any team — match the data/<team>.json stem
python render_html.py france # browser version (flag images)
python summary.py            # all 48 teams — four variants (output/summary*.html + .txt)
```

The combined `output/summary.html` (all 48 teams) is the headline view — open it in a
browser. Per-team pages have names, notes and confidence markers.

`summary.py` builds a combined grid: each team titled with its flag, then flag-only
rows, with player columns aligned so each column is one starter. It writes **four
variants** (each as `.html` + `.txt`):

- `summary` — rows labelled **Born / Fathers / Mothers**.
- `summary_emoji` — the same three rows labelled **👶 / 👨 / 👩** with a legend at the top.
- `summary_born` — **only the Born row** (parents omitted).
- `summary_born_emoji` — only the Born row, labelled **👶** with a legend at the top.

### Where the starters were born (all 48 teams)

Each column is one starter, shown by where they were **born** (parents' origins omitted —
run `summary.py` for the full version).

<details>
<summary>Show all 48 teams</summary>

```
🇨🇭  SWITZERLAND
  Born  🇨🇭 🇨🇭 🇨🇭 🇨🇭 🇨🇭 🇨🇭 🇨🇭 🇨🇭 🇨🇭 🇨🇲 🇨🇭
🇫🇷  FRANCE
  Born  🇬🇫 🇫🇷 🇫🇷 🇫🇷 🇫🇷 🇫🇷 🇫🇷 🏴󠁧󠁢󠁥󠁮󠁧󠁿 🇫🇷 🇫🇷 🇫🇷
🇲🇦  MOROCCO
  Born  🇨🇦 🇪🇸 🇪🇸 🇫🇷 🇳🇱 🇫🇷 🇫🇷 🇪🇸 🇧🇪 🇲🇦 🇪🇸
🇩🇪  GERMANY
  Born  🇩🇪 🇩🇪 🇩🇪 🇩🇪 🇩🇪 🇩🇪 🇩🇪 🇩🇪 🇩🇪 🇩🇪 🇩🇪
🇸🇳  SENEGAL
  Born  🇫🇷 🇸🇳 🇫🇷 🇫🇷 🇸🇳 🇸🇳 🇫🇷 🇸🇳 🇸🇳 🇸🇳 🇬🇲
🇭🇷  CROATIA
  Born  🇭🇷 🇭🇷 🇧🇦 🇭🇷 🇩🇪 🇭🇷 🇩🇪 🇧🇦 🇭🇷 🇨🇭 🇭🇷
🇩🇿  ALGERIA
  Born  🇫🇷 🇧🇪 🇫🇷 🇩🇿 🇫🇷 🇩🇿 🇳🇱 🇩🇪 🇫🇷 🇩🇿 🇫🇷
🇦🇷  ARGENTINA
  Born  🇦🇷 🇦🇷 🇦🇷 🇦🇷 🇦🇷 🇦🇷 🇦🇷 🇦🇷 🇦🇷 🇦🇷 🇦🇷
🇦🇺  AUSTRALIA
  Born  🇦🇺 🇮🇹 🏴󠁧󠁢󠁳󠁣󠁴󠁿 🏴󠁧󠁢󠁳󠁣󠁴󠁿 🇦🇺 🇦🇺 🇦🇺 🇦🇺 🇧🇪 🇹🇿 🇬🇳
🇦🇹  AUSTRIA
  Born  🇦🇹 🇦🇹 🇦🇹 🇦🇹 🇦🇹 🇦🇹 🇦🇹 🇦🇹 🇦🇹 🇦🇹 🇦🇹
🇧🇪  BELGIUM
  Born  🇧🇪 🇧🇪 🇧🇪 🇧🇪 🇧🇪 🇧🇪 🇧🇪 🇧🇪 🇧🇪 🇧🇪 🇧🇪
🇧🇦  BOSNIA AND HERZEGOVINA
  Born  🇧🇦 🇦🇹 🇧🇦 🇸🇪 🇩🇪 🇩🇪 🇧🇦 🇸🇪 🇧🇦 🇧🇦 🇩🇪
🇧🇷  BRAZIL
  Born  🇧🇷 🇧🇷 🇧🇷 🇧🇷 🇧🇷 🇧🇷 🇧🇷 🇧🇷 🇧🇷 🇧🇷 🇧🇷
🇨🇦  CANADA
  Born  🇨🇦 🇨🇦 🏴󠁧󠁢󠁥󠁮󠁧󠁿 🇨🇦 🇨🇦 🇨🇦 🇨🇦 🇨🇮 🇨🇦 🇺🇸 🇨🇦
🇨🇻  CAPE VERDE
  Born  🇨🇻 🇵🇹 🇮🇪 🇨🇻 🇳🇱 🇨🇻 🇳🇱 🇵🇹 🇨🇻 🇨🇻 🇨🇻
🇨🇴  COLOMBIA
  Born  🇨🇴 🇨🇴 🇨🇴 🇨🇴 🇨🇴 🇨🇴 🇨🇴 🇨🇴 🇨🇴 🇨🇴 🇨🇴
🇨🇼  CURAÇAO
  Born  🇳🇱 🇳🇱 🇳🇱 🇳🇱 🇳🇱 🇳🇱 🇳🇱 🇳🇱 🇳🇱 🇳🇱 🇳🇱
🇨🇿  CZECHIA
  Born  🇨🇿 🇨🇿 🇨🇿 🇨🇿 🇨🇿 🇨🇿 🇨🇿 🇨🇿 🇨🇿 🇨🇿 🇨🇿
🇨🇩  DR CONGO
  Born  🇫🇷 🏴󠁧󠁢󠁥󠁮󠁧󠁿 🇨🇩 🇨🇩 🇫🇷 🇫🇷 🇧🇪 🇫🇷 🇨🇩 🇫🇷 🇫🇷
🇪🇨  ECUADOR
  Born  🇦🇷 🇪🇨 🇪🇨 🇪🇨 🇪🇨 🇩🇪 🇪🇨 🇪🇨 🇪🇨 🇪🇨 🇪🇨
🇪🇬  EGYPT
  Born  🇪🇬 🇪🇬 🇪🇬 🇪🇬 🇪🇬 🇪🇬 🇪🇬 🇪🇬 🇪🇬 🇪🇬 🇪🇬
🏴󠁧󠁢󠁥󠁮󠁧󠁿  ENGLAND
  Born  🏴󠁧󠁢󠁥󠁮󠁧󠁿 🏴󠁧󠁢󠁥󠁮󠁧󠁿 🏴󠁧󠁢󠁥󠁮󠁧󠁿 🏴󠁧󠁢󠁥󠁮󠁧󠁿 🏴󠁧󠁢󠁥󠁮󠁧󠁿 🏴󠁧󠁢󠁥󠁮󠁧󠁿 🏴󠁧󠁢󠁥󠁮󠁧󠁿 🏴󠁧󠁢󠁥󠁮󠁧󠁿 🏴󠁧󠁢󠁥󠁮󠁧󠁿 🏴󠁧󠁢󠁥󠁮󠁧󠁿 🏴󠁧󠁢󠁥󠁮󠁧󠁿
🇬🇭  GHANA
  Born  🇬🇭 🇬🇭 🏴󠁧󠁢󠁥󠁮󠁧󠁿 🇫🇷 🇬🇭 🇬🇭 🇬🇭 🇬🇭 🇬🇭 🇫🇷 🏴󠁧󠁢󠁥󠁮󠁧󠁿
🇭🇹  HAITI
  Born  🇫🇷 🇭🇹 🇭🇹 🇭🇹 🇫🇷 🇭🇹 🇫🇷 🇭🇹 🇫🇷 🇫🇷 🇭🇹
🇮🇷  IRAN
  Born  🇮🇷 🇮🇷 🇮🇷 🇮🇷 🇮🇷 🇮🇷 🇮🇷 🇸🇪 🇮🇷 🇮🇷 🇮🇷
🇮🇶  IRAQ
  Born  🇮🇶 🇮🇶 🇮🇶 🇩🇪 🇩🇰 🇮🇶 🇸🇪 🇸🇪 🏴󠁧󠁢󠁥󠁮󠁧󠁿 🇮🇶 🇮🇶
🇨🇮  CÔTE D'IVOIRE
  Born  🇫🇷 🇨🇮 🇨🇮 🇨🇮 🇨🇮 🇨🇮 🇨🇮 🇨🇮 🇫🇷 🇨🇮 🇨🇮
🇯🇵  JAPAN
  Born  🇺🇸 🇯🇵 🇯🇵 🇯🇵 🇯🇵 🇯🇵 🇯🇵 🇯🇵 🇯🇵 🇯🇵 🇯🇵
🇯🇴  JORDAN
  Born  🇯🇴 🇯🇴 🇯🇴 🇯🇴 🇯🇴 🇯🇴 🇯🇴 🇯🇴 🇯🇴 🇯🇴 🇯🇴
🇲🇽  MEXICO
  Born  🇲🇽 🇲🇽 🇲🇽 🇲🇽 🇲🇽 🇲🇽 🇲🇽 🇺🇸 🇲🇽 🇲🇽 🇨🇴
🇳🇱  NETHERLANDS
  Born  🇳🇱 🇳🇱 🇳🇱 🇳🇱 🇳🇱 🇳🇱 🇳🇱 🇳🇱 🇳🇱 🇳🇱 🇳🇱
🇳🇿  NEW ZEALAND
  Born  🇳🇿 🇳🇿 🏴󠁧󠁢󠁷󠁬󠁳󠁿 🇳🇿 🇳🇿 🏴󠁧󠁢󠁥󠁮󠁧󠁿 🇳🇿 🇳🇿 🇳🇿 🇳🇿 🇳🇿
🇳🇴  NORWAY
  Born  🇳🇴 🇳🇴 🇳🇴 🇳🇴 🇳🇴 🇳🇴 🇳🇴 🇳🇴 🇳🇴 🏴󠁧󠁢󠁥󠁮󠁧󠁿 🇳🇴
🇵🇦  PANAMA
  Born  🇵🇦 🇵🇦 🇵🇦 🇵🇦 🇵🇦 🇵🇦 🇵🇦 🇵🇦 🇵🇦 🇵🇦 🇵🇦
🇵🇾  PARAGUAY
  Born  🇵🇾 🇵🇾 🇵🇾 🇵🇾 🇦🇷 🇦🇷 🇵🇾 🇵🇾 🇵🇾 🇵🇾 🇵🇾
🇵🇹  PORTUGAL
  Born  🇨🇭 🇵🇹 🇵🇹 🇵🇹 🇵🇹 🇵🇹 🇵🇹 🇵🇹 🇵🇹 🇵🇹 🇵🇹
🇶🇦  QATAR
  Born  🇶🇦 🇶🇦 🇵🇹 🇩🇿 🇶🇦 🇶🇦 🇸🇩 🇸🇳 🇧🇪 🇸🇴 🇶🇦
🇸🇦  SAUDI ARABIA
  Born  🇸🇦 🇸🇦 🇸🇦 🇸🇦 🇸🇦 🇸🇦 🇸🇦 🇸🇦 🇸🇦 🇸🇦 🇸🇦
🏴󠁧󠁢󠁳󠁣󠁴󠁿  SCOTLAND
  Born  🏴󠁧󠁢󠁳󠁣󠁴󠁿 🏴󠁧󠁢󠁳󠁣󠁴󠁿 🏴󠁧󠁢󠁳󠁣󠁴󠁿 🏴󠁧󠁢󠁳󠁣󠁴󠁿 🏴󠁧󠁢󠁳󠁣󠁴󠁿 🏴󠁧󠁢󠁳󠁣󠁴󠁿 🏴󠁧󠁢󠁳󠁣󠁴󠁿 🏴󠁧󠁢󠁥󠁮󠁧󠁿 🏴󠁧󠁢󠁳󠁣󠁴󠁿 🏴󠁧󠁢󠁳󠁣󠁴󠁿 🇦🇺
🇿🇦  SOUTH AFRICA
  Born  🇿🇦 🇿🇦 🇿🇦 🇿🇦 🇿🇦 🇿🇦 🇿🇦 🇿🇦 🇿🇦 🇿🇦 🇿🇦
🇰🇷  SOUTH KOREA
  Born  🇰🇷 🇰🇷 🇰🇷 🇰🇷 🇰🇷 🇰🇷 🇰🇷 🇰🇷 🇰🇷 🇰🇷 🇰🇷
🇪🇸  SPAIN
  Born  🇪🇸 🇪🇸 🇫🇷 🇫🇷 🇪🇸 🇪🇸 🇪🇸 🇪🇸 🇪🇸 🇪🇸 🇪🇸
🇸🇪  SWEDEN
  Born  🇸🇪 🇸🇪 🇸🇪 🇸🇪 🇸🇪 🇸🇪 🇸🇪 🇸🇪 🇸🇪 🇸🇪 🇸🇪
🇹🇳  TUNISIA
  Born  🇹🇳 🇫🇷 🇫🇷 🇩🇪 🇫🇷 🇫🇷 🇫🇷 🇩🇪 🇫🇷 🇳🇴 🇹🇳
🇹🇷  TÜRKIYE
  Born  🇹🇷 🇹🇷 🇹🇷 🇹🇷 🇳🇱 🇩🇪 🇳🇱 🇹🇷 🇹🇷 🇩🇪 🇹🇷
🇺🇾  URUGUAY
  Born  🇦🇷 🇺🇾 🇺🇾 🇺🇾 🇺🇾 🇺🇾 🇺🇾 🇺🇾 🇺🇾 🇺🇾 🇺🇾
🇺🇸  UNITED STATES
  Born  🇺🇸 🇳🇱 🇺🇸 🇺🇸 🏴󠁧󠁢󠁥󠁮󠁧󠁿 🇺🇸 🇺🇸 🇺🇸 🇩🇪 🇺🇸 🇺🇸
🇺🇿  UZBEKISTAN
  Born  🇰🇿 🇺🇿 🇺🇿 🇺🇿 🇺🇿 🇺🇿 🇺🇿 🇺🇿 🇺🇿 🇺🇿 🇺🇿
```

</details>

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
