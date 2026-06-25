"""Test fixtures for the discovery API slice.

The real taxonomy ships every intent as production_status=not_available (nothing
is published yet), which is the faithful production state. To exercise the
serving logic we inject a small *active* fixture catalog via the FastAPI
dependency override, so tests never depend on on-disk catalog files.
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from acteos_api.discovery import DiscoveryService, get_discovery_service
from acteos_api.main import app
from acteos_intent_resolver import RankingConfig, RomanianNormalizer

TAXONOMY: dict = {
    "schema_version": "2.1.0-test",
    "locale": "ro-RO",
    "categories": [
        {"id": "identity_documents", "title_ro": "Acte de identitate", "icon_key": "id", "order": 1},
        {"id": "vehicle_mobility", "title_ro": "Ma\u0219in\u0103 \u0219i mobilitate", "order": 2},
        {"id": "family_children", "title_ro": "Familie \u0219i copii", "order": 3},
    ],
    "intents": [
        {
            "id": "ro.intent.identity.renew_expired_id",
            "category_id": "identity_documents",
            "kind": "direct_goal",
            "title_ro": "Re\u00eennoie\u0219te buletinul expirat",
            "outcome_ro": "Act de identitate valabil",
            "aliases_ro": ["buletin expirat", "act de identitate expirat"],
            "production_status": "active",
            "release_wave": "R1A",
        },
        {
            "id": "ro.intent.identity.obtain_or_renew_passport",
            "category_id": "identity_documents",
            "kind": "direct_goal",
            "title_ro": "Ob\u021bine sau re\u00eennoie\u0219te pa\u0219aportul",
            "outcome_ro": "Pa\u0219aport valabil",
            "aliases_ro": ["pasaport", "reinnoire pasaport"],
            "production_status": "active",
            "release_wave": "R1B",
        },
        {
            "id": "ro.intent.vehicle.register_used_purchase_ro",
            "category_id": "vehicle_mobility",
            "kind": "direct_goal",
            "title_ro": "\u00cenmatriculeaz\u0103 o ma\u0219in\u0103 cump\u0103rat\u0103 din Rom\u00e2nia",
            "outcome_ro": "Ma\u0219in\u0103 \u00eenmatriculat\u0103 pe numele t\u0103u",
            "aliases_ro": ["inmatriculare masina", "inmatriculez masina"],
            "production_status": "active",
            "release_wave": "R1A",
        },
        {
            "id": "ro.intent.family.register_child_birth",
            "category_id": "family_children",
            "kind": "direct_goal",
            "title_ro": "\u00cenregistreaz\u0103 na\u0219terea copilului",
            "outcome_ro": "Certificat de na\u0219tere",
            "aliases_ro": ["certificat de nastere"],
            "production_status": "not_available",
            "release_wave": "R1B",
        },
    ],
}


@pytest.fixture(scope="session")
def discovery_service() -> DiscoveryService:
    return DiscoveryService(TAXONOMY, RankingConfig(), RomanianNormalizer())


@pytest.fixture()
def client(discovery_service: DiscoveryService):
    app.dependency_overrides[get_discovery_service] = lambda: discovery_service
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
