.PHONY: help build up down restart logs ps clean install

ifneq (,$(wildcard ./.env))
    include .env
    export
endif
help:
	@echo "Janus AI Agent Makefile commands:"
	@echo "  make up         Start all services via Docker Compose in detached mode"
	@echo "  make down       Stop all services"
	@echo "  make build      Build all Docker images"
	@echo "  make restart    Restart all services"
	@echo "  make logs       View logs for all services"
	@echo "  make ps         List running services"
	@echo "  make clean      Stop and remove containers, networks, images, and volumes"
	@echo "  make install    Install local dependencies (Node modules and Python venv if needed locally)"
	@echo "  make dev-mobile Start Expo mobile app (React Native)"

build:
	docker compose -f docker-compose.dev.yml build

up-db:
	docker compose -f docker-compose.dev.yml up -d database chromadb

down-db:
	docker compose -f docker-compose.dev.yml rm -s -f database chromadb

down:
	docker compose -f docker-compose.dev.yml down

dev-be:
	@echo "Starting Backend natively..."
	cd BE && . venv/bin/activate && flask run --host=0.0.0.0 --port=5000

dev-fe:
	@echo "Starting Frontend natively..."
	cd FE && npm run dev

dev-mobile:
	@echo "Starting Mobile (Expo) natively..."
	cd mobile && npx expo start

dev:
	@echo "To run development environment, please open separate terminals."
	@echo "Terminal 1: make dev-be"
	@echo "Terminal 2: make dev-fe"
	@echo "Terminal 3 (optional): make dev-mobile"

logs:
	docker compose -f docker-compose.dev.yml logs -f

ps:
	docker compose -f docker-compose.dev.yml ps

clean:
	docker compose -f docker-compose.dev.yml down -v --rmi all --remove-orphans

install:
	@echo "Installing Node dependencies (FE, mobile, shared)..."
	npm install
	@echo "Installing BE dependencies (requires python3 and venv)..."
	cd BE && python3 -m venv venv && . venv/bin/activate && pip install --upgrade pip setuptools && pip install -e ".[dev]"

setup-hooks:
	@echo "Setting up Git Hooks..."
	cd BE && . venv/bin/activate && pre-commit install

lint:
	@echo "Linting Backend..."
	cd BE && . venv/bin/activate && ruff check .
	@echo "Linting Frontend..."
	cd FE && npm run lint

format:
	@echo "Formatting Backend..."
	cd BE && . venv/bin/activate && ruff format .
	@echo "Formatting Frontend..."
	cd FE && npm run format
