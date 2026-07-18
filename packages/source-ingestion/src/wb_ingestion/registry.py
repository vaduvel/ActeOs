"""Safe source registry.

Manages the canonical list of sources (URLs, publishers, trust levels)
with an allowlist of permitted domains for fetching.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from urllib.parse import urlparse

from wb_ingestion.errors import IngestionProblemCode, RegistryError


class TrustLevel(str, Enum):
    """How much we trust a source publisher."""

    OFFICIAL = "official"          # government, official institution
    LEGAL_DATABASE = "legal_database"  # legislatie.just.ro etc.
    SECONDARY = "secondary"        # news, blogs, forums


class SourceStatus(str, Enum):
    """Lifecycle status of a registered source."""

    ACTIVE = "active"
    DEPRECATED = "deprecated"
    SUSPENDED = "suspended"        # temporarily unreachable / broken


@dataclass(frozen=True)
class Source:
    """A registered content source."""

    source_id: str
    url: str
    publisher: str
    trust: TrustLevel
    status: SourceStatus = SourceStatus.ACTIVE
    language: str = "ro"
    registered_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    last_fetched_at: datetime | None = None
    last_snapshot_id: str | None = None
    fetch_interval_hours: int = 168  # default: weekly
    notes: str = ""

    @property
    def domain(self) -> str:
        return urlparse(self.url).hostname or ""


def make_source_id(url: str) -> str:
    """Deterministic source ID from URL."""
    return hashlib.sha256(url.encode("utf-8")).hexdigest()[:16]


class SourceRegistry:
    """In-memory source registry with domain allowlist.

    Thread-safe for single-process use. Persistence is handled
    by the caller (serialize to/from YAML or DB).
    """

    def __init__(self, allowed_domains: set[str] | None = None) -> None:
        self._sources: dict[str, Source] = {}
        self._allowed_domains: set[str] = allowed_domains or set()
        self._url_index: dict[str, str] = {}  # url → source_id

    @property
    def allowed_domains(self) -> frozenset[str]:
        return frozenset(self._allowed_domains)

    def add_allowed_domain(self, domain: str) -> None:
        self._allowed_domains.add(domain.lower().strip())

    def remove_allowed_domain(self, domain: str) -> None:
        self._allowed_domains.discard(domain.lower().strip())

    def is_domain_allowed(self, url: str) -> bool:
        """Check if the URL's domain is in the allowlist."""
        hostname = (urlparse(url).hostname or "").lower()
        # Check exact match and parent domain match
        for allowed in self._allowed_domains:
            if hostname == allowed or hostname.endswith(f".{allowed}"):
                return True
        return False

    def register(
        self,
        url: str,
        publisher: str,
        trust: TrustLevel,
        *,
        source_id: str | None = None,
        language: str = "ro",
        fetch_interval_hours: int = 168,
        notes: str = "",
    ) -> Source:
        """Register a new source. Raises if URL already registered."""
        if url in self._url_index:
            raise RegistryError(
                IngestionProblemCode.SOURCE_ALREADY_EXISTS,
                f"URL already registered: {url}",
            )
        sid = source_id or make_source_id(url)
        source = Source(
            source_id=sid,
            url=url,
            publisher=publisher,
            trust=trust,
            language=language,
            fetch_interval_hours=fetch_interval_hours,
            notes=notes,
        )
        self._sources[sid] = source
        self._url_index[url] = sid
        return source

    def get(self, source_id: str) -> Source:
        """Get source by ID. Raises if not found."""
        try:
            return self._sources[source_id]
        except KeyError:
            raise RegistryError(
                IngestionProblemCode.SOURCE_NOT_FOUND,
                f"Source not found: {source_id}",
            ) from None

    def get_by_url(self, url: str) -> Source:
        """Get source by URL. Raises if not found."""
        sid = self._url_index.get(url)
        if sid is None:
            raise RegistryError(
                IngestionProblemCode.SOURCE_NOT_FOUND,
                f"Source not found for URL: {url}",
            )
        return self._sources[sid]

    def update_status(self, source_id: str, status: SourceStatus) -> Source:
        """Update source status. Returns updated source."""
        source = self.get(source_id)
        updated = Source(
            source_id=source.source_id,
            url=source.url,
            publisher=source.publisher,
            trust=source.trust,
            status=status,
            language=source.language,
            registered_at=source.registered_at,
            last_fetched_at=source.last_fetched_at,
            last_snapshot_id=source.last_snapshot_id,
            fetch_interval_hours=source.fetch_interval_hours,
            notes=source.notes,
        )
        self._sources[source_id] = updated
        return updated

    def record_fetch(self, source_id: str, snapshot_id: str) -> Source:
        """Record a successful fetch. Returns updated source."""
        source = self.get(source_id)
        updated = Source(
            source_id=source.source_id,
            url=source.url,
            publisher=source.publisher,
            trust=source.trust,
            status=source.status,
            language=source.language,
            registered_at=source.registered_at,
            last_fetched_at=datetime.now(UTC),
            last_snapshot_id=snapshot_id,
            fetch_interval_hours=source.fetch_interval_hours,
            notes=source.notes,
        )
        self._sources[source_id] = updated
        return updated

    def list_all(self) -> list[Source]:
        """List all registered sources."""
        return list(self._sources.values())

    def list_active(self) -> list[Source]:
        """List sources with status=ACTIVE."""
        return [s for s in self._sources.values() if s.status == SourceStatus.ACTIVE]

    def list_due_for_fetch(self, now: datetime | None = None) -> list[Source]:
        """List active sources that are due for re-fetching."""
        now = now or datetime.now(UTC)
        due: list[Source] = []
        for source in self.list_active():
            if source.last_fetched_at is None:
                due.append(source)
                continue
            elapsed = (now - source.last_fetched_at).total_seconds() / 3600
            if elapsed >= source.fetch_interval_hours:
                due.append(source)
        return due

    def count(self) -> int:
        return len(self._sources)
