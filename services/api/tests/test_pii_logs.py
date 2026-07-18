"""PII-free logs test: verify that no PII appears in structured log output.

Tests the logging pipeline end-to-end:
1. JsonFormatter strips denylisted keys from log context.
2. scrub_payload redacts PII in audit payloads.
3. Access logs contain method, path, status — never request/response bodies.
"""

from __future__ import annotations

import json
import logging

from wb_api.audit import _is_pii_key, scrub_payload
from wb_api.logging import JsonFormatter, log_event, new_request_id, set_request_id


class TestJsonFormatterPII:
    """JsonFormatter must not emit denylisted keys."""

    def _format(self, msg: str, **context) -> dict:
        formatter = JsonFormatter()
        logger = logging.getLogger("test.pii")
        record = logger.makeRecord(
            name="test.pii", level=logging.INFO, fn="", lno=0,
            msg=msg, args=(), exc_info=None,
            extra={"context": context},
        )
        output = formatter.format(record)
        return json.loads(output)

    def test_no_facts_in_log(self) -> None:
        entry = self._format("request.access", method="POST", path="/v1/journeys", facts={"age": 25})
        assert "facts" not in entry

    def test_no_value_in_log(self) -> None:
        entry = self._format("request.access", method="POST", path="/v1/journeys", value="secret")
        assert "value" not in entry

    def test_no_message_in_log(self) -> None:
        entry = self._format("feedback.submit", device_id="abc", message="user complaint text")
        assert "message" not in entry

    def test_no_payload_in_log(self) -> None:
        entry = self._format("audit", action="create", payload={"secret": "data"})
        assert "payload" not in entry

    def test_no_note_in_log(self) -> None:
        entry = self._format("requirement.update", note="personal note")
        assert "note" not in entry

    def test_no_email_in_log(self) -> None:
        entry = self._format("contact", email="user@example.com")
        assert "email" not in entry

    def test_no_token_in_log(self) -> None:
        entry = self._format("auth", token="bearer_token_123")
        assert "token" not in entry

    def test_no_authorization_in_log(self) -> None:
        entry = self._format("auth", authorization="Bearer xyz")
        assert "authorization" not in entry

    def test_allowed_keys_present(self) -> None:
        entry = self._format(
            "request.access", method="GET", path="/v1/journeys",
            status=200, request_id="abc123",
        )
        assert entry["method"] == "GET"
        assert entry["path"] == "/v1/journeys"
        assert entry["status"] == 200

    def test_request_id_in_log(self) -> None:
        rid = new_request_id()
        set_request_id(rid)
        entry = self._format("test", key="value")
        assert entry["request_id"] == rid


class TestScrubPayload:
    """Audit payload scrubbing redacts PII."""

    def test_email_redacted(self) -> None:
        result = scrub_payload({"user_email": "test@example.com", "action": "create"})
        assert result["user_email"] == "[redacted]"
        assert result["action"] == "create"

    def test_phone_redacted(self) -> None:
        result = scrub_payload({"contact_phone": "+40712345678"})
        assert result["contact_phone"] == "[redacted]"

    def test_cnp_redacted(self) -> None:
        result = scrub_payload({"cnp": "1234567890123"})
        assert result["cnp"] == "[redacted]"

    def test_name_redacted(self) -> None:
        result = scrub_payload({"first_name": "Ion", "last_name": "Popescu"})
        assert result["first_name"] == "[redacted]"
        assert result["last_name"] == "[redacted]"

    def test_address_redacted(self) -> None:
        result = scrub_payload({"address": "Str. Republicii 1"})
        assert result["address"] == "[redacted]"

    def test_iban_redacted(self) -> None:
        result = scrub_payload({"iban": "RO49AAAA1B31007593840000"})
        assert result["iban"] == "[redacted]"

    def test_value_redacted(self) -> None:
        result = scrub_payload({"value": 42})
        assert result["value"] == "[redacted]"

    def test_note_redacted(self) -> None:
        result = scrub_payload({"note": "personal observation"})
        assert result["note"] == "[redacted]"

    def test_message_redacted(self) -> None:
        result = scrub_payload({"message": "user feedback"})
        assert result["message"] == "[redacted]"

    def test_passport_redacted(self) -> None:
        result = scrub_payload({"passport": "AB123456"})
        assert result["passport"] == "[redacted]"

    def test_nested_pii_redacted(self) -> None:
        result = scrub_payload({
            "user": {
                "name": "Ion",
                "email": "ion@example.com",
            },
            "action": "create",
        })
        assert result["user"]["name"] == "[redacted]"
        assert result["user"]["email"] == "[redacted]"
        assert result["action"] == "create"

    def test_list_pii_redacted(self) -> None:
        result = scrub_payload({
            "contacts": [
                {"name": "Ion", "phone": "123"},
                {"name": "Maria", "phone": "456"},
            ]
        })
        assert result["contacts"][0]["name"] == "[redacted]"
        assert result["contacts"][1]["phone"] == "[redacted]"

    def test_non_pii_preserved(self) -> None:
        result = scrub_payload({
            "action": "journey.create",
            "intent_id": "identity_card_first",
            "route_hash": "abc123",
            "status": "active",
        })
        assert result["action"] == "journey.create"
        assert result["intent_id"] == "identity_card_first"
        assert result["route_hash"] == "abc123"
        assert result["status"] == "active"


class TestPIIKeyDetection:
    """Key matching is case-insensitive and handles common patterns."""

    def test_exact_match(self) -> None:
        assert _is_pii_key("email")
        assert _is_pii_key("phone")
        assert _is_pii_key("cnp")
        assert _is_pii_key("name")
        assert _is_pii_key("address")
        assert _is_pii_key("value")
        assert _is_pii_key("note")
        assert _is_pii_key("message")

    def test_case_insensitive(self) -> None:
        assert _is_pii_key("Email")
        assert _is_pii_key("PHONE")
        assert _is_pii_key("Cnp")

    def test_suffix_match(self) -> None:
        assert _is_pii_key("user_email")
        assert _is_pii_key("contact_phone")
        assert _is_pii_key("home_address")
        assert _is_pii_key("first_name")

    def test_non_pii(self) -> None:
        assert not _is_pii_key("action")
        assert not _is_pii_key("intent_id")
        assert not _is_pii_key("route_hash")
        assert not _is_pii_key("status")
        assert not _is_pii_key("device_id")
