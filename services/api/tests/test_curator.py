"""Curator endpoint tests: auth, scopes, response shapes."""

from __future__ import annotations

import uuid
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
    app = create_app(settings=_test_settings())
    mock = MagicMock()
    def override():
        return mock
    app.dependency_overrides[get_services] = override
    yield TestClient(app)
    app.dependency_overrides.clear()


# Auth tokens for testing
CURATOR_READ = "Bearer curator1:sources:read"
CURATOR_WRITE = "Bearer curator1:sources:write,rules:write"
CURATOR_REVIEW = "Bearer curator2:rules:review"
CURATOR_PUBLISH = "Bearer curator3:rules:publish"
CURATOR_ALL = "Bearer curator1:sources:read,sources:write,rules:write,rules:review,rules:publish"


class TestCuratorAuth:
    """Authentication and scope enforcement."""

    def test_no_auth_header_rejected(self, client: TestClient) -> None:
        resp = client.get("/v1/curator/sources")
        assert resp.status_code == 422
        body = resp.json()
        assert body["code"] == "unauthorized"

    def test_invalid_auth_format_rejected(self, client: TestClient) -> None:
        resp = client.get(
            "/v1/curator/sources",
            headers={"Authorization": "Basic abc123"},
        )
        assert resp.status_code == 422

    def test_insufficient_scope_rejected(self, client: TestClient) -> None:
        resp = client.get(
            "/v1/curator/sources",
            headers={"Authorization": "Bearer curator1:rules:review"},
        )
        assert resp.status_code == 422
        body = resp.json()
        assert body["code"] == "insufficient_scope"


