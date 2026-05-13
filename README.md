<p align="center">
  <h1 align="center">✈️ AeroMind API</h1>
  <p align="center"><strong>Multi-agent AI backend for intelligent airport management</strong></p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/PostgreSQL-17-336791?logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Google_Gemini-2.0_Flash-4285F4?logo=google&logoColor=white" alt="Gemini">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
</p>

---

## 🌟 What is AeroMind?

AeroMind is a production-ready REST API that powers an intelligent airport assistant. Passengers and operators interact with it through a **natural language chat interface**. Behind the scenes, an **orchestrator** powered by Google Gemini classifies every message and routes it to the most suitable specialized AI agent.

Each agent can call real airport tools — searching flights, tracking baggage, filing incidents — via a **Model Context Protocol (MCP)** server. Agents that deal with policies and procedures also perform **Retrieval-Augmented Generation (RAG)** over an official document store backed by **pgvector**.

---

## 🏗️ Architecture Overview

```mermaid
graph TD
    Client["🌐 HTTP Client"] --> API

    subgraph API["⚡ FastAPI"]
        R["/auth · /flights · /bookings\n/baggage · /chat · /incidents · /documents"]
    end

    API --> Orch["🧠 Orchestrator\nGemini LLM · temperature=0\nIntent classification"]

    Orch -->|"✈️ flight queries"| FA["FlightAgent"]
    Orch -->|"🧳 baggage queries"| BA["BaggageAgent"]
    Orch -->|"💬 support & policies"| SA["SupportAgent"]
    Orch -->|"🔒 security & procedures"| SeA["SecurityAgent"]

    FA --> MCP
    BA --> MCP
    SA --> RAG
    SeA --> RAG

    subgraph MCP["🔌 MCP Server · FastMCP"]
        T["9 airport tools"]
    end

    subgraph RAG["📚 RAG System"]
        E["Gemini Embeddings\n3072 dimensions"]
        V[("pgvector\ncosine similarity")]
        E --> V
    end

    MCP --> AppL
    RAG --> AppL

    subgraph AppL["📋 Application Layer"]
        UC["Use Cases · DTOs · Ports"]
    end

    AppL --> DB[("🐘 PostgreSQL 17\n+ pgvector")]
```

### Clean Architecture Layers

```mermaid
graph BT
    style Domain fill:#1e3a5f,stroke:#4a9eff,color:#e8f4ff
    style Application fill:#1a3a2a,stroke:#4aff8c,color:#e8fff0
    style Infra fill:#3a1e3a,stroke:#cc4aff,color:#f0e8ff
    style API fill:#3a2a1a,stroke:#ff8c4a,color:#fff0e8

    Domain["💎 Domain\nEntities · Value Objects · Domain Exceptions"]
    Application["📋 Application\nUse Cases · Ports · DTOs"]
    Infra["🔧 Infrastructure\nSQLAlchemy · Gemini · JWT · bcrypt"]
    API["🌐 API\nRouters · Middleware · Dependencies"]

    Application --> Domain
    Infra --> Application
    API --> Application
```

---

## 🛠️ Tech Stack

| Technology                      | Purpose                                                        |
| ------------------------------- | -------------------------------------------------------------- |
| ⚡ **FastAPI**                  | Async REST framework                                           |
| 🗄️ **SQLAlchemy 2 (async)**     | ORM with async session support                                 |
| 🐘 **PostgreSQL 17 + pgvector** | Relational DB + vector similarity search                       |
| 🔄 **Alembic**                  | Database migrations                                            |
| 🤖 **Google Gemini**            | LLM (`gemini-2.0-flash`) + Embeddings (`gemini-embedding-001`) |
| 🔌 **FastMCP**                  | Model Context Protocol server for agent tools                  |
| ✅ **Pydantic v2**              | Data validation and settings management                        |
| 🔐 **bcrypt**                   | Password hashing                                               |
| 🪙 **JWT (PyJWT)**              | Stateless authentication                                       |
| 📦 **Poetry**                   | Dependency management                                          |
| 🐳 **Docker / Docker Compose**  | Containerization                                               |
| 🧪 **pytest + pytest-asyncio**  | Testing                                                        |
| 🔍 **ruff**                     | Linting                                                        |
| 🔬 **mypy**                     | Static type checking                                           |

---

## 📋 Prerequisites

Before you start, make sure you have:

