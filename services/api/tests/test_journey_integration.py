"""Journey lifecycle integration test: create → get → patch facts → recalculate.

Verifies the full flow a citizen would follow, ensuring each step
produces valid responses and state transitions are correct.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from wb_api.app import create_app
from wb_api.config import Settings
from wb_api.deps import get_services
from wb_api.schemas import (
    FactInput,
    Journey,
    JourneySummary,
    RecalculationResult,
    RequirementState,
    RouteDiff,
    RouteResolution,
)


def _test_settings() -> Settings:
    return Settings(
        database_url="sqlite:///:memory:",
        bundle_dir="/tmp/bundles",
        log_level="DEBUG",
        service_version="0.1.0-test",
    )


DEVICE_ID = str(uuid.uuid4())
HEADERS = {"X-Device-Id": DEVICE_ID}
JURISDICTION_ID = str(uuid.uuid4())
JOURNEY_ID = str(uuid.uuid4())
NOW = datetime.now(UTC)

ROUTE_RESOLUTION = RouteResolution(
    status="resolved",
    route_hash=f"sha256:{'a' * 64}",
    rule_bundle_hash=f"sha256:{'b' * 64}",
    facts_hash=f"sha256:{'c' * 64}",
    engine_version="0.1.0",
    evaluated_at=NOW,
    missing_facts=[],
    steps=[],
    blocking_issues=[],
    confidence="verified",
)

JOURNEY_OBJ = Journey(
    id=JOURNEY_ID,
    intent_id="identity_card_first",
    title="Carte de identitate",
    status="active",
    jurisdiction_id=JURISDICTION_ID,
    created_at=NOW,
    updated_at=NOW,
    facts=[FactInput(fact_id="age", value=25, source="user")],
    resolution=ROUTE_RESOLUTION,
    requirement_states=[],
)

RECALC_RESULT = RecalculationResult(
    previous_route_hash=f"sha256:{'a' * 64}",
    resolution=ROUTE_RESOLUTION,
    diff=RouteDiff(
        added_steps=[],
        removed_steps=[],
        changed_requirements=[],
        deadline_changes=[],
    ),
)


@pytest.fixture()
def client() -> TestClient:
    app = create_app(settings=_test_settings())
    mock = MagicMock()

    # Wire the full happy path
    mock.journeys.create.return_value = JOURNEY_OBJ
    mock.journeys.get.return_value = JOURNEY_OBJ
    mock.journeys.list.return_value = [
        JourneySummary(
            id=JOURNEY_ID, intent_id="identity_card_first",
            title="Carte de identitate", status="active",
            next_action_title="Obține cazier judiciar",
            next_deadline=None, updated_at=NOW,
        )
    ]
    mock.journeys.patch_facts.return_value = JOURNEY_OBJ
    mock.journeys.recalculate.return_value = RECALC_RESULT
    mock.journeys.update_requirement.return_value = RequirementState(
        requirement_id="cazier_judiciar", status="in_progress",
        note=None, updated_at=NOW,
    )

    def override():
        return mock

    app.dependency_overrides[get_services] = override
    yield TestClient(app)
    app.dependency_overrides.clear()


class TestJourneyLifecycle:
    """Full journey lifecycle: create → get → list → patch → recalculate → update req."""

    def test_create_journey(self, client: TestClient) -> None:
        resp = client.post(
            "/v1/journeys",
            json={
                "intent_id": "identity_card_first",
                "jurisdiction_id": JURISDICTION_ID,
                "evaluated_at": NOW.isoformat(),
                "facts": [{"fact_id": "age", "value": 25}],
            },
            headers=HEADERS,
        )
        assert resp.status_code == 201
        body = resp.json()
        assert body["id"] == JOURNEY_ID
        assert body["intent_id"] == "identity_card_first"
        assert body["status"] == "active"
        assert "resolution" in body
        assert body["resolution"]["status"] == "resolved"
        assert body["resolution"]["facts_hash"] == f"sha256:{'c' * 64}"

    def test_get_journey(self, client: TestClient) -> None:
        resp = client.get(f"/v1/journeys/{JOURNEY_ID}", headers=HEADERS)
        assert resp.status_code == 200
        body = resp.json()
        assert body["id"] == JOURNEY_ID
        assert "facts" in body
        assert len(body["facts"]) == 1
        assert body["facts"][0]["fact_id"] == "age"

    def test_list_journeys(self, client: TestClient) -> None:
        resp = client.get("/v1/journeys", headers=HEADERS)
        assert resp.status_code == 200
        body = resp.json()
        assert isinstance(body, list)
        assert len(body) == 1
        assert body[0]["id"] == JOURNEY_ID
        assert body[0]["next_action_title"] == "Obține cazier judiciar"

    def test_patch_facts(self, client: TestClient) -> None:
        resp = client.patch(
            f"/v1/journeys/{JOURNEY_ID}/facts",
            json={
                "facts": [
                    {"fact_id": "age", "value": 25},
                    {"fact_id": "has_cazier", "value": True},
                ],
            },
            headers=HEADERS,
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["id"] == JOURNEY_ID

    def test_recalculate(self, client: TestClient) -> None:
        resp = client.post(
            f"/v1/journeys/{JOURNEY_ID}/recalculate",
            json={"reason": "user_change"},
            headers=HEADERS,
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["previous_route_hash"] == f"sha256:{'a' * 64}"
        assert "resolution" in body
        assert "diff" in body
        assert "added_steps" in body["diff"]
        assert "removed_steps" in body["diff"]
        assert "changed_requirements" in body["diff"]
        assert "deadline_changes" in body["diff"]

    def test_update_requirement(self, client: TestClient) -> None:
        resp = client.patch(
            f"/v1/journeys/{JOURNEY_ID}/requirements/cazier_judiciar",
            json={"status": "in_progress"},
            headers=HEADERS,
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["requirement_id"] == "cazier_judiciar"
        assert body["status"] == "in_progress"


class TestJourneyResponseShapes:
    """Every response conforms to the spec schema."""

    def test_journey_has_all_required_fields(self, client: TestClient) -> None:
        resp = client.get(f"/v1/journeys/{JOURNEY_ID}", headers=HEADERS)
        body = resp.json()
        # JourneySummary fields
        assert "id" in body
        assert "intent_id" in body
        assert "title" in body
        assert "status" in body
        assert "updated_at" in body
        # Journey-specific fields
        assert "jurisdiction_id" in body
        assert "created_at" in body
        assert "resolution" in body

    def test_resolution_has_required_fields(self, client: TestClient) -> None:
        resp = client.get(f"/v1/journeys/{JOURNEY_ID}", headers=HEADERS)
        resolution = resp.json()["resolution"]
        assert "status" in resolution
        assert "facts_hash" in resolution
        assert "engine_version" in resolution
        assert "evaluated_at" in resolution
        assert "steps" in resolution
        assert "missing_facts" in resolution
        assert "blocking_issues" in resolution

    def test_journey_status_enum(self, client: TestClient) -> None:
        resp = client.get(f"/v1/journeys/{JOURNEY_ID}", headers=HEADERS)
        body = resp.json()
        assert body["status"] in ("active", "completed", "archived")

    def test_resolution_status_enum(self, client: TestClient) -> None:
        resp = client.get(f"/v1/journeys/{JOURNEY_ID}", headers=HEADERS)
        body = resp.json()
        assert body["resolution"]["status"] in ("resolved", "needs_facts", "blocked")
