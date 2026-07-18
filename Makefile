.DEFAULT_GOAL := help
SHELL := /bin/bash

# Python packages installed editable into the shared .venv (Python 3.13).
# uv is the canonical installer per the architecture doc; fall back to pip.
PY_PACKAGES := packages/contracts packages/rule-engine packages/source-ingestion services/api

.PHONY: help doctor bootstrap up down format lint typecheck migrate seed-verified \
        test-unit test-contract test-integration test-android test-web test-security test-all \
        codegen codegen-check build-all smoke-local

help:
	@echo "Targets: doctor bootstrap up down format lint typecheck migrate seed-verified"
	@echo "         test-unit test-integration test-android test-web test-security test-all"
	@echo "         codegen codegen-check build-all smoke-local"

# ---------------------------------------------------------------------------
# Environment checks
# ---------------------------------------------------------------------------

doctor:
	@echo "== toolchain check =="
	@command -v uv       >/dev/null && echo "  uv:       $$($(command -v uv) --version)"      || echo "  uv:       MISSING"
	@command -v python3  >/dev/null && echo "  python3:  $$(python3 --version)"               || echo "  python3:  MISSING"
	@command -v docker   >/dev/null && docker info --format '  docker:    {{.ServerVersion}}' 2>/dev/null || echo "  docker:   not running (integration tests will skip)"
	@command -v node     >/dev/null && echo "  node:     $$(node --version)"                  || echo "  node:     MISSING"
	@command -v pnpm     >/dev/null && echo "  pnpm:     $$(pnpm --version)"                  || echo "  pnpm:     MISSING"
	@command -v java     >/dev/null && echo "  java:     $$(java -version 2>&1 | head -1)"    || echo "  java:     MISSING"

# ---------------------------------------------------------------------------
# Python environment
# ---------------------------------------------------------------------------

VENV := .venv
PY   := $(VENV)/bin/python
PIP  := $(VENV)/bin/python -m pip

$(VENV)/bin/activate:
	uv venv --python 3.13 $(VENV)

bootstrap: $(VENV)/bin/activate
	@for p in $(PY_PACKAGES); do \
		echo "== $$p =="; \
		uv pip install -e "$$p[dev]" --python $(VENV)/bin/python; \
	done

# ---------------------------------------------------------------------------
# Local services (docker-compose: postgres:17 + minio)
# ---------------------------------------------------------------------------

up:
	docker compose up -d

down:
	docker compose down

# ---------------------------------------------------------------------------
# Quality gates
# ---------------------------------------------------------------------------

format:
	@for p in $(PY_PACKAGES); do echo "== $$p =="; (cd $$p && ruff format .); done

lint:
	@for p in $(PY_PACKAGES); do echo "== $$p =="; (cd $$p && ruff check .); done

typecheck:
	@for p in $(PY_PACKAGES); do echo "== $$p =="; (cd $$p && mypy src); done

# ---------------------------------------------------------------------------
# Database migrations (services/api)
# ---------------------------------------------------------------------------

migrate:
	cd services/api && alembic upgrade head

migrate-new:
	@test -n "$(MSG)" || (echo "Usage: make migrate-new MSG='description'" && exit 1)
	cd services/api && alembic revision --autogenerate -m "$(MSG)"

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

# Unit tests: pure, in-memory, no Docker. Always run.
test-unit:
	@for p in $(PY_PACKAGES); do echo "== $$p =="; (cd $$p && python -m pytest -q -m "not integration"); done

# Integration tests: need Docker (testcontainers spins up postgres:17).
test-integration:
	cd services/api && python -m pytest -q -m "integration"

# P4+ — not yet implemented.
test-contract:
	@echo "[test-contract] TODO P4"
test-android:
	@echo "[test-android] TODO P6"
test-web:
	cd apps/curator-web && pnpm vitest run
test-security:
	@echo "[test-security] TODO P9"

seed-verified:
	@echo "[seed-verified] TODO P8"

# Everything that can run locally, runs.
test-all: test-unit test-integration
	@echo "[test-all] unit + integration complete"

# ---------------------------------------------------------------------------
# Code generation (WB-012): Python, Kotlin, TypeScript from JSON Schemas.
# ---------------------------------------------------------------------------

codegen:
	python packages/contracts/scripts/generate_python.py
	@echo "[codegen] Python models generated"
	@if [ -d apps/curator-web ]; then cd apps/curator-web && pnpm run codegen; echo "[codegen] TS models generated"; fi
	@if [ -f apps/android/gradlew ]; then cd apps/android && ./gradlew :core:contracts:generateContracts; echo "[codegen] Kotlin models generated"; fi

codegen-check:
	python packages/contracts/scripts/check_codegen.py

# ---------------------------------------------------------------------------
# Build (P10)
# ---------------------------------------------------------------------------

build-all:
	@echo "[build-all] TODO P10"

smoke-local:
	@echo "[smoke-local] TODO P0"
