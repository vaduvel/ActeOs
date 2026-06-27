"""Contract tests for the live case API responses.

These tests validate real FastAPI responses against the committed OpenAPI 3.1
contract in ``contracts/openapi.yaml``. They intentionally run without a live DB:
the case service is overridden with the same deterministic in-memory harness used
by the API slice tests.

Why this exists: ``validate_pack.py`` proves the authored data pack is coherent,
and ordinary API tests prove behavior. This file closes the contract gap by
asserting that externally visible JSON for POST/GET /v1/cases and validation
errors still satisfies the public OpenAPI components.
"""
from __future__ import annotations

import uuid
from datetime import date, datetime
from pathlib import Path
from typing import Any

import pytest
import yaml
from fastapi.testclient import TestClient

from acteos_api.cases import CaseService, get_case_service
from acteos_api.main import REQUEST_ID_HEADER, app
from acteos_api.repository import InMemoryCaseRepository
from acteos_api.rulesets import RulesetRepository

PACK_ROOT = Path(__file__).resolve().parents[3]
OPENAPI_PATH = PACK_ROOT / "contracts" / "openapi.yaml"

MINOR_PASSPORT = {
    "event_type_id": "life.minor_passport",
    "status": "draft",
    "rules": [
        {
            "id": "rule.mp.docs",
            "canonical_rule_id": "minor_passport.docs",
            "event_type_id": "life.minor_passport",
            "jurisdiction_ids": ["ro"],
            "severity": "critical",
            "when": {"op": "const", "value": True},
            "effects": [
                {"type": "include_step", "step_id": "apply_minor_passport"},
                {"type": "include_requirement", "requirement_id": "req.minor_birth_certificate"},
            ],
            "source_claim_ids": ["claim.mp.docs"],
            "status": "draft",
        },
        {
            "id": "rule.mp.single_parent_gate",
            "canonical_rule_id": "minor_passport.single_parent_gate",
            "event_type_id": "life.minor_passport",
            "jurisdiction_ids": ["ro"],
            "severity": "critical",
            "when": {
                "op": "all",
                "args": [
                    {"op": "eq", "field": "both_parents_consent", "value": False},
                    {"op": "eq", "field": "has_single_parent_doc", "value": False},
                ],
            },
            "effects": [
                {"type": "block", "message_ro": "Fara ambii parinti ai nevoie de procura."},
            ],
            "source_claim_ids": ["claim.mp.single"],
            "status": "draft",
        },
    ],
}

INTENT_LINKS = {"ro.intent.identity.obtain_minor_passport": ["ro.life.minor_passport"]}


@pytest.fixture(scope="session")
def openapi_contract() -> dict[str, Any]:
    return yaml.safe_load(OPENAPI_PATH.read_text(encoding="utf-8"))


@pytest.fixture()
def client():
    repo = RulesetRepository.from_mapping({"life.minor_passport": MINOR_PASSPORT})
    svc = CaseService(INTENT_LINKS, repo, InMemoryCaseRepository(), ruleset_version="test-1")
    app.dependency_overrides[get_case_service] = lambda: svc
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def _payload(**overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "intent_type_id": "ro.intent.identity.obtain_minor_passport",
        "reference_date": "2026-06-25",
        "timezone": "Europe/Bucharest",
        "jurisdiction_path": ["ro", "ro.tm.timisoara"],
        "installation_id": "2c6ee198-20d0-4e30-9443-f0d4fd46c87a",
        "facts": {"both_parents_consent": True, "has_single_parent_doc": False},
    }
    base.update(overrides)
    return base


def _response_schema(contract: dict[str, Any], path: str, method: str, status: str) -> dict[str, Any]:
    return contract["paths"][path][method]["responses"][status]["content"]["application/json"]["schema"]


def _resolve_ref(schema: dict[str, Any], contract: dict[str, Any]) -> dict[str, Any]:
    ref = schema.get("$ref")
    if not ref:
        return schema
    prefix = "#/components/schemas/"
    assert ref.startswith(prefix), f"Unsupported local ref: {ref}"
    return contract["components"]["schemas"][ref.removeprefix(prefix)]


def _type_names(schema: dict[str, Any]) -> set[str]:
    raw_type = schema.get("type")
    if raw_type is None:
        return set()
    if isinstance(raw_type, list):
        return set(raw_type)
    return {raw_type}


