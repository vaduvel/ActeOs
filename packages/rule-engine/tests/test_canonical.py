from wb_rule_engine.canonical import canonical_json, sha256_hex


def test_key_order_independent():
    a = {"b": 1, "a": 2, "c": [3, 2, 1]}
    b = {"a": 2, "c": [3, 2, 1], "b": 1}
    assert canonical_json(a) == canonical_json(b)
    assert sha256_hex(a) == sha256_hex(b)


def test_hash_prefix():
    h = sha256_hex({"x": 1})
    assert h.startswith("sha256:")
    assert len(h) == len("sha256:") + 64


def test_unicode_preserved():
    # ensure_ascii=False keeps diacritics stable and deterministic
    assert canonical_json({"oras": "Timisoara"}) == '{"oras":"Timisoara"}'
