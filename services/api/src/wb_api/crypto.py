"""Envelope field encryption for sensitive citizen data.

AES-256-GCM with a 96-bit random nonce. Tokens are self-describing and carry
the key id so keys can be rotated without re-reading every row eagerly:

    wbenc:1:<key_id>:<urlsafe_b64(nonce || ciphertext_with_tag)>

Additional authenticated data (AAD) binds a ciphertext to its context (for
example the column name + row id) so a value cannot be silently copied between
fields. AAD is authenticated, not encrypted.
"""
from __future__ import annotations

import base64
import os
from typing import Mapping

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

PREFIX = "wbenc"
VERSION = "1"
NONCE_BYTES = 12
KEY_BYTES = 32


class CryptoError(Exception):
    pass


class UnknownKey(CryptoError):
    pass


class DecryptionError(CryptoError):
    pass


def _as_bytes(value) -> bytes:
    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        return value.encode("utf-8")
    raise TypeError("expected str or bytes")


class FieldCipher:
    """Encrypt/decrypt individual field values with a keyring."""

    def __init__(self, keys: Mapping[str, bytes], active_key_id: str):
        if active_key_id not in keys:
            raise UnknownKey(f"active key '{active_key_id}' is not in the keyring")
        for kid, key in keys.items():
            if len(key) != KEY_BYTES:
                raise ValueError(f"key '{kid}' must be {KEY_BYTES} bytes for AES-256")
        self._keys = dict(keys)
        self._active = active_key_id

    @classmethod
    def from_env(cls) -> "FieldCipher":
        """Build from WB_ENC_KEYS='kid1:base64,kid2:base64' and WB_ENC_ACTIVE_KEY."""
        raw = os.environ.get("WB_ENC_KEYS", "")
        keys: dict[str, bytes] = {}
        for item in (p for p in raw.split(",") if p.strip()):
            kid, b64 = item.split(":", 1)
            keys[kid.strip()] = base64.b64decode(b64.strip())
        active = os.environ.get("WB_ENC_ACTIVE_KEY", next(iter(keys), ""))
        return cls(keys, active)

    def encrypt(self, plaintext, *, aad=b"") -> str:
        nonce = os.urandom(NONCE_BYTES)
        ct = AESGCM(self._keys[self._active]).encrypt(nonce, _as_bytes(plaintext), _as_bytes(aad))
        blob = base64.urlsafe_b64encode(nonce + ct).decode("ascii")
        return f"{PREFIX}:{VERSION}:{self._active}:{blob}"

    def decrypt(self, token: str, *, aad=b"") -> bytes:
        parts = token.split(":", 3)
        if len(parts) != 4:
            raise DecryptionError("malformed ciphertext token")
        prefix, version, key_id, blob = parts
        if prefix != PREFIX or version != VERSION:
            raise DecryptionError("unsupported ciphertext token")
        if key_id not in self._keys:
            raise UnknownKey(f"unknown key id '{key_id}'")
        raw = base64.urlsafe_b64decode(blob.encode("ascii"))
        nonce, ct = raw[:NONCE_BYTES], raw[NONCE_BYTES:]
        try:
            return AESGCM(self._keys[key_id]).decrypt(nonce, ct, _as_bytes(aad))
        except Exception as exc:  # cryptography raises InvalidTag
            raise DecryptionError("authentication failed (wrong key, AAD, or tampered)") from exc

    def decrypt_str(self, token: str, *, aad=b"") -> str:
        return self.decrypt(token, aad=aad).decode("utf-8")