def _assert_json_matches_schema(value: Any, schema: dict[str, Any], contract: dict[str, Any], path: str = "$") -> None:
    schema = _resolve_ref(schema, contract)

    if "oneOf" in schema:
        errors: list[AssertionError] = []
        for option in schema["oneOf"]:
            try:
                _assert_json_matches_schema(value, option, contract, path)
                return
            except AssertionError as exc:  # pragma: no cover - diagnostic path
                errors.append(exc)
        raise AssertionError(f"{path}: value did not match any oneOf option: {errors}")

    if "const" in schema:
        assert value == schema["const"], f"{path}: expected const {schema['const']!r}, got {value!r}"
    if "enum" in schema:
        assert value in schema["enum"], f"{path}: expected one of {schema['enum']!r}, got {value!r}"

    type_names = _type_names(schema)
    if value is None:
        assert "null" in type_names, f"{path}: expected non-null value for schema {schema!r}"
        return

    non_null_types = type_names - {"null"}
    if non_null_types:
        assert any(_matches_json_type(value, type_name) for type_name in non_null_types), (
            f"{path}: expected type {sorted(non_null_types)!r}, got {type(value).__name__}"
        )

    if "object" in non_null_types or (not non_null_types and "properties" in schema):
        assert isinstance(value, dict), f"{path}: expected object"
        for required_key in schema.get("required", []):
            assert required_key in value, f"{path}: missing required key {required_key!r}"
        for key, child_schema in schema.get("properties", {}).items():
            if key in value:
                _assert_json_matches_schema(value[key], child_schema, contract, f"{path}.{key}")
        return

    if "array" in non_null_types:
        assert isinstance(value, list), f"{path}: expected array"
        if "minItems" in schema:
            assert len(value) >= schema["minItems"], f"{path}: expected at least {schema['minItems']} items"
        if "maxItems" in schema:
            assert len(value) <= schema["maxItems"], f"{path}: expected at most {schema['maxItems']} items"
        item_schema = schema.get("items")
        if item_schema:
            for idx, item in enumerate(value):
                _assert_json_matches_schema(item, item_schema, contract, f"{path}[{idx}]")
        return

    if "string" in non_null_types and "format" in schema:
        _assert_string_format(value, schema["format"], path)


def _matches_json_type(value: Any, type_name: str) -> bool:
    if type_name == "object":
        return isinstance(value, dict)
    if type_name == "array":
        return isinstance(value, list)
    if type_name == "string":
        return isinstance(value, str)
    if type_name == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if type_name == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if type_name == "boolean":
        return isinstance(value, bool)
    raise AssertionError(f"Unsupported JSON schema type: {type_name}")


def _assert_string_format(value: Any, fmt: str, path: str) -> None:
    assert isinstance(value, str), f"{path}: expected string for format {fmt}"
    if fmt == "uuid":
        uuid.UUID(value)
    elif fmt == "date":
        date.fromisoformat(value)
    elif fmt == "date-time":
        datetime.fromisoformat(value.replace("Z", "+00:00"))


def test_post_case_live_response_matches_committed_openapi_case_response(client, openapi_contract):
    response = client.post("/v1/cases", json=_payload(), headers={REQUEST_ID_HEADER: "contract-post"})

    assert response.status_code == 201
    body = response.json()
    schema = _response_schema(openapi_contract, "/v1/cases", "post", "201")
    _assert_json_matches_schema(body, schema, openapi_contract)

    # Privacy boundary: response intentionally does not echo identity handles.
    assert "user_id" not in body
    assert "installation_id" not in body


def test_get_case_live_response_matches_committed_openapi_case_response(client, openapi_contract):
    created = client.post("/v1/cases", json=_payload()).json()

    response = client.get(f"/v1/cases/{created['id']}", headers={REQUEST_ID_HEADER: "contract-get"})

    assert response.status_code == 200
    schema = _response_schema(openapi_contract, "/v1/cases/{case_id}", "get", "200")
    _assert_json_matches_schema(response.json(), schema, openapi_contract)


def test_validation_error_live_response_matches_committed_openapi_error_response(client, openapi_contract):
    response = client.post(
        "/v1/cases",
        json=_payload(jurisdiction_path=["ro"]),
        headers={REQUEST_ID_HEADER: "contract-validation"},
    )

    assert response.status_code == 422
    body = response.json()
    schema = _response_schema(openapi_contract, "/v1/cases", "post", "422")
    _assert_json_matches_schema(body, schema, openapi_contract)
    assert body["error"]["code"] == "VALIDATION_ERROR"
    assert body["error"]["request_id"] == "contract-validation"
