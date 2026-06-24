"""Map a country name to its flag emoji (terminal) or ISO code (for image URLs).

A flag emoji is two Unicode "regional indicator" letters built from the
country's ISO 3166-1 alpha-2 code (e.g. CH -> 🇨🇭). So the job is really just
name -> alpha-2 code -> emoji.

Resolution order for a name:
  1. UNKNOWN sentinels      -> white flag 🏳️
  2. Built-in OVERRIDES     -> Kosovo, overseas territories, UK home nations, variants
  3. pycountry fuzzy lookup -> broad coverage, only if the package is installed
  4. give up                -> white flag 🏳️

A field may name more than one origin (e.g. "Mauritania / Senegal"); use
`country_to_flags` / `name_to_codes` to get all of them.
"""

from __future__ import annotations

# --- alpha-2 code -> flag emoji ------------------------------------------------

_REGIONAL_INDICATOR_A = 0x1F1E6  # Unicode codepoint for 🇦
_ASCII_A = ord("A")

WHITE_FLAG = "\U0001F3F3️"  # 🏳️ — used for unknown / unresolved origins

# Codes that aren't a plain 2-letter ISO country: map straight to an emoji.
# UK home nations use Unicode tag sequences; flagcdn uses the same "gb-eng" path.
_SPECIAL_EMOJI = {
    "GB-ENG": "\U0001F3F4\U000E0067\U000E0062\U000E0065\U000E006E\U000E0067\U000E007F",  # 🏴 England
    "GB-SCT": "\U0001F3F4\U000E0067\U000E0062\U000E0073\U000E0063\U000E0074\U000E007F",  # 🏴 Scotland
    "GB-WLS": "\U0001F3F4\U000E0067\U000E0062\U000E0077\U000E006C\U000E0073\U000E007F",  # 🏴 Wales
}


def code_to_flag(code: str) -> str:
    """Turn a country code (e.g. 'CH' or 'GB-ENG') into its flag emoji."""
    code = code.upper()
    if code in _SPECIAL_EMOJI:
        return _SPECIAL_EMOJI[code]
    if len(code) != 2 or not code.isalpha():
        return WHITE_FLAG
    return "".join(chr(_REGIONAL_INDICATOR_A + ord(c) - _ASCII_A) for c in code)


# --- country name -> alpha-2 code ----------------------------------------------

# Sentinels meaning "no known origin".
_UNKNOWN = {"", "unknown", "uncertain", "n/a", "none", "?"}

# Separators for fields that list more than one origin.
_SEPARATORS = [" / ", "/", " and ", " & ", ", ", ","]

# Names pycountry can't resolve (Kosovo, UK home nations) or spells differently,
# plus every country/territory used across our data files. Keys are lowercased.
OVERRIDES = {
    # not a real ISO country / special:
    "kosovo": "XK",
    "england": "GB-ENG",
    "scotland": "GB-SCT",
    "wales": "GB-WLS",
    "northern ireland": "GB-NIR",
    # countries in the data:
    "switzerland": "CH", "france": "FR", "germany": "DE", "spain": "ES",
    "netherlands": "NL", "belgium": "BE", "canada": "CA", "croatia": "HR",
    "serbia": "RS", "morocco": "MA", "algeria": "DZ", "nigeria": "NG",
    "cameroon": "CM", "senegal": "SN", "mali": "ML", "mauritania": "MR",
    "guinea": "GN", "guinea-bissau": "GW", "lebanon": "LB", "benin": "BJ",
    "haiti": "HT", "chile": "CL",
    "gambia": "GM", "the gambia": "GM",
    "ivory coast": "CI", "côte d'ivoire": "CI", "cote d'ivoire": "CI",
    "bosnia and herzegovina": "BA", "bosnia": "BA",
    # French overseas territories (own flags on flagcdn):
    "french guiana": "GF", "guadeloupe": "GP", "martinique": "MQ", "réunion": "RE",
    # other common variants for when more teams are added later:
    "turkey": "TR", "türkiye": "TR", "north macedonia": "MK",
    "dr congo": "CD", "democratic republic of the congo": "CD",
    "republic of the congo": "CG", "cape verde": "CV", "cabo verde": "CV",
    "south korea": "KR", "north korea": "KP",
    "united states": "US", "usa": "US", "united kingdom": "GB",
    "palestine": "PS", "state of palestine": "PS",
    "russia": "RU", "russian federation": "RU",
}

try:  # optional dependency — extends coverage but not required
    import pycountry  # type: ignore
except ImportError:  # pragma: no cover
    pycountry = None


def _normalize(name: str) -> str:
    """Lowercase and drop any parenthetical detail, e.g. 'Croatia (Zadar)' -> 'croatia'."""
    name = name.split("(")[0]
    return name.strip().lower()


def name_to_code(name: str) -> str | None:
    """Resolve a single country name to an ISO alpha-2 code (or GB-ENG etc.), else None."""
    key = _normalize(name)
    if key in _UNKNOWN:
        return None
    if key in OVERRIDES:
        return OVERRIDES[key]
    if pycountry is not None:
        try:
            return pycountry.countries.lookup(key).alpha_2
        except LookupError:
            return None
    return None


def split_origins(field: str) -> list[str]:
    """Split a possibly-compound origin field into individual country names."""
    parts = [field]
    for sep in _SEPARATORS:
        parts = [piece for chunk in parts for piece in chunk.split(sep)]
    return [p.strip() for p in parts if p.strip()]


def name_to_codes(field: str) -> list[str]:
    """Resolve a (possibly compound) origin field to a list of codes; [] if none."""
    return [c for c in (name_to_code(p) for p in split_origins(field)) if c]


def country_to_flag(name: str) -> str:
    """Single country name -> flag emoji, white flag if unknown/unresolved."""
    code = name_to_code(name)
    return code_to_flag(code) if code else WHITE_FLAG


def country_to_flags(field: str) -> str:
    """Compound origin field -> one or more flag emoji joined, white flag if none."""
    codes = name_to_codes(field)
    return "".join(code_to_flag(c) for c in codes) if codes else WHITE_FLAG


if __name__ == "__main__":
    checks = ["Switzerland", "Kosovo", "England", "French Guiana", "Guinea-Bissau",
              "Bosnia and Herzegovina", "Mauritania / Senegal", "unknown", ""]
    for c in checks:
        print(f"{c or '(empty)':<26} -> {country_to_flags(c)}")