class TestSourceEndpoints:
    """Source registry CRUD."""

    def test_list_sources(self, client: TestClient) -> None:
        resp = client.get(
            "/v1/curator/sources",
            headers={"Authorization": CURATOR_READ},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert "items" in body

    def test_create_source(self, client: TestClient) -> None:
        resp = client.post(
            "/v1/curator/sources",
            json={
                "canonical_url": "https://www.primariatm.ro/acte",
                "publisher": "Primăria Timișoara",
                "authority_level": "uat",
                "freshness_class": "operational",
                "review_interval_days": 30,
            },
            headers={"Authorization": CURATOR_WRITE},
        )
        assert resp.status_code == 201
        body = resp.json()
        assert "id" in body
        assert body["canonical_url"] == "https://www.primariatm.ro/acte"
        assert body["publisher"] == "Primăria Timișoara"
        assert body["status"] == "active"
        assert body["freshness_class"] == "operational"

    def test_create_source_write_scope_required(self, client: TestClient) -> None:
        resp = client.post(
            "/v1/curator/sources",
            json={
                "canonical_url": "https://example.com",
                "publisher": "Test",
                "authority_level": "institution",
                "freshness_class": "explanatory",
                "review_interval_days": 90,
            },
            headers={"Authorization": CURATOR_READ},  # read-only scope
        )
        assert resp.status_code == 422
        assert resp.json()["code"] == "insufficient_scope"

    def test_fetch_source(self, client: TestClient) -> None:
        source_id = str(uuid.uuid4())
        resp = client.post(
            f"/v1/curator/sources/{source_id}/fetch",
            headers={"Authorization": CURATOR_WRITE},
        )
        assert resp.status_code == 202
        body = resp.json()
        assert "job_id" in body
        assert body["status"] in ("queued", "running")


class TestDraftCreation:
    def test_create_draft(self, client: TestClient) -> None:
        snapshot_id = str(uuid.uuid4())
        resp = client.post(
            f"/v1/curator/source-snapshots/{snapshot_id}/draft",
            json={
                "intent_id": "identity_card_first",
                "jurisdiction_id": str(uuid.uuid4()),
                "use_ai_extraction": False,
            },
            headers={"Authorization": CURATOR_WRITE},
        )
        assert resp.status_code == 202
        body = resp.json()
        assert "draft_id" in body
        assert body["status"] in ("draft", "extracting")

    def test_create_draft_requires_write_scope(self, client: TestClient) -> None:
        resp = client.post(
            f"/v1/curator/source-snapshots/{uuid.uuid4()}/draft",
            json={"intent_id": "test", "jurisdiction_id": str(uuid.uuid4())},
            headers={"Authorization": CURATOR_READ},
        )
        assert resp.status_code == 422


class TestRuleReview:
    def test_submit_review(self, client: TestClient) -> None:
        rule_id = str(uuid.uuid4())
        resp = client.post(
            f"/v1/curator/rule-versions/{rule_id}/review",
            json={
                "decision": "approve",
                "rationale": "Content verified against official source.",
            },
            headers={"Authorization": CURATOR_REVIEW},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["rule_version_id"] == rule_id
        assert "status" in body
        assert "reviews_required" in body
        assert "reviews_received" in body

    def test_review_decision_enum(self, client: TestClient) -> None:
        resp = client.post(
            f"/v1/curator/rule-versions/{uuid.uuid4()}/review",
            json={"decision": "invalid_decision", "rationale": "Test rationale here"},
            headers={"Authorization": CURATOR_REVIEW},
        )
        assert resp.status_code == 422

    def test_review_rationale_min_length(self, client: TestClient) -> None:
        resp = client.post(
            f"/v1/curator/rule-versions/{uuid.uuid4()}/review",
            json={"decision": "approve", "rationale": "short"},
            headers={"Authorization": CURATOR_REVIEW},
        )
        assert resp.status_code == 422


class TestPublishRollback:
    def test_publish_bundle(self, client: TestClient) -> None:
        bundle_id = str(uuid.uuid4())
        resp = client.post(
            f"/v1/curator/bundles/{bundle_id}/publish",
            json={"channel": "production", "reason": "Content update verified"},
            headers={"Authorization": CURATOR_PUBLISH},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["bundle_id"] == bundle_id
        assert body["channel"] == "production"
        assert "publication_id" in body
        assert "bundle_hash" in body
        assert "published_at" in body

    def test_publish_requires_publish_scope(self, client: TestClient) -> None:
        resp = client.post(
            f"/v1/curator/bundles/{uuid.uuid4()}/publish",
            json={"channel": "canary"},
            headers={"Authorization": CURATOR_READ},
        )
        assert resp.status_code == 422

    def test_rollback_bundle(self, client: TestClient) -> None:
        bundle_id = str(uuid.uuid4())
        resp = client.post(
            f"/v1/curator/bundles/{bundle_id}/rollback",
            json={
                "target_publication_id": str(uuid.uuid4()),
                "reason": "Rollback due to incorrect fee amount in claim",
            },
            headers={"Authorization": CURATOR_PUBLISH},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["bundle_id"] == bundle_id

    def test_rollback_reason_min_length(self, client: TestClient) -> None:
        resp = client.post(
            f"/v1/curator/bundles/{uuid.uuid4()}/rollback",
            json={
                "target_publication_id": str(uuid.uuid4()),
                "reason": "too short",
            },
            headers={"Authorization": CURATOR_PUBLISH},
        )
        assert resp.status_code == 422


class TestCuratorResponseShapes:
    """Verify no extra undocumented fields in responses."""

    def test_bundle_publication_shape(self, client: TestClient) -> None:
        resp = client.post(
            f"/v1/curator/bundles/{uuid.uuid4()}/publish",
            json={"channel": "canary", "reason": "Testing canary publish"},
            headers={"Authorization": CURATOR_PUBLISH},
        )
        body = resp.json()
        allowed = {"publication_id", "bundle_id", "bundle_hash", "channel", "published_at"}
        extra = set(body.keys()) - allowed
        assert extra == set(), f"Extra fields: {extra}"

    def test_rule_version_status_shape(self, client: TestClient) -> None:
        resp = client.post(
            f"/v1/curator/rule-versions/{uuid.uuid4()}/review",
            json={"decision": "approve", "rationale": "Verified against source."},
            headers={"Authorization": CURATOR_REVIEW},
        )
        body = resp.json()
        allowed = {"rule_version_id", "status", "reviews_required", "reviews_received"}
        extra = set(body.keys()) - allowed
        assert extra == set(), f"Extra fields: {extra}"
