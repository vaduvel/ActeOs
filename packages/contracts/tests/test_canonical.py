from wb_contracts.canonical import canonical_json, sha256_hex


def test_key_order_independent():
    a = {"b": 1, "a": 2}
    b = {"a": 2, "b": 1}
    assert canonical_json(a) == canonical_json(b)
    assert sha256_hex(a) == sha256_hex(b)


def test_compact_separators():
    assert canonical_json({"a": 1, "b": [1, 2]}) == '{"a":1,"b":[1,2]}'


def test_unicode_is_literal():
    assert canonical_json({"x": "ă"}) == '{"x":"ă"}'


def test_hash_prefix():
    assert sha256_hex({"n": 1}).startswith("sha256:")
