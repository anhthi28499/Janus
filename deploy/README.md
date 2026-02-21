# Janus Deployment Guide

The `docker-compose.yml` located in this directory is intended to be used on your production server. It pulls the pre-built `latest` Docker images directly from `ghcr.io` for both the backend and frontend. 

It does **not** rely on `Dockerfile` build processes, keeping server downtime to a minimum.

## Deployment Steps

1. Install Docker and Docker Compose on your host machine.
2. Clone or download ONLY this directory to your server workspace.
3. Establish your environment variables. The `docker-compose` setup strictly requires them.

Create a `.env` file in this directory based on `.env.example`:

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

4. Launch the application:

```bash
docker-compose --env-file .env up -d
```

5. Verify services:

```bash
docker-compose logs -f
```

The Frontend will be exposed internally on port `3000` while the backend runs on port `5000`. You should map these using an Nginx reverse proxy configuration for outside web traffic.
