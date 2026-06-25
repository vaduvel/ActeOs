from datetime import datetime, timezone

import pytest

from wb_rule_engine import resolve

hypothesis = pytest.importorskip("hypothesis")
from hypothesis import given, strategies as st  # noqa: E402

from tests.conftest import _bundle  # noqa: E402

NOW = datetime(2026, 6, 1, tzinfo=timezone.utc)


@given(
    year=st.integers(min_value=2018, max_value=2024),
    month=st.integers(min_value=1, max_value=12),
    day=st.integers(min_value=1, max_value=28),
)
def test_route_hash_stable_across_runs(year, month, day):
    req = {
        "intent_id": "test.enroll",
        "jurisdiction_id": "ro.timis.timisoara",
        "reference_date": "2026-09-01",
        "facts": {"birth_date": f"{year:04d}-{month:02d}-{day:02d}"},
    }
    a = resolve(req, _bundle(), now=NOW)
    b = resolve(req, _bundle(), now=NOW)
    assert a["route_hash"] == b["route_hash"]
