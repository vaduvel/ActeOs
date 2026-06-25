.DEFAULT_GOAL := help
SHELL := /bin/bash
PY_PACKAGES := packages/contracts packages/rule-engine

.PHONY: help doctor bootstrap up down format lint typecheck migrate seed-verified test-unit test-contract test-integration test-android test-web test-security test-all build-all smoke-local

help:
	@echo "Targets: doctor bootstrap up down format lint typecheck migrate seed-verified"
	@echo "         test-unit test-contract test-integration test-android test-web test-security test-all build-all smoke-local"

doctor:
	@echo "[doctor] TODO P0: verify toolchains (JDK 17, Python 3.13, Node 22, Docker)"

bootstrap:
	@for p in $(PY_PACKAGES); do echo "== $$p =="; (cd $$p && python -m pip install -e '.[dev]'); done

up:
	docker compose up -d

down:
	docker compose down

format:
	@for p in $(PY_PACKAGES); do (cd $$p && python -m ruff format .); done

lint:
	@for p in $(PY_PACKAGES); do (cd $$p && python -m ruff check .); done

typecheck:
	@for p in $(PY_PACKAGES); do (cd $$p && python -m mypy src); done

migrate:
	@echo "[migrate] TODO P1: alembic upgrade head"

seed-verified:
	@echo "[seed-verified] TODO P8"

test-unit:
	@for p in $(PY_PACKAGES); do echo "== $$p =="; (cd $$p && python -m pytest -q); done

test-contract:
	@echo "[test-contract] TODO P4"

test-integration:
	@echo "[test-integration] TODO"

test-android:
	@echo "[test-android] TODO P6"

test-web:
	@echo "[test-web] TODO P5"

test-security:
	@echo "[test-security] TODO P9"

test-all: test-unit
	@echo "[test-all] ran unit suites; other suites pending"

build-all:
	@echo "[build-all] TODO"

smoke-local:
	@echo "[smoke-local] TODO P0"
