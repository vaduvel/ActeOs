import os

import pytest

pytest.importorskip("cryptography")

from wb_api.crypto import DecryptionError, FieldCipher, UnknownKey  # noqa: E402

KEYS = {"k1": os.urandom(32), "k2": os.urandom(32)}


def _cipher(active="k1"):
    return FieldCipher(KEYS, active)


def test_roundtrip():
    c = _cipher()
    token = c.encrypt("CNP 1234567890123", aad="journeys:facts:row-1")
    assert token.startswith("wbenc:1:k1:")
    assert c.decrypt_str(token, aad="journeys:facts:row-1") == "CNP 1234567890123"


def test_nonce_is_random():
    c = _cipher()
    assert c.encrypt("x") != c.encrypt("x")


def test_aad_mismatch_fails():
    c = _cipher()
    token = c.encrypt("secret", aad="ctx-a")
    with pytest.raises(DecryptionError):
        c.decrypt(token, aad="ctx-b")


def test_tampered_ciphertext_fails():
    c = _cipher()
    token = c.encrypt("secret", aad="ctx")
    tampered = token[:-2] + ("AA" if not token.endswith("AA") else "BB")
    with pytest.raises(DecryptionError):
        c.decrypt(tampered, aad="ctx")


def test_unknown_active_key_rejected():
    with pytest.raises(UnknownKey):
        FieldCipher(KEYS, "missing")


def test_wrong_key_length_rejected():
    with pytest.raises(ValueError):
        FieldCipher({"short": b"too-short"}, "short")


def test_decrypt_with_rotated_keyring():
    # encrypted under k1, keyring still holds k1 even when active is k2
    token = FieldCipher(KEYS, "k1").encrypt("v", aad="a")
    assert FieldCipher(KEYS, "k2").decrypt_str(token, aad="a") == "v"
