"""Versioned Romanian text normalizer for discovery lookup.

Mirrors contracts/intent_ranking.yaml -> normalization and docs/03A §8:
  * Unicode NFKC
  * casefold (lowercase)
  * diacritics-insensitive lookup key (strip combining marks; ă/â/î/ș/ț -> a/a/i/s/t)
  * punctuation -> space, whitespace collapsed
  * stable whitespace tokenization
  * numeric tokens preserved

The normalizer only produces a *lookup key*; it never alters the copy shown to
the user. Abbreviation expansion is intentionally editorial/configurable (see
``abbreviations``) and empty by default: we do not invent administrative
expansions in code. The abbreviations listed in docs/03A §8 are recognized as
approved short tokens so they are not discarded by the min-length guard.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field

NORMALIZATION_VERSION = "2.1.0"

# docs/03A §8 recognized abbreviations (kept as valid short tokens). Their
# canonical expansions are editorial config, not invented here.
APPROVED_SHORT_TOKENS = frozenset({"ci", "cei", "civ", "rca", "itp", "drpciv", "dgpci", "spclep", "pfa", "srl"})

_NON_KEY_CHARS = re.compile(r"[^0-9a-z\s]")
_WS = re.compile(r"\s+")


def _strip_diacritics(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch))


@dataclass(frozen=True)
class RomanianNormalizer:
    """Deterministic, versioned normalizer.

    ``min_query_chars`` and ``approved_short_tokens`` come from
    contracts/intent_ranking.yaml. ``abbreviations`` maps a recognized
    abbreviation token to its expansion token(s); empty by default.
    """

    version: str = NORMALIZATION_VERSION
    min_query_chars: int = 2
    approved_short_tokens: frozenset[str] = APPROVED_SHORT_TOKENS
    abbreviations: dict[str, str] = field(default_factory=dict)

    def key(self, text: str | None) -> str:
        """Return the diacritics-insensitive lookup key for a string."""
        if not text:
            return ""
        s = unicodedata.normalize("NFKC", str(text))
        s = s.casefold()
        s = _strip_diacritics(s)
        s = _NON_KEY_CHARS.sub(" ", s)
        s = _WS.sub(" ", s).strip()
        return s

    def tokens(self, text: str | None) -> list[str]:
        """Stable whitespace tokenization with controlled abbreviation expansion."""
        key = self.key(text)
        if not key:
            return []
        out: list[str] = []
        for tok in key.split(" "):
            expansion = self.abbreviations.get(tok)
            if expansion:
                out.extend(self.key(expansion).split(" "))
            else:
                out.append(tok)
        return out

    def token_set(self, text: str | None) -> frozenset[str]:
        return frozenset(self.tokens(text))

    def is_too_short(self, text: str | None) -> bool:
        """True if the normalized query is below the minimum and not an approved token."""
        key = self.key(text)
        if not key:
            return True
        if key in self.approved_short_tokens:
            return False
        return len(key.replace(" ", "")) < self.min_query_chars
