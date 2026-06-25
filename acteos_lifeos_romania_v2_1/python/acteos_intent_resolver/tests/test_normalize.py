from acteos_intent_resolver.normalize import NORMALIZATION_VERSION, RomanianNormalizer

nz = RomanianNormalizer()


def test_diacritics_insensitive_key():
    assert nz.key("schimb\u0103 domiciliul") == nz.key("schimba domiciliul")
    assert nz.key("expirat\u0103") == "expirata"
    assert nz.key("\u00een buletin") == "in buletin"
    assert nz.key("ap\u0103") == "apa"


def test_casefold_and_punctuation():
    assert nz.key("  BULETIN,  Expirat! ") == "buletin expirat"
    assert nz.key("mi-am pierdut buletinul") == "mi am pierdut buletinul"


def test_nfkc_compatibility():
    # full-width / compatibility chars fold to ascii letters
    assert nz.key("\uff22uletin") == "buletin"


def test_numeric_tokens_preserved():
    assert nz.tokens("clasa 0 pregatitoare") == ["clasa", "0", "pregatitoare"]


def test_min_length_and_approved_short_tokens():
    assert nz.is_too_short("c") is True
    assert nz.is_too_short("") is True
    assert nz.is_too_short("ci") is False  # approved short token
    assert nz.is_too_short("buletin") is False


def test_tokens_stable():
    assert nz.tokens("Buletin  expirat") == ["buletin", "expirat"]
    assert nz.token_set("buletin expirat") == frozenset({"buletin", "expirat"})


def test_abbreviation_expansion_is_opt_in():
    expanding = RomanianNormalizer(abbreviations={"ci": "carte de identitate"})
    assert expanding.tokens("ci expirata") == ["carte", "de", "identitate", "expirata"]
    # default normalizer does NOT invent expansions
    assert nz.tokens("ci expirata") == ["ci", "expirata"]


def test_version_constant():
    assert nz.version == NORMALIZATION_VERSION == "2.1.0"
