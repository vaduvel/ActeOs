.PHONY: validate dev-db api-test contracts-test

PYTHON ?= python3

validate:
	$(PYTHON) infra/scripts/validate_pack.py

dev-db:
	docker compose -f infra/docker-compose.yml up -d postgres

api-test:
	cd services/api && $(PYTHON) -m pytest

contracts-test:
	$(PYTHON) infra/scripts/validate_pack.py
