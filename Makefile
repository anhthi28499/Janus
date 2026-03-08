.PHONY: help build up-db down-db down dev-be dev-fe dev-mobile logs ps clean install setup-hooks lint format test-be-unit test-be-integration test-fe-unit test-fe-e2e test-all

ifneq (,$(wildcard ./.env))
    include .env
    export
endif
help:
	@echo "Janus AI Agent Makefile commands:"
	@echo "  make up-db      Start database services (Postgres, ChromaDB)"
	@echo "  make down       Stop all services"
	@echo "  make build      Build all Docker images"
	@echo "  make dev-be     Start Backend (Flask)"
	@echo "  make dev-fe     Start Frontend (Nuxt)"
	@echo "  make logs       View logs for all services"
	@echo "  make ps         List running services"
	@echo "  make clean      Stop and remove containers, networks, images, and volumes"
	@echo "  make install    Install local dependencies (Node modules and Python venv if needed locally)"
	@echo "  make dev-mobile Start Expo mobile app (React Native)"
	@echo "  make test-all   Run all tests (BE unit/integration, FE unit)"

build:
	docker compose -f infra/docker/docker-compose.dev.yml build

up-db:
	docker compose -f infra/docker/docker-compose.dev.yml up -d database chromadb

down-db:
	docker compose -f infra/docker/docker-compose.dev.yml rm -s -f database chromadb

down:
	docker compose -f infra/docker/docker-compose.dev.yml down

dev-be:
	@echo "Starting Backend natively..."
	cd apps/backend && . venv/bin/activate && flask run --host=0.0.0.0 --port=5000

dev-fe:
	@echo "Starting Frontend natively..."
	cd apps/web && npm run dev

dev-mobile:
	@echo "Starting Mobile (Expo) natively..."
	cd apps/mobile && npx expo start

dev:
	@echo "To run development environment, please open separate terminals."
	@echo "Terminal 1: make dev-be"
	@echo "Terminal 2: make dev-fe"
	@echo "Terminal 3 (optional): make dev-mobile"

logs:
	docker compose -f infra/docker/docker-compose.dev.yml logs -f

ps:
	docker compose -f infra/docker/docker-compose.dev.yml ps

clean:
	docker compose -f infra/docker/docker-compose.dev.yml down -v --rmi all --remove-orphans

install:
	@echo "Installing Node dependencies..."
	npm install
	@echo "Installing Backend dependencies (requires python3 and venv)..."
	cd apps/backend && python3 -m venv venv && . venv/bin/activate && pip install --upgrade pip setuptools && pip install -e ".[dev]"

setup-hooks:
	@echo "Setting up Git Hooks..."
	cd apps/backend && . venv/bin/activate && pre-commit install

lint:
	@echo "Linting Backend..."
	cd apps/backend && . venv/bin/activate && ruff check .
	@echo "Linting Frontend..."
	cd apps/web && npm run lint

format:
	@echo "Formatting Backend..."
	cd apps/backend && . venv/bin/activate && ruff format .
	@echo "Formatting Frontend..."
	cd apps/web && npm run format

test-be-unit:
	@echo "Running Backend Unit Tests..."
	cd apps/backend && . venv/bin/activate && pytest tests/unit -v

test-be-integration:
	@echo "Running Backend Integration Tests..."
	cd apps/backend && . venv/bin/activate && pytest tests/integration -v

test-fe-unit:
	@echo "Running Frontend Unit Tests..."
	cd apps/web && npm run test:unit

test-fe-e2e:
	@echo "Running Frontend E2E Tests..."
	cd apps/web && npm run test:e2e

test-all: test-be-unit test-be-integration test-fe-unit
