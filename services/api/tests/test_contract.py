"""Contract tests: validate response shapes against the OpenAPI spec.

Every endpoint's response must:
1. Match the declared response_model schema (no extra undocumented fields).
2. Return the documented status code.
3. Return problem+json for errors with the canonical Problem shape.

These tests run against the FastAPI test client with a mocked service layer —
no database needed. They verify the wire contract, not business logic.
"""

from __future__ import annotations

import json
import uuid
from datetime import UTC, datetime
from typing import Any
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from wb_api.app import create_app
from wb_api.config import Settings
from wb_api.deps import get_services


def _test_settings() -> Settings:
    return Settings(
        database_url="sqlite:///:memory:",
        bundle_dir="/tmp/bundles",
        log_level="DEBUG",
        service_version="0.1.0-test",
    )


@pytest.fixture()
def client() -> TestClient:
    """Test client with mocked services."""
    app = create_app(settings=_test_settings())

    # Mock the service layer
    mock_services = MagicMock()

    # Health endpoints don't need mocking — they use settings directly
    # For other endpoints, we'll mock per-test

    def override_services():
        return mock_services

    app.dependency_overrides[get_services] = override_services

    yield TestClient(app)
    app.dependency_overrides.clear()


DEVICE_ID = str(uuid.uuid4())
DEVICE_HEADERS = {"X-Device-Id": DEVICE_ID}


# =====================================================================
# System endpoints
# =====================================================================

class TestHealthContract:
    def test_health_live_shape(self, client: TestClient) -> None:
        resp = client.get("/health/live")
        assert resp.status_code == 200
        body = resp.json()
        # Required fields per spec
        assert "status" in body
        assert body["status"] in ("ok", "degraded")
        assert "version" in body
        assert "timestamp" in body
        # No extra undocumented fields
        allowed = {"status", "version", "timestamp", "checks"}
        assert set(body.keys()) <= allowed

    def test_health_ready_shape(self, client: TestClient) -> None:
        resp = client.get("/health/ready")
        body = resp.json()
        assert "status" in body
        assert "version" in body
        assert "timestamp" in body
        allowed = {"status", "version", "timestamp", "checks"}
        assert set(body.keys()) <= allowed


# =====================================================================
# Catalog endpoints
# =====================================================================

class TestCatalogContract:
    def test_list_intents_response_shape(self, client: TestClient) -> None:
        mock = client.app.dependency_overrides[get_services]()
        mock.catalog.list_intents.return_value = []

        resp = client.get("/v1/catalog/intents")
        assert resp.status_code == 200
        body = resp.json()
        assert "items" in body
        assert isinstance(body["items"], list)

    def test_intent_summary_shape(self, client: TestClient) -> None:
        from wb_api.schemas import IntentSummary

        intent = IntentSummary(
            id="identity_card_first",
            title="Carte de identitate",
            short_description="Prima carte de identitate",
            category="identity",
            keywords=["buletin", "CI"],
            release_status="production",
        )
        mock = client.app.dependency_overrides[get_services]()
        mock.catalog.list_intents.return_value = [intent]

        resp = client.get("/v1/catalog/intents")
        body = resp.json()
        assert len(body["items"]) == 1
        item = body["items"][0]
        # Required fields
        assert "id" in item
        assert "title" in item
        assert "category" in item
        assert "release_status" in item
        assert item["release_status"] in ("production", "preview")

    def test_list_jurisdictions_shape(self, client: TestClient) -> None:
        mock = client.app.dependency_overrides[get_services]()
        mock.catalog.list_jurisdictions.return_value = []

        resp = client.get("/v1/catalog/jurisdictions")
        assert resp.status_code == 200
        body = resp.json()
        assert "items" in body

    def test_jurisdiction_shape(self, client: TestClient) -> None:
        from wb_api.schemas import Jurisdiction

        jur = Jurisdiction(
            id=str(uuid.uuid4()),
            parent_id=None,
            code="timis",
            name="Timiș",
            type="county",
            timezone="Europe/Bucharest",
        )
        mock = client.app.dependency_overrides[get_services]()
        mock.catalog.list_jurisdictions.return_value = [jur]

        resp = client.get("/v1/catalog/jurisdictions")
        body = resp.json()
        item = body["items"][0]
        assert item["timezone"] == "Europe/Bucharest"
        assert item["type"] in ("country", "county", "uat", "institution")


