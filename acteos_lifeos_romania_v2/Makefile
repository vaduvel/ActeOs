.PHONY: validate dev-db api-test contracts-test

validate:
	python infra/scripts/validate_pack.py

dev-db:
	docker compose -f infra/docker-compose.yml up -d postgres

api-test:
	cd services/api && python -m pytest

contracts-test:
	python infra/scripts/validate_pack.py
