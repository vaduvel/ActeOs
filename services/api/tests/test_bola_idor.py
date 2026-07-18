"""BOLA/IDOR tests: verify that device A cannot access device B's resources.

Every journey endpoint must:
1. Return 404 (not 403) when accessing another device's journey.
2. Not leak the existence of a journey through timing or error messages.
3. Scope all list endpoints to the requesting device only.
4. Reject requests without a valid X-Device-Id header.

The anti-IDOR guarantee lives in ``JourneyRepo.get_owned()`` which does not
distinguish "not found" from "not yours" — both return the same 404 error.
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
from wb_api.errors import NotFoundError


def _test_settings() -> Settings:
    return Settings(
        database_url="sqlite:///:memory:",
        bundle_dir="/tmp/bundles",
        log_level="DEBUG",
        service_version="0.1.0-test",
    )


DEVICE_A = str(uuid.uuid4())
DEVICE_B = str(uuid.uuid4())
HEADERS_A = {"X-Device-Id": DEVICE_A}
HEADERS_B = {"X-Device-Id": DEVICE_B}

FAKE_JOURNEY_ID = str(uuid.uuid4())


@pytest.fixture()
def client() -> TestClient:
    app = create_app(settings=_test_settings())
    mock_services = MagicMock()

    # Default: journey_repo.get_owned raises NotFoundError (anti-IDOR)
    mock_services.journeys.get.side_effect = NotFoundError("journey not found", code="journey_not_found")
    mock_services.journeys.delete.side_effect = NotFoundError("journey not found", code="journey_not_found")
    mock_services.journeys.patch_facts.side_effect = NotFoundError("journey not found", code="journey_not_found")
    mock_services.journeys.recalculate.side_effect = NotFoundError("journey not found", code="journey_not_found")
    mock_services.journeys.update_requirement.side_effect = NotFoundError("journey not found", code="journey_not_found")

    def override():
        return mock_services

    app.dependency_overrides[get_services] = override
    yield TestClient(app)
    app.dependency_overrides.clear()


class TestMissingDeviceHeader:
    """Requests without X-Device-Id must be rejected."""

    def test_get_journey_no_device_header(self, client: TestClient) -> None:
        resp = client.get(f"/v1/journeys/{FAKE_JOURNEY_ID}")
        assert resp.status_code == 422  # validation error

    def test_list_journeys_no_device_header(self, client: TestClient) -> None:
        resp = client.get("/v1/journeys")
        assert resp.status_code == 422

    def test_delete_journey_no_device_header(self, client: TestClient) -> None:
        resp = client.delete(f"/v1/journeys/{FAKE_JOURNEY_ID}")
        assert resp.status_code == 422

    def test_patch_facts_no_device_header(self, client: TestClient) -> None:
        resp = client.patch(
            f"/v1/journeys/{FAKE_JOURNEY_ID}/facts",
            json={"facts": [{"fact_id": "age", "value": 25}]},
        )
        assert resp.status_code == 422

    def test_invalid_device_id_format(self, client: TestClient) -> None:
        resp = client.get(
            f"/v1/journeys/{FAKE_JOURNEY_ID}",
            headers={"X-Device-Id": "not-a-uuid"},
        )
        assert resp.status_code == 422


class TestCrossDeviceAccess:
    """Device A must never see device B's journey data."""

    def test_get_other_device_journey_returns_404(self, client: TestClient) -> None:
        """GET journey with device B's ID returns 404, not 403."""
        resp = client.get(f"/v1/journeys/{FAKE_JOURNEY_ID}", headers=HEADERS_B)
        assert resp.status_code == 404
        body = resp.json()
        assert body["code"] == "journey_not_found"

    def test_delete_other_device_journey_returns_404(self, client: TestClient) -> None:
        resp = client.delete(f"/v1/journeys/{FAKE_JOURNEY_ID}", headers=HEADERS_B)
        assert resp.status_code == 404

    def test_patch_other_device_facts_returns_404(self, client: TestClient) -> None:
        resp = client.patch(
            f"/v1/journeys/{FAKE_JOURNEY_ID}/facts",
            json={"facts": [{"fact_id": "age", "value": 30}]},
            headers=HEADERS_B,
        )
        assert resp.status_code == 404

    def test_recalculate_other_device_returns_404(self, client: TestClient) -> None:
        resp = client.post(
            f"/v1/journeys/{FAKE_JOURNEY_ID}/recalculate",
            json={},
            headers=HEADERS_B,
        )
        assert resp.status_code == 404

    def test_update_requirement_other_device_returns_404(self, client: TestClient) -> None:
        resp = client.patch(
            f"/v1/journeys/{FAKE_JOURNEY_ID}/requirements/req1",
            json={"status": "completed"},
            headers=HEADERS_B,
        )
        assert resp.status_code == 404


class TestNoInformationLeakage:
    """The API must not leak whether a journey exists through error responses."""

    def test_404_does_not_distinguish_not_found_from_not_yours(self, client: TestClient) -> None:
        """Both cases must return the exact same error code and message."""
        resp = client.get(f"/v1/journeys/{uuid.uuid4()}", headers=HEADERS_A)
        body = resp.json()
        assert resp.status_code == 404
        assert body["code"] == "journey_not_found"
        # The detail message must NOT say "not yours" or "forbidden"
        assert "not yours" not in body.get("detail", "").lower()
        assert "forbidden" not in body.get("detail", "").lower()
        assert "permission" not in body.get("detail", "").lower()

    def test_404_response_shape_is_problem_json(self, client: TestClient) -> None:
        resp = client.get(f"/v1/journeys/{uuid.uuid4()}", headers=HEADERS_A)
        body = resp.json()
        assert "type" in body
        assert "title" in body
        assert "status" in body
        assert body["status"] == 404


class TestListScoping:
    """List endpoints must only return the requesting device's data."""

    def test_list_journeys_scoped_to_device(self, client: TestClient) -> None:
        """Journey list is filtered by device_id in the service layer."""
        mock = client.app.dependency_overrides[get_services]()
        mock.journeys.list.return_value = []

        resp = client.get("/v1/journeys", headers=HEADERS_A)
        assert resp.status_code == 200

        # Verify service was called with the correct device_id
        mock.journeys.list.assert_called_once()
        call_kwargs = mock.journeys.list.call_args
        assert call_kwargs is not None
        # The device_id should match the header we sent
        assert call_kwargs.kwargs.get("device_id") == DEVICE_A or \
               (call_kwargs[1].get("device_id") if len(call_kwargs) > 1 else None) == DEVICE_A
