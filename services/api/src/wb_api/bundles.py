"""Verified rule-bundle provider.

The rule engine is given a bundle of the exact shape ``{bundle_version, rules}``
and computes ``rule_bundle_hash = sha256(bundle)``; therefore the dict handed to
the engine must contain *only* those canonical fields, or the hash would drift.
``assemble_engine_bundle`` is the single place that constructs that dict, used
both when publishing (to compute the stored ``bundle_sha256``) and when
resolving, guaranteeing publish/resolve hash parity.

Resolution order:
1. The currently published production bundle in the database (source of truth).
2. A verified, immutable bundle JSON on disk under ``WB_BUNDLE_DIR`` named
   ``<intent_id>.json`` — used for offline/dev/test and first-boot seeding.
"""
from __future__ import annotations

import json
import threading
from dataclasses import dataclass
from pathlib import Path

from .canonical import sha256_hex
from .repositories import ContentBundleRepo


def assemble_engine_bundle(bundle_version: str, rules: list[dict]) -> dict:
    """Canonical engine bundle. ONLY these keys may be present."""
    return {"bundle_version": bundle_version, "rules": rules}


@dataclass(frozen=True)
class ResolvedBundle:
    engine_bundle: dict
    bundle_hash: str
    bundle_id: str | None
    channel: str
    origin: str  # "db" | "file"


class BundleProvider:
    def __init__(self, *, content_repo: ContentBundleRepo | None = None, bundle_dir: str | None = None):
        self._content = content_repo
        self._dir = Path(bundle_dir) if bundle_dir else None
        self._file_cache: dict[str, tuple[float, ResolvedBundle]] = {}
        self._lock = threading.Lock()

    # --- database (authoritative) ------------------------------------------
    def _from_db(self, intent_id: str, jurisdiction_id: str, channel: str) -> ResolvedBundle | None:
        if self._content is None:
            return None
        pub = self._content.current_publication(intent_id, jurisdiction_id, channel=channel)
        if pub is None:
            return None
        bundle = self._content.get_bundle(pub.bundle_id)
        if bundle is None:
            return None
        rules = self._content.bundle_rules(pub.bundle_id)
        version = (bundle.manifest or {}).get("bundle_version") or bundle.bundle_sha256
        engine_bundle = assemble_engine_bundle(version, rules)
        return ResolvedBundle(
            engine_bundle=engine_bundle,
            bundle_hash=sha256_hex(engine_bundle),
            bundle_id=bundle.id,
            channel=channel,
            origin="db",
        )

    # --- filesystem (verified, immutable) ----------------------------------
    def _from_file(self, intent_id: str) -> ResolvedBundle | None:
        if self._dir is None:
            return None
        path = self._dir / f"{intent_id}.json"
        if not path.is_file():
            return None
        mtime = path.stat().st_mtime
        with self._lock:
            cached = self._file_cache.get(intent_id)
            if cached and cached[0] == mtime:
                return cached[1]
        data = json.loads(path.read_text(encoding="utf-8"))
        engine_bundle = assemble_engine_bundle(data["bundle_version"], data["rules"])
        resolved = ResolvedBundle(
            engine_bundle=engine_bundle,
            bundle_hash=sha256_hex(engine_bundle),
            bundle_id=None,
            channel="file",
            origin="file",
        )
        with self._lock:
            self._file_cache[intent_id] = (mtime, resolved)
        return resolved

    def for_intent(self, intent_id: str, jurisdiction_id: str, *, channel: str = "production") -> ResolvedBundle | None:
        return self._from_db(intent_id, jurisdiction_id, channel) or self._from_file(intent_id)
