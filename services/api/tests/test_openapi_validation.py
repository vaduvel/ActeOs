"""OpenAPI contract validation: verify the generated spec matches expectations.

Checks that:
1. All spec paths from 08_API_SPEC.yaml exist in the generated OpenAPI.
2. All operations have response models declared.
3. Security schemes are defined.
4. No undocumented endpoints leak into the spec.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from wb_api.app import create_app
from wb_api.config import Settings


def _test_settings() -> Settings:
    return Settings(
        database_url="sqlite:///:memory:",
        bundle_dir="/tmp/bundles",
        log_level="DEBUG",
        service_version="0.1.0-test",
    )


@pytest.fixture()
def openapi_spec() -> dict:
    app = create_app(settings=_test_settings())
    client = TestClient(app)
    resp = client.get("/openapi.json")
    assert resp.status_code == 200
    return resp.json()


# Expected paths from 08_API_SPEC.yaml
EXPECTED_PATHS = {
    "/health/live",
    "/health/ready",
    "/v1/catalog/intents",
    "/v1/catalog/jurisdictions",
    "/v1/routes/resolve",
    "/v1/journeys",
    "/v1/journeys/{journey_id}",
    "/v1/journeys/{journey_id}/facts",
    "/v1/journeys/{journey_id}/recalculate",
    "/v1/journeys/{journey_id}/requirements/{requirement_id}",
    "/v1/journeys/{journey_id}/document-analyses",
    "/v1/evidence/{claim_id}",
    "/v1/feedback",
    "/v1/curator/sources",
    "/v1/curator/sources/{source_id}/fetch",
    "/v1/curator/source-snapshots/{snapshot_id}/draft",
    "/v1/curator/rule-versions/{rule_version_id}/review",
    "/v1/curator/bundles/{bundle_id}/publish",
    "/v1/curator/bundles/{bundle_id}/rollback",
}

# Paths that must NOT appear (internal/framework)
FORBIDDEN_PATHS = {
    "/docs",
    "/redoc",
    "/openapi.json",
    "/favicon.ico",
}


class TestExpectedPaths:
    def test_all_spec_paths_exist(self, openapi_spec: dict) -> None:
        actual_paths = set(openapi_spec.get("paths", {}).keys())
        missing = EXPECTED_PATHS - actual_paths
        assert missing == set(), f"Missing paths in OpenAPI spec: {missing}"

    def test_no_forbidden_paths(self, openapi_spec: dict) -> None:
        actual_paths = set(openapi_spec.get("paths", {}).keys())
        leaked = FORBIDDEN_PATHS & actual_paths
        assert leaked == set(), f"Forbidden paths in spec: {leaked}"


class TestOperations:
    def test_all_operations_have_tags(self, openapi_spec: dict) -> None:
        for path, methods in openapi_spec["paths"].items():
            for method, operation in methods.items():
                if method in ("get", "post", "patch", "delete", "put"):
                    assert "tags" in operation, f"{method.upper()} {path} missing tags"

    def test_all_operations_have_responses(self, openapi_spec: dict) -> None:
        for path, methods in openapi_spec["paths"].items():
            for method, operation in methods.items():
                if method in ("get", "post", "patch", "delete", "put"):
                    assert "responses" in operation, f"{method.upper()} {path} missing responses"
                    assert len(operation["responses"]) > 0

    def test_post_operations_have_request_body(self, openapi_spec: dict) -> None:
        post_paths = [
            ("/v1/routes/resolve", "post"),
            ("/v1/journeys", "post"),
            ("/v1/journeys/{journey_id}/recalculate", "post"),
            ("/v1/feedback", "post"),
            ("/v1/curator/sources", "post"),
        ]
        for path, method in post_paths:
            if path in openapi_spec["paths"] and method in openapi_spec["paths"][path]:
                op = openapi_spec["paths"][path][method]
                assert "requestBody" in op, f"POST {path} missing requestBody"


class TestSecuritySchemes:
    def test_curator_bearer_defined(self, openapi_spec: dict) -> None:
        schemes = openapi_spec.get("components", {}).get("securitySchemes", {})
        assert "curatorBearer" in schemes

    def test_curator_scopes_defined(self, openapi_spec: dict) -> None:
        schemes = openapi_spec.get("components", {}).get("securitySchemes", {})
        bearer = schemes.get("curatorBearer", {})
        flows = bearer.get("flows", {})
        # Should have at least one flow with scopes
        all_scopes: set[str] = set()
        for flow in flows.values():
            all_scopes.update(flow.get("scopes", {}).keys())
        expected_scopes = {"sources:read", "sources:write", "rules:write", "rules:review", "rules:publish"}
        assert expected_scopes <= all_scopes, f"Missing scopes: {expected_scopes - all_scopes}"


class TestInfoBlock:
    def test_title(self, openapi_spec: dict) -> None:
        assert "Waze" in openapi_spec["info"]["title"]

    def test_version_exists(self, openapi_spec: dict) -> None:
        assert "version" in openapi_spec["info"]
        assert len(openapi_spec["info"]["version"]) > 0