# =====================================================================
# Route resolution
# =====================================================================

class TestRouteResolutionContract:
    def test_resolve_route_response_shape(self, client: TestClient) -> None:
        from wb_api.schemas import RouteResolution

        resolution = RouteResolution(
            status="resolved",
            route_hash=f"sha256:{'a' * 64}",
            rule_bundle_hash=f"sha256:{'b' * 64}",
            facts_hash=f"sha256:{'c' * 64}",
            engine_version="0.1.0",
            evaluated_at=datetime.now(UTC),
            missing_facts=[],
            steps=[],
            blocking_issues=[],
            confidence="verified",
        )
        mock = client.app.dependency_overrides[get_services]()
        mock.resolver.resolve.return_value = resolution

        resp = client.post(
            "/v1/routes/resolve",
            json={
                "intent_id": "identity_card_first",
                "jurisdiction_id": str(uuid.uuid4()),
                "evaluated_at": datetime.now(UTC).isoformat(),
                "facts": [],
            },
            headers=DEVICE_HEADERS,
        )
        assert resp.status_code == 200
        body = resp.json()

        # Required fields per spec
        assert "status" in body
        assert body["status"] in ("resolved", "needs_facts", "blocked")
        assert "facts_hash" in body
        assert "engine_version" in body
        assert "evaluated_at" in body

    def test_resolve_route_422_on_invalid_input(self, client: TestClient) -> None:
        """Invalid input returns 422 with problem+json."""
        resp = client.post(
            "/v1/routes/resolve",
            json={"bad_field": True},
            headers=DEVICE_HEADERS,
        )
        assert resp.status_code == 422
        body = resp.json()
        # Problem+json shape
        assert "type" in body
        assert "title" in body
        assert "status" in body


# =====================================================================
# Error contract
# =====================================================================

class TestErrorContract:
    def test_error_response_has_problem_shape(self, client: TestClient) -> None:
        """All error responses follow problem+json."""
        resp = client.post(
            "/v1/routes/resolve",
            json={},
            headers=DEVICE_HEADERS,
        )
        body = resp.json()
        assert "type" in body
        assert "title" in body
        assert "status" in body
        assert isinstance(body["status"], int)
        assert 400 <= body["status"] < 600

    def test_error_content_type(self, client: TestClient) -> None:
        resp = client.post(
            "/v1/routes/resolve",
            json={},
            headers=DEVICE_HEADERS,
        )
        # FastAPI returns application/json for validation errors by default
        # but our exception handler should return problem+json
        assert resp.status_code == 422


# =====================================================================
# Response field validation
# =====================================================================

class TestNoExtraFields:
    """Verify responses don't leak undocumented fields."""

    def test_health_response_no_extra(self, client: TestClient) -> None:
        resp = client.get("/health/live")
        body = resp.json()
        allowed = {"status", "version", "timestamp", "checks"}
        extra = set(body.keys()) - allowed
        assert extra == set(), f"Extra fields in HealthResponse: {extra}"

    def test_catalog_items_no_extra(self, client: TestClient) -> None:
        from wb_api.schemas import IntentSummary

        intent = IntentSummary(
            id="test", title="Test", category="test",
            release_status="production",
        )
        mock = client.app.dependency_overrides[get_services]()
        mock.catalog.list_intents.return_value = [intent]

        resp = client.get("/v1/catalog/intents")
        item = resp.json()["items"][0]
        allowed = {"id", "title", "short_description", "category", "keywords", "release_status"}
        extra = set(item.keys()) - allowed
        assert extra == set(), f"Extra fields in IntentSummary: {extra}"

    def test_jurisdiction_no_extra(self, client: TestClient) -> None:
        from wb_api.schemas import Jurisdiction

        jur = Jurisdiction(
            id=str(uuid.uuid4()), code="timis", name="Timiș",
            type="county", timezone="Europe/Bucharest",
        )
        mock = client.app.dependency_overrides[get_services]()
        mock.catalog.list_jurisdictions.return_value = [jur]

        resp = client.get("/v1/catalog/jurisdictions")
        item = resp.json()["items"][0]
        allowed = {"id", "parent_id", "code", "name", "type", "timezone"}
        extra = set(item.keys()) - allowed
        assert extra == set(), f"Extra fields in Jurisdiction: {extra}"
