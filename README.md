# Janus AI Agent

Janus is a modern, full-stack LangGraph-powered AI Agent designed to securely interact, retrieve context from Vector DBs, schedule, check the weather, and evaluate its own generation logic.

## Architecture & Structure
This repository represents a Monorepo containing the Nuxt 3 Frontend, Flask Python Backend, and React Native (Expo) Mobile app.

*   `apps/backend/`: Python Backend (Flask, SQLAlchemy, LangGraph, Pinecone/Chroma)
*   `apps/web/`: NuxtJS Frontend (Vue 3, Tailwind, Vitest)
*   `apps/mobile/`: React Native (Expo) Mobile app
*   `packages/shared/`: Shared TypeScript package (types, API client) for web & mobile
*   Tests live inside each app: `apps/backend/tests/`, `apps/web/tests/`
*   `infra/docker/`: Docker Compose for dev & production deployment

## Prerequisites
1.  **Node.js** (v18+)
2.  **Python** 3.10+
3.  **Docker** & Docker Compose
4.  Copy `.env.example` to `.env` and fill in necessary keys.

## Quick Start (Development)

> **After directory restructure:** Run `make install` to recreate the Python venv and reinstall npm workspaces.

The local development environment uses `Makefile` to quickly spawn the database backend alongside your raw Native code without needing constant Docker image rebuilds. 

> Note: All Environment Variables MUST be defined in `.env` as the compose files do not contain fallbacks anymore.

```bash
# 1. First time setup: Generate virtual environments and install all NPM/Pip dependencies
make install

# 2. Start PostgreSQL & ChromaDB via Docker (optional for DB-dependent features)
make up-db

# 3. Launch Backend (in a separate terminal)
make dev-be

# 4. Launch Frontend (in another terminal)
make dev-fe

# 5. (Optional) Launch Mobile app (Expo)
make dev-mobile
```
- Web app at `http://localhost:3000`
- API at `http://localhost:5000/api/v1`
- Mobile: run `make dev-mobile`, then scan QR code with Expo Go. Set `EXPO_PUBLIC_API_BASE` to your machine IP when using a physical device.

## Code Quality & Git Hooks
We use `pre-commit` for global Git hooks, **Ruff** for Python backend, and **ESLint/Prettier** for the Nuxt frontend. 

Ensure you set up your local hooks before committing to the repository:
```bash
make setup-hooks
```
You can manually run the linters and formatters using the provided Makefile commands:
```bash
# To run linters (Ruff and ESLint) without modifying files
make lint

# To run formatters (Ruff format and Prettier)
make format
```

## Running Tests
```bash
make test-all
# Or individually: make test-be-unit, make test-be-integration, make test-fe-unit
```

## Production Deployment
See [infra/docker/README.md](./infra/docker/README.md) for deployment using GitHub Container Registry images.
