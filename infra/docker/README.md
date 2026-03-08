# Janus Docker

## Development

`docker-compose.dev.yml` provides PostgreSQL and ChromaDB for local development.

```bash
# From project root
make up-db
# or
docker compose -f infra/docker/docker-compose.dev.yml up -d database chromadb
```

## Production Deployment

`docker-compose.prod.yml` is intended for production. It pulls pre-built images from `ghcr.io` for backend and frontend.

**Steps:**
1. Install Docker and Docker Compose on your host.
2. Copy `infra/docker/` (including .env.example) to your server.
3. Create `.env` from `.env.example`:

```bash
# Postgre configuration
POSTGRES_USER=my_secure_user
POSTGRES_PASSWORD=my_secure_pass
POSTGRES_DB=janus_db

# External Keys
OPENAI_API_KEY=sk-your-openai-key
PINECONE_API_KEY=your-pinecone
PINECONE_ENV=us-east-1
```

4. Launch:
```bash
docker compose -f docker-compose.prod.yml --env-file .env up -d
```

Frontend: port 3000, Backend: port 5000. Use Nginx reverse proxy for production.
