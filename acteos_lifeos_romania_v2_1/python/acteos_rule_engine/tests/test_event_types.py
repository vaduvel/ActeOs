"""Tests for the life-event catalog -> content.life_event_types compiler."""

from __future__ import annotations

from acteos_rule_engine.authoring.event_types import (
    EventTypeRecord,
    canonical_event_type_id,
    compile_event_types,
)

CATALOG = {
    "schema_version": "2.0.0",
    "waves": {
        "R1A": [
            {
                "id": "ro.life.moved_home",
                "category_id": "home_address_utilities",
                "title_ro": "M-am mutat",
                "trigger_phrases_ro": ["m-am mutat"],
                "release_wave": "R1A",
                "research_status": "required",
                "production_status": "not_available",
            }
        ],
        "R1B": [
            {
                "id": "ro.life.minor_passport",
                "category_id": "identity_documents",
                "title_ro": "Fac pasaport unui minor",
                "trigger_phrases_ro": ["fac pasaport unui minor"],
                "release_wave": "R1B",
                "research_status": "required",
                "production_status": "not_available",
            }
        ],
        "R2": [
            {
                "id": "ro.life.future_thing",
                "category_id": "x",
                "title_ro": "X",
                "release_wave": "R2",
            }
        ],
    },
}


def test_canonical_id():
    assert canonical_event_type_id("ro.life.minor_passport") == "life.minor_passport"
    assert canonical_event_type_id("life.minor_passport") == "life.minor_passport"


def test_compile_scope_r1_includes_r1a_and_r1b():
    records = compile_event_types(CATALOG, scope=("R1",))
    assert {r.id for r in records} == {"life.moved_home", "life.minor_passport"}


def test_record_field_mapping():
    records = compile_event_types(CATALOG, scope=("R1",))
    mp = next(r for r in records if r.id == "life.minor_passport")
    assert mp.title_ro == "Fac pasaport unui minor"
    assert mp.category_id == "identity_documents"
    assert mp.release_wave == "R1B"
    assert mp.schema_version == "2.0.0"
    assert mp.trigger_phrases_ro == ["fac pasaport unui minor"]
    assert mp.description_ro is None
    assert mp.parent_event_id is None


def test_as_content_row_keys():
    records = compile_event_types(CATALOG, scope=("R1",))
    row = records[0].as_content_row()
    assert set(row) == {
        "id",
        "category_id",
        "title_ro",
        "description_ro",
        "trigger_phrases_ro",
        "parent_event_id",
        "release_wave",
        "research_status",
        "production_status",
        "schema_version",
    }


def test_scope_r2_only():
    records = compile_event_types(CATALOG, scope=("R2",))
    assert {r.id for r in records} == {"life.future_thing"}


def test_title_missing_is_skipped():
    catalog = {
        "schema_version": "2.0.0",
        "waves": {"R1A": [{"id": "ro.life.notitle", "category_id": "x", "release_wave": "R1A"}]},
    }
    assert compile_event_types(catalog, scope=("R1",)) == []


def test_records_sorted_by_id():
    records = compile_event_types(CATALOG, scope=("R1",))
    assert [r.id for r in records] == sorted(r.id for r in records)
