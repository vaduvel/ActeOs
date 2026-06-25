SHELL := /usr/bin/env bash
.DEFAULT_GOAL := help

.PHONY: help doctor bootstrap up down format lint typecheck migrate seed-verified test-unit test-contract test-integration test-android test-web test-security test-all build-all smoke-local

help:
	@printf '%s\n' 'doctor bootstrap up down format lint typecheck migrate seed-verified test-all build-all smoke-local'

doctor:
	@./scripts/doctor.sh

bootstrap:
	@./scripts/bootstrap.sh

up:
	@docker compose up -d postgres minio mailpit

down:
	@docker compose down

format:
	@pnpm format && uv run ruff format . && ./gradlew spotlessApply

lint:
	@pnpm lint && uv run ruff check . && ./gradlew lint

typecheck:
	@pnpm typecheck && uv run mypy services packages && ./gradlew compileDebugKotlin

migrate:
	@uv run alembic -c services/api/alembic.ini upgrade head

seed-verified:
	@uv run python scripts/seed_verified.py

test-unit:
	@uv run pytest -m unit && pnpm test:unit && ./gradlew testDebugUnitTest

test-contract:
	@uv run pytest -m contract && pnpm test:contract

test-integration:
	@uv run pytest -m integration

test-android:
	@./gradlew testDebugUnitTest connectedDebugAndroidTest

test-web:
	@pnpm --filter curator test && pnpm --filter curator build

test-security:
	@./scripts/security_scan.sh

test-all: lint typecheck test-unit test-contract test-integration test-web
	@./gradlew testDebugUnitTest

build-all:
	@uv build && pnpm build && ./gradlew assembleRelease

smoke-local:
	@./scripts/smoke_local.sh
