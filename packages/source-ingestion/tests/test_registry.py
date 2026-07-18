"""Tests for the source registry."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from wb_ingestion.errors import RegistryError
from wb_ingestion.registry import (
    SourceRegistry,
    SourceStatus,
    TrustLevel,
    make_source_id,
)


@pytest.fixture()
def registry() -> SourceRegistry:
    reg = SourceRegistry()
    reg.add_allowed_domain("primariatm.ro")
    reg.add_allowed_domain("gov.ro")
    return reg


class TestMakeSourceId:
    def test_deterministic(self) -> None:
        assert make_source_id("https://example.com") == make_source_id("https://example.com")

    def test_different_urls(self) -> None:
        assert make_source_id("https://a.com") != make_source_id("https://b.com")


class TestSourceRegistration:
    def test_register_source(self, registry: SourceRegistry) -> None:
        source = registry.register(
            url="https://www.primariatm.ro/acte",
            publisher="Primăria Timișoara",
            trust=TrustLevel.OFFICIAL,
        )
        assert source.url == "https://www.primariatm.ro/acte"
        assert source.status == SourceStatus.ACTIVE
        assert source.trust == TrustLevel.OFFICIAL
        assert registry.count() == 1

    def test_duplicate_url_raises(self, registry: SourceRegistry) -> None:
        registry.register(
            url="https://www.primariatm.ro/acte",
            publisher="Primăria Timișoara",
            trust=TrustLevel.OFFICIAL,
        )
        with pytest.raises(RegistryError, match="already registered"):
            registry.register(
                url="https://www.primariatm.ro/acte",
                publisher="Other",
                trust=TrustLevel.SECONDARY,
            )

    def test_get_by_url(self, registry: SourceRegistry) -> None:
        source = registry.register(
            url="https://www.primariatm.ro/acte",
            publisher="Primăria Timișoara",
            trust=TrustLevel.OFFICIAL,
        )
        found = registry.get_by_url("https://www.primariatm.ro/acte")
        assert found.source_id == source.source_id

    def test_get_not_found(self, registry: SourceRegistry) -> None:
        with pytest.raises(RegistryError, match="not found"):
            registry.get("nonexistent")


class TestDomainAllowlist:
    def test_allowed_domain(self, registry: SourceRegistry) -> None:
        assert registry.is_domain_allowed("https://www.primariatm.ro/page")
        assert registry.is_domain_allowed("https://sub.primariatm.ro/page")

    def test_blocked_domain(self, registry: SourceRegistry) -> None:
        assert not registry.is_domain_allowed("https://evil.com/phish")

    def test_exact_domain_match(self, registry: SourceRegistry) -> None:
        assert registry.is_domain_allowed("https://primariatm.ro/")
        assert not registry.is_domain_allowed("https://fakeprimariatm.ro/")


class TestFetchScheduling:
    def test_never_fetched_is_due(self, registry: SourceRegistry) -> None:
        registry.register(
            url="https://www.primariatm.ro/acte",
            publisher="Test",
            trust=TrustLevel.OFFICIAL,
        )
        due = registry.list_due_for_fetch()
        assert len(due) == 1

    def test_recently_fetched_not_due(self, registry: SourceRegistry) -> None:
        source = registry.register(
            url="https://www.primariatm.ro/acte",
            publisher="Test",
            trust=TrustLevel.OFFICIAL,
            fetch_interval_hours=24,
        )
        registry.record_fetch(source.source_id, "snap123")
        due = registry.list_due_for_fetch()
        assert len(due) == 0

    def test_old_fetch_is_due(self, registry: SourceRegistry) -> None:
        source = registry.register(
            url="https://www.primariatm.ro/acte",
            publisher="Test",
            trust=TrustLevel.OFFICIAL,
            fetch_interval_hours=1,
        )
        registry.record_fetch(source.source_id, "snap123")
        # Simulate time passing
        future = datetime.now(UTC) + timedelta(hours=2)
        due = registry.list_due_for_fetch(now=future)
        assert len(due) == 1
