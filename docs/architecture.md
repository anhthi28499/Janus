Janus/
├── apps/
│   ├── backend/                  # Mã nguồn Backend (Python/Flask)
│   │   ├── src/
│   │   │   ├── agent/            # Logic liên quan đến AI agent (LangGraph)
│   │   │   ├── controllers/      # Request handlers/Routing
│   │   │   ├── core/             # Cấu hình lõi (Settings, Database)
│   │   │   ├── middlewares/      # Middleware (Auth, Logging)
│   │   │   ├── repositories/     # Data Access Layer
│   │   │   ├── services/         # Business logic
│   │   │   └── app.py            # Điểm vào chính
│   │   ├── tests/                # Unit & Integration tests
│   │   ├── Dockerfile
│   │   └── pyproject.toml
│   │
│   ├── web/                      # Mã nguồn Frontend (Nuxt.js)
│   │   ├── assets/
│   │   ├── components/
│   │   ├── composables/          # Nuxt auto-import hooks
│   │   ├── layouts/
│   │   ├── pages/
│   │   ├── plugins/
│   │   ├── stores/
│   │   ├── utils/
│   │   ├── public/
│   │   ├── tests/
│   │   └── nuxt.config.ts
│   │
│   └── mobile/                   # Ứng dụng Mobile (React Native / Expo)
│       ├── src/
│       │   ├── screens/
│       │   ├── components/
│       │   ├── hooks/
│       │   └── constants/
│       └── metro.config.js
│
├── packages/
│   └── shared/                   # Package dùng chung (FE + Mobile)
│       ├── src/
│       │   ├── types/
│       │   ├── api/
│       │   └── constants.ts
│       └── package.json          # @janus/shared
│
├── infra/
│   └── docker/
│       ├── docker-compose.dev.yml    # Development (Postgres, ChromaDB)
│       ├── docker-compose.prod.yml   # Production (GHCR images)
│       └── README.md
│
├── docs/
├── .github/workflows/
├── Makefile
├── package.json                 # npm workspaces: apps/*, packages/*
├── .env
├── .env.example
└── .gitignore
