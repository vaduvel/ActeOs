.PHONY: validate dev-db api-test test-contract contracts-test db-test

PYTHON ?= python3

validate:
	$(PYTHON) infra/scripts/validate_pack.py

dev-db:
	docker compose -f infra/docker-compose.yml up -d postgres

api-test:
	cd services/api && $(PYTHON) -m pytest

test-contract:
	cd services/api && $(PYTHON) -m pytest tests/test_contract_cases_api.py

contracts-test: validate test-contract

db-test:
	cd services/api && $(PYTHON) -m pytest db_tests
