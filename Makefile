.DEFAULT_GOAL := help
SHELL := /bin/bash

.PHONY: help doctor bootstrap up down format lint typecheck migrate seed-verified \
	test-unit test-contract test-integration test-android test-web test-security \
	test-all build-all smoke-local

help: ## Afișează țintele disponibile
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

doctor: ## Verifică prerechizitele de toolchain (JDK 17, Python 3.13, Node, Docker)
	@echo "[doctor] TODO P0: verifică versiunile de toolchain"

bootstrap: ## Instalează dependențele pentru toate workspace-urile
	@echo "[bootstrap] TODO P0: instalează deps android/services/packages/curator-web"

up: ## Pornește infrastructura locală (Postgres + MinIO)
	docker compose up -d

down: ## Oprește infrastructura locală
	docker compose down

format: ## Rulează formatatoarele
	@echo "[format] TODO"

lint: ## Rulează linterele
	@echo "[lint] TODO"

typecheck: ## Rulează verificările de tipuri
	@echo "[typecheck] TODO"

migrate: ## Aplică migrațiile de bază de date
	@echo "[migrate] TODO P1: alembic upgrade head"

seed-verified: ## Încarcă doar seed-urile oficiale verificate
	@echo "[seed-verified] TODO P8"

test-unit: ## Teste unitare
	@echo "[test-unit] TODO"

test-contract: ## Teste de contract
	@echo "[test-contract] TODO"

test-integration: ## Teste de integrare
	@echo "[test-integration] TODO"

test-android: ## Teste Android
	@echo "[test-android] TODO"

test-web: ## Teste portal curator
	@echo "[test-web] TODO"

test-security: ## Gate-uri de securitate (SAST/deps/secret scan)
	@echo "[test-security] TODO"

test-all: ## Rulează toate testele
	@echo "[test-all] TODO"

build-all: ## Build pentru toate artefactele deployabile
	@echo "[build-all] TODO"

smoke-local: ## Smoke test pe mediul local
	@echo "[smoke-local] TODO P0"
