"""Map a country name to its flag emoji.

A flag emoji is two Unicode "regional indicator" letters built from the
country's ISO 3166-1 alpha-2 code (e.g. CH -> 🇨🇭). So the job is really just
name -> alpha-2 code -> emoji.

Resolution order for a name:
  1. UNKNOWN sentinels      -> white flag 🏳️
  2. Built-in OVERRIDES     -> handles Kosovo (not in ISO) and common name variants
  3. pycountry fuzzy lookup -> broad coverage, only if the package is installed
  4. give up                -> white flag 🏳️

This keeps the module dependency-free for the names we actually use, while
letting `pip install pycountry` extend coverage to every other country for free.
"""

from __future__ import annotations

# --- alpha-2 code -> flag emoji ------------------------------------------------

_REGIONAL_INDICATOR_A = 0x1F1E6  # Unicode codepoint for 🇦
_ASCII_A = ord("A")

WHITE_FLAG = "\U0001F3F3️"  # 🏳️ — used for unknown / unresolved origins


def code_to_flag(alpha2: str) -> str:
    """Turn a 2-letter country code (e.g. 'CH') into its flag emoji."""
    alpha2 = alpha2.upper()
    if len(alpha2) != 2 or not alpha2.isalpha():
        return WHITE_FLAG
    return "".join(chr(_REGIONAL_INDICATOR_A + ord(c) - _ASCII_A) for c in alpha2)


# --- country name -> alpha-2 code ----------------------------------------------

# Sentinels meaning "no known origin".
_UNKNOWN = {"", "unknown", "n/a", "none", "?"}

# Names pycountry can't resolve (Kosovo) or spells differently, plus the
# specific spellings used in our data files. Keys are lowercased.
OVERRIDES = {
    "kosovo": "XK",            # user-assigned ISO code; 🇽🇰 renders on most platforms
    "switzerland": "CH",
    "nigeria": "NG",
    "spain": "ES",
    "chile": "CL",
    "germany": "DE",
    "cameroon": "CM",
    "senegal": "SN",
    # common variants you may hit when adding more teams later:
    "turkey": "TR",
    "türkiye": "TR",
    "north macedonia": "MK",
    "dr congo": "CD",
    "democratic republic of the congo": "CD",
    "republic of the congo": "CG",
    "ivory coast": "CI",
    "côte d'ivoire": "CI",
    "cote d'ivoire": "CI",
    "cape verde": "CV",
    "cabo verde": "CV",
    "south korea": "KR",
    "north korea": "KP",
    "united states": "US",
    "usa": "US",
}

try:  # optional dependency — extends coverage but not required
    import pycountry  # type: ignore
except ImportError:  # pragma: no cover
    pycountry = None


def name_to_code(name: str) -> str | None:
    """Resolve a country name to an ISO alpha-2 code, or None if unknown."""
    key = name.strip().lower()
    if key in _UNKNOWN:
        return None
    if key in OVERRIDES:
        return OVERRIDES[key]
    if pycountry is not None:
        try:
            return pycountry.countries.lookup(name).alpha_2
        except LookupError:
            return None
    return None


def country_to_flag(name: str) -> str:
    """Country name -> flag emoji, with a white flag for unknown/unresolved."""
    code = name_to_code(name)
    return code_to_flag(code) if code else WHITE_FLAG


if __name__ == "__main__":
    # Quick self-check of the tricky cases.
    checks = ["Switzerland", "Kosovo", "Cape Verde", "Cameroon", "unknown", ""]
    for c in checks:
        print(f"{c or '(empty)':<14} -> {country_to_flag(c)}")
