# Janus AI Agent

Janus is a modern, full-stack LangGraph-powered AI Agent designed to securely interact, retrieve context from Vector DBs, schedule, check the weather, and evaluate its own generation logic.

## Architecture & Structure
This repository represents a Monorepo containing the Nuxt 3 Frontend, Flask Python Backend, and React Native (Expo) Mobile app.

*   `BE/`: Python Backend (Flask, SQLAlchemy, LangGraph, Pinecone/Chroma)
    *   `src/ controllers, middlewares, services, core, repositories, agent`
*   `FE/`: NuxtJS Frontend (Vue 3, Vanilla CSS, Vitest)
*   `mobile/`: React Native (Expo) Mobile app (Chat feature)
*   `shared/`: Shared TypeScript package (types, API client) used by mobile and FE
*   `tests/`: Unified Root Test Suite 
    *   `BE/unit`, `BE/integration`
    *   `FE/unit`, `FE/integration`
*   `scripts/tests/`: Bash scripts to execute testing pipelines manually or via CI.
*   `deploy/`: Deployment folder for remote `.env` execution and using GHCR images.

## Prerequisites
1.  **Node.js** (v18+)
2.  **Python** 3.10+
3.  **Docker** & Docker Compose
4.  Copy `.env.example` to `.env` and fill in necessary keys.

## Quick Start (Development)
The local development environment uses `Makefile` to quickly spawn the database backend alongside your raw Native code without needing constant Docker image rebuilds. 

> Note: All Environment Variables MUST be defined in `.env` as the compose files do not contain fallbacks anymore.

```bash
# 1. First time setup: Generate virtual environments and install all NPM/Pip dependencies
make install

# 2. Start PostgreSQL & Local ChromaDB via Docker, and launch the Backend natively
make dev-be

# 3. (In a separate terminal) Launch Frontend natively
make dev-fe

# 4. (Optional) Launch Mobile app (Expo)
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
Run the entire testing suite (unit & integration) globally:
```bash
./scripts/tests/test_all.sh
```

## Production Deployment
Please read the [deploy/README.md](./deploy/README.md) file to see how to spin up Janus via GitHub Container Registry images.
