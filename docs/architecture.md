Janus/
├── BE/                           # Mã nguồn Backend (Python/FastAPI hoặc tương tự)
│   ├── src/
│   │   ├── agent/                # Logic liên quan đến AI agent
│   │   ├── controllers/          # Request handlers/Routing (Tiếp nhận HTTP requests)
│   │   ├── core/                 # Cấu hình lõi (Settings, Database connection, v.v.)
│   │   ├── middlewares/          # Các middleware của ứng dụng (Auth, Logging, v.v.)
│   │   ├── repositories/         # Tương tác với Database (Data Access Layer)
│   │   ├── services/             # Logic nghiệp vụ (Business logic)
│   │   └── app.py                # Điểm vào chính của ứng dụng Backend
│   ├── venv/                     # Môi trường ảo Python (Virtual Environment)
│   ├── Dockerfile                # File build Docker image cho BE
│   └── pyproject.toml            # Quản lý thư viện phụ thuộc Python (Poetry/Pipenv)
│
├── FE/                           # Mã nguồn Frontend (Nuxt.js / Vue.js)
│   ├── assets/                   # Tài nguyên tĩnh chưa biên dịch (SASS, images, fonts)
│   ├── components/               # Các UI components tái sử dụng được (Vue components)
│   ├── pages/                    # Các trang của ứng dụng (tạo Router tự động trong Nuxt)
│   ├── public/                   # Tài nguyên tĩnh phục vụ trực tiếp ở chế độ root (favicon, v.v.)
│   ├── .nuxt/                    # Thư mục build và config tự động của Nuxt
│   ├── node_modules/             # Thư viện phụ thuộc Node.js
│   ├── app.vue                   # Component gốc của ứng dụng Nuxt
│   ├── nuxt.config.ts            # Cấu hình ứng dụng Nuxt.js
│   ├── package.json              # Quản lý thư viện phụ thuộc Node.js
│   ├── package-lock.json         # Lockfile phiên bản thư viện
│   └── tsconfig.json             # Cấu hình TypeScript
│
├── mobile/                       # Ứng dụng Mobile (React Native / Expo)
│   ├── src/
│   │   ├── screens/              # Các màn hình (ChatScreen, v.v.)
│   │   ├── components/           # UI components (MessageBubble, ChatInput)
│   │   ├── hooks/                # Custom hooks (useChat)
│   │   └── constants/            # Theme, cấu hình
│   ├── App.tsx                   # Component gốc
│   ├── app.json                  # Cấu hình Expo
│   ├── metro.config.js           # Cấu hình Metro cho monorepo
│   └── package.json
│
├── shared/                       # Package dùng chung (FE + Mobile)
│   ├── src/
│   │   ├── types/                # Message, ChatResponse, v.v.
│   │   ├── api/                  # sendMessage, getHistory
│   │   └── constants.ts          # getApiBase
│   └── package.json              # @janus/shared
│
├── deploy/                       # Cấu hình triển khai dự án (Deployment)
│   ├── docker-compose.yml        # Tệp cấu hình chạy Docker compose (Môi trường Production)
│   ├── .env.example              # Mẫu file .env cho deploy
│   └── README.md                 # Hướng dẫn deploy cụ thể
│
├── docs/                         # Tài liệu của dự án
│
├── scripts/                      # Các kịch bản tiện ích (bash, shell, python scripts)
│   └── tests/                    # Scripts liên quan đến việc chạy test
│
├── tests/                        # Source code các bài Unit Test/Integration Test cho toàn dự án
│
├── .github/                      # Cấu hình GitHub (Workflows rỗng CI/CD, issue templates...)
├── .pytest_cache/                # Bộ nhớ đệm của tool Pytest
│
├── docker-compose.dev.yml        # Cấu hình Docker compose dùng cho môi trường Development
├── Makefile                      # Chứa các tập lệnh (commands) chạy tự động (VD: make dev, make build...)
├── README.md                     # Tài liệu giới thiệu chính của dự án 
├── .env                          # Các biến môi trường của hệ thống
├── .env.example                  # File mẫu định nghĩa các biến môi trường
└── .gitignore                    # Bỏ qua các file/folder khi push lên Git