- 🐳 **Docker** and **Docker Compose** v2 — verify with `docker compose version`
- 🐍 **Python 3.12+** — only needed for local development
- 📦 **Poetry** — install with `pip install poetry`
- 🔑 **Google AI Studio API key** with Gemini access — [get one here](https://aistudio.google.com/app/apikey)

---

## 🚀 Quick Start with Docker

The fastest way to run the full stack (database + API) is with Docker Compose.

**① Clone the repository**

```bash
git clone https://github.com/blandev/aeromind-api.git
cd aeromind-api
```

**② Create your environment file**

```bash
cp .env.example .env
```

Open `.env` and fill in your values:

```env
# PostgreSQL (used by docker-compose)
POSTGRES_USER=aeromind
POSTGRES_PASSWORD=aeromind
POSTGRES_DB=aeromind
POSTGRES_PORT=5432

# Database URL — use this format when running inside Docker
DATABASE_URL=postgresql+asyncpg://aeromind:aeromind@db:5432/aeromind

# JWT — generate a secret with: openssl rand -hex 32
JWT_SECRET_KEY=replace-with-a-long-random-string
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=60

# Google Gemini
GOOGLE_API_KEY=your-google-api-key-here
GOOGLE_EMBEDDING_MODEL=models/gemini-embedding-001
```

**③ Start all services**

```bash
docker compose up -d
```

This starts two containers:

| Container | Description                 | Port   |
| --------- | --------------------------- | ------ |
| `db`      | PostgreSQL 17 with pgvector | `5432` |
| `api`     | AeroMind REST API           | `8000` |

**④ Apply database migrations**

The API container starts but does **not** run migrations automatically. Run them once:

```bash
make migrate
```

**⑤ Open the interactive docs**

Visit **[http://localhost:8000/docs](http://localhost:8000/docs)** — the full Swagger UI with all endpoints is ready.

**⑥ Register your first admin user**

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@aeromind.com", "password": "secret123", "role": "ADMIN"}'
```

**⑦ Log in and get your JWT token**

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@aeromind.com", "password": "secret123"}'
```

Copy the `access_token` from the response and use it as a `Bearer` token in the `Authorization` header for all protected endpoints.

---

## 💻 Local Development

For active development, run only the database in Docker and the API locally for hot-reload.

**① Start only the database**

```bash
docker compose up -d db
```

**② Install dependencies**

```bash
poetry install
```

**③ Switch the database URL in `.env`**

```env
# Comment out the Docker URL and use localhost instead:
DATABASE_URL=postgresql+asyncpg://aeromind:aeromind@localhost:5432/aeromind
```

**④ Apply migrations**

```bash
make migrate
```

**⑤ Start the development server**

```bash
make dev
# → http://localhost:8000 with auto-reload
```

**⑥ Run the test suite**

```bash
make test          # run tests
make coverage      # run tests + coverage report
```

---

## ⚙️ Environment Variables

| Variable                 | Required | Default                       | Description                              |
| ------------------------ | -------- | ----------------------------- | ---------------------------------------- |
| `DATABASE_URL`           | ✅       | —                             | AsyncPG connection string                |
| `POSTGRES_USER`          | ✅       | —                             | PostgreSQL username _(Docker only)_      |
| `POSTGRES_PASSWORD`      | ✅       | —                             | PostgreSQL password _(Docker only)_      |
| `POSTGRES_DB`            | ✅       | —                             | PostgreSQL database name _(Docker only)_ |
| `POSTGRES_PORT`          | ❌       | `5432`                        | Exposed PostgreSQL port                  |
| `JWT_SECRET_KEY`         | ✅       | —                             | Secret for signing JWT tokens            |
| `JWT_ALGORITHM`          | ❌       | `HS256`                       | JWT signing algorithm                    |
| `JWT_EXPIRATION_MINUTES` | ❌       | `60`                          | Token validity in minutes                |
| `GOOGLE_API_KEY`         | ✅       | —                             | Google AI Studio API key                 |
| `GOOGLE_EMBEDDING_MODEL` | ❌       | `models/gemini-embedding-001` | Gemini embedding model                   |
| `GOOGLE_LLM_MODEL`       | ❌       | `models/gemini-2.0-flash`     | Gemini LLM model                         |

---

## 🔗 API Endpoints

### 🔐 Authentication

| Method | Path             | Auth   | Description                    |
| ------ | ---------------- | ------ | ------------------------------ |
| `POST` | `/auth/register` | Public | Register a new user            |
| `POST` | `/auth/login`    | Public | Log in and receive a JWT token |

### ✈️ Flights

| Method | Path                   | Auth | Description                                      |
| ------ | ---------------------- | ---- | ------------------------------------------------ |
| `GET`  | `/flights`             | Any  | Search flights (`origin`, `destination`, `date`) |
| `GET`  | `/flights/{flight_id}` | Any  | Get a specific flight by ID                      |

### 📋 Bookings

| Method | Path                       | Auth       | Description                 |
| ------ | -------------------------- | ---------- | --------------------------- |
| `GET`  | `/bookings/{booking_id}`   | Passenger+ | Get a booking by ID         |
| `GET`  | `/bookings/user/{user_id}` | Passenger+ | Get all bookings for a user |

### 🧳 Baggage

| Method | Path                         | Auth       | Description                                      |
| ------ | ---------------------------- | ---------- | ------------------------------------------------ |
| `GET`  | `/baggage/{tag}`             | Passenger+ | Track baggage by tag number                      |
| `POST` | `/baggage/{tag}/report-lost` | Passenger+ | Report lost baggage _(auto-creates an incident)_ |

### ⚠️ Incidents

| Method | Path         | Auth      | Description           |
| ------ | ------------ | --------- | --------------------- |
| `POST` | `/incidents` | Operator+ | Create a new incident |
| `GET`  | `/incidents` | Operator+ | List all incidents    |

### 📚 Documents _(RAG)_

| Method | Path                | Auth  | Description                             |
| ------ | ------------------- | ----- | --------------------------------------- |
| `POST` | `/documents/ingest` | Admin | Ingest a document into the vector store |
| `POST` | `/documents/search` | Any   | Semantic search over ingested documents |

### 🤖 Chat _(AI)_

| Method | Path    | Auth       | Description                              |
| ------ | ------- | ---------- | ---------------------------------------- |
| `POST` | `/chat` | Passenger+ | Send a message to the multi-agent system |

**Example:**

```json
// Request
{ "message": "What is the status of flight AM-201?" }

// Response
{
  "response": "Flight AM-201 departs BOG at 08:30 and arrives MDE at 09:20. Status: ON TIME.",
  "agent": "flight_agent"
}
```

### 🏥 Health

| Method | Path      | Auth   | Description          |
| ------ | --------- | ------ | -------------------- |
| `GET`  | `/health` | Public | Service health check |

---

## 👤 User Roles

| Role           | Access Level                             |
| -------------- | ---------------------------------------- |
| 🧑 `PASSENGER` | Chat, baggage tracking, view bookings    |
| 🛂 `OPERATOR`  | Everything above + incident management   |
| 👑 `ADMIN`     | Full access including document ingestion |

---

## 🤖 The AI System

### Multi-Agent Flow

```mermaid
sequenceDiagram
    actor U as 👤 User
    participant O as 🧠 Orchestrator
    participant A as 🤖 Specialized Agent
    participant G as ✨ Gemini LLM
    participant T as 🔧 Tools / RAG

    U->>O: POST /chat { message }
    O->>G: Classify intent (temperature=0)
    G-->>O: "flight_agent" | "baggage_agent" | "support_agent" | "security_agent"
    O->>A: run(message)

    loop Agentic Loop (up to 5 rounds)
        A->>G: message + tool declarations
        G-->>A: function_call(name, args)
        A->>T: execute tool
        T-->>A: tool result (JSON)
        A->>G: function_response
    end

    G-->>A: final text response
    A-->>U: { response, agent }
```

### Specialized Agents

| Agent              | Handles                             | Tools                                  |
| ------------------ | ----------------------------------- | -------------------------------------- |
| ✈️ `FlightAgent`   | Flight searches and status queries  | `search_flights`, `get_flight`         |
| 🧳 `BaggageAgent`  | Baggage tracking and lost reports   | `track_baggage`, `report_lost_baggage` |
| 💬 `SupportAgent`  | Policies, FAQs, general assistance  | `search_policies` _(RAG)_              |
| 🔒 `SecurityAgent` | Security procedures and regulations | `search_policies` _(RAG)_              |

---

### 📚 RAG System

The `SupportAgent` and `SecurityAgent` ground their responses in official airport documents using RAG.

```mermaid
flowchart LR
    subgraph Ingestion["📥 Ingestion (POST /documents/ingest)"]
        direction TB
        D["📄 Plain-text\nDocument"]
        C["Chunks\n500 chars · 50 overlap"]
        E["Embeddings\nGemini · 3072 dims"]
        D --> C --> E
    end

    DB[("🐘 pgvector")]
    E --> DB

    subgraph Retrieval["🔍 Retrieval (at chat time)"]
        direction TB
        Q["❓ User Query"]
        QE["Query Embedding"]
        TOP["Top-5 chunks\ncosine similarity"]
        Q --> QE --> TOP
    end

    DB --> TOP
    TOP --> R["💬 Grounded\nAgent Response"]
```

---

### 🔌 MCP Server

AeroMind exposes a **Model Context Protocol (MCP)** server via [FastMCP](https://github.com/jlowin/fastmcp), allowing any MCP-compatible client (such as Claude Desktop) to call airport tools directly.

| Tool                  | Description                            |
| --------------------- | -------------------------------------- |
| `search_flights`      | Search for available flights           |
| `get_flight`          | Get details of a specific flight       |
| `get_booking`         | Get a booking by ID                    |
| `get_user_bookings`   | Get all bookings for a user            |
| `track_baggage`       | Track baggage by tag                   |
| `report_lost_baggage` | Report lost baggage                    |
| `create_incident`     | Create an airport incident             |
| `get_incidents`       | List all incidents                     |
| `search_documents`    | Semantic search over airport documents |

---

## 📁 Project Structure

```
aeromind-api/
├── app/
│   ├── agents/                  # 🤖 Multi-agent system
│   │   ├── base_agent.py        #    Agentic loop base class
│   │   ├── rag_agent.py         #    Base for RAG-capable agents
│   │   ├── orchestrator.py      #    Intent classification + routing
│   │   ├── flight_agent.py
│   │   ├── baggage_agent.py
│   │   ├── support_agent.py
│   │   └── security_agent.py
│   ├── api/
│   │   ├── routers/             # 🌐 FastAPI route handlers
│   │   ├── auth.py              #    JWT middleware
│   │   └── dependencies.py      #    Dependency injection
│   ├── application/
│   │   ├── use_cases/           # 📋 Business logic (one file per use case)
│   │   ├── ports/               #    Repository & service interfaces
│   │   ├── dtos/                #    Data Transfer Objects
│   │   └── exceptions/          #    Application-level exceptions
│   ├── domain/
│   │   ├── entities/            # 💎 Core business entities
│   │   └── exceptions/          #    Domain-level exceptions
│   ├── infrastructure/
│   │   ├── config/              # ⚙️  Settings (pydantic-settings)
│   │   ├── database/            #    SQLAlchemy models, session, base
│   │   ├── repositories/        #    Concrete SQLAlchemy implementations
│   │   └── services/            #    Gemini, JWT, bcrypt implementations
│   ├── mcp/
│   │   ├── server.py            # 🔌 FastMCP server definition
│   │   └── tools/               #    One file per tool category
│   └── main.py                  # 🚀 FastAPI app + exception handlers
├── migrations/                  # 🔄 Alembic migration files
├── tests/                       # 🧪 pytest test suite
├── docker-compose.yml
├── Dockerfile
├── Makefile
├── pyproject.toml
└── .env.example
```

---

## 🧰 Makefile Commands

| Command                    | Description                        |
| -------------------------- | ---------------------------------- |
| `make dev`                 | Start dev server with hot-reload   |
| `make test`                | Run the test suite                 |
| `make coverage`            | Run tests with coverage report     |
| `make lint`                | Lint with ruff                     |
| `make type-check`          | Type check with mypy               |
| `make migrate`             | Apply all pending migrations       |
| `make migrate-gen m="msg"` | Generate a new migration           |
| `make migrate-down`        | Roll back the last migration       |
| `make docker-up`           | Start all Docker services          |
| `make docker-down`         | Stop all Docker services           |
| `make docker-logs`         | Follow Docker logs                 |
| `make docker-build`        | Rebuild Docker images              |
| `make db-shell`            | Open a psql shell in the container |

---

## ⚡ CI/CD

GitHub Actions workflow (`.github/workflows/ci.yml`) runs on every push and pull request:

```mermaid
flowchart LR
    Push["📤 git push /\nPull Request"] --> Lint["🔍 Lint\nruff check"]
    Lint --> Types["🔬 Type Check\nmypy"]
    Types --> Tests["🧪 Tests\npytest --cov"]
    Tests --> Done["✅ All checks\npassed"]
```

**Required GitHub Secrets:**

| Secret           | Description                     |
| ---------------- | ------------------------------- |
| `DATABASE_URL`   | Test database connection string |
| `JWT_SECRET_KEY` | Any random string for tests     |
| `GOOGLE_API_KEY` | Google AI Studio API key        |

---

## 📄 License

[MIT](LICENSE)
