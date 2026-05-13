<p align="center">
  <h1 align="center">✈️ AeroMind API</h1>
  <p align="center"><strong>Backend de IA multi-agente para la gestión inteligente de aeropuertos</strong></p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/PostgreSQL-17-336791?logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Google_Gemini-2.0_Flash-4285F4?logo=google&logoColor=white" alt="Gemini">
  <img src="https://img.shields.io/badge/Licencia-MIT-green" alt="Licencia">
</p>

---

## 🌟 ¿Qué es AeroMind?

AeroMind es una API REST que impulsa un asistente inteligente de aeropuerto. Los pasajeros y operadores interactúan con ella a través de una **interfaz de chat en lenguaje natural**. Detrás de escena, un **orquestador** impulsado por Google Gemini clasifica cada mensaje y lo enruta al agente de IA más adecuado.

Cada agente puede llamar a herramientas reales del aeropuerto — buscar vuelos, rastrear equipaje, registrar incidencias — a través de un servidor **Model Context Protocol (MCP)**. Los agentes que tratan con políticas y procedimientos también realizan **Generación Aumentada con Recuperación (RAG)** sobre un almacén de documentos oficiales respaldado por **pgvector**.

---

## 🏗️ Visión General de la Arquitectura

```mermaid
graph TD
    Client["🌐 Cliente HTTP"] --> API

    subgraph API["⚡ FastAPI"]
        R["/auth · /flights · /bookings\n/baggage · /chat · /incidents · /documents"]
    end

    API --> Orch["🧠 Orquestador\nGemini LLM · temperature=0\nClasificación de intención"]

    Orch -->|"✈️ consultas de vuelos"| FA["FlightAgent"]
    Orch -->|"🧳 consultas de equipaje"| BA["BaggageAgent"]
    Orch -->|"💬 soporte y políticas"| SA["SupportAgent"]
    Orch -->|"🔒 seguridad y procedimientos"| SeA["SecurityAgent"]

    FA --> MCP
    BA --> MCP
    SA --> RAG
    SeA --> RAG

    subgraph MCP["🔌 Servidor MCP · FastMCP"]
        T["9 herramientas del aeropuerto"]
    end

    subgraph RAG["📚 Sistema RAG"]
        E["Gemini Embeddings\n3072 dimensiones"]
        V[("pgvector\nsimilitud coseno")]
        E --> V
    end

    MCP --> AppL
    RAG --> AppL

    subgraph AppL["📋 Capa de Aplicación"]
        UC["Casos de uso · DTOs · Puertos"]
    end

    AppL --> DB[("🐘 PostgreSQL 17\n+ pgvector")]
```

### Capas de Clean Architecture

```mermaid
graph BT
    style Domain fill:#1e3a5f,stroke:#4a9eff,color:#e8f4ff
    style Application fill:#1a3a2a,stroke:#4aff8c,color:#e8fff0
    style Infra fill:#3a1e3a,stroke:#cc4aff,color:#f0e8ff
    style API fill:#3a2a1a,stroke:#ff8c4a,color:#fff0e8

    Domain["💎 Dominio\nEntidades · Objetos de Valor · Excepciones de Dominio"]
    Application["📋 Aplicación\nCasos de Uso · Puertos · DTOs"]
    Infra["🔧 Infraestructura\nSQLAlchemy · Gemini · JWT · bcrypt"]
    API["🌐 API\nRouters · Middleware · Dependencias"]

    Application --> Domain
    Infra --> Application
    API --> Application
```

---

## 🛠️ Stack Tecnológico

| Tecnología                      | Propósito                                                      |
| ------------------------------- | -------------------------------------------------------------- |
| ⚡ **FastAPI**                  | Framework REST asíncrono                                       |
| 🗄️ **SQLAlchemy 2 (async)**     | ORM con soporte de sesión asíncrona                            |
| 🐘 **PostgreSQL 17 + pgvector** | BD relacional + búsqueda de similitud vectorial                |
| 🔄 **Alembic**                  | Migraciones de base de datos                                   |
| 🤖 **Google Gemini**            | LLM (`gemini-2.0-flash`) + Embeddings (`gemini-embedding-001`) |
| 🔌 **FastMCP**                  | Servidor Model Context Protocol para herramientas de agentes   |
| ✅ **Pydantic v2**              | Validación de datos y gestión de configuración                 |
| 🔐 **bcrypt**                   | Hashing de contraseñas                                         |
| 🪙 **JWT (PyJWT)**              | Autenticación sin estado                                       |
| 📦 **Poetry**                   | Gestión de dependencias                                        |
| 🐳 **Docker / Docker Compose**  | Contenedorización                                              |
| 🧪 **pytest + pytest-asyncio**  | Pruebas                                                        |
| 🔍 **ruff**                     | Linting                                                        |
| 🔬 **mypy**                     | Verificación de tipos estática                                 |

---

## 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener:

- 🐳 **Docker** y **Docker Compose** v2 — verifica con `docker compose version`
- 🐍 **Python 3.12+** — solo necesario para desarrollo local
- 📦 **Poetry** — instala con `pip install poetry`
- 🔑 **Clave de API de Google AI Studio** con acceso a Gemini — [obtén una aquí](https://aistudio.google.com/app/apikey)

---

## 🚀 Inicio Rápido con Docker

La forma más rápida de ejecutar el stack completo (base de datos + API) es con Docker Compose.

**① Clona el repositorio**

```bash
git clone https://github.com/blandev/aeromind-api.git
cd aeromind-api
```

**② Crea tu archivo de entorno**

```bash
cp .env.example .env
```

Abre `.env` y completa tus valores:

```env
# PostgreSQL (usado por docker-compose)
POSTGRES_USER=aeromind
POSTGRES_PASSWORD=aeromind
POSTGRES_DB=aeromind
POSTGRES_PORT=5432

# URL de la base de datos — usa este formato cuando ejecutas dentro de Docker
DATABASE_URL=postgresql+asyncpg://aeromind:aeromind@db:5432/aeromind

# JWT — genera una clave con: openssl rand -hex 32
JWT_SECRET_KEY=reemplaza-con-una-cadena-aleatoria-larga
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=60

# Google Gemini
GOOGLE_API_KEY=tu-clave-de-api-aqui
GOOGLE_EMBEDDING_MODEL=models/gemini-embedding-001
```

**③ Inicia todos los servicios**

```bash
docker compose up -d
```

Esto levanta dos contenedores:

| Contenedor | Descripción                | Puerto |
| ---------- | -------------------------- | ------ |
| `db`       | PostgreSQL 17 con pgvector | `5432` |
| `api`      | AeroMind REST API          | `8000` |

**④ Aplica las migraciones de base de datos**

El contenedor de la API inicia pero **no** ejecuta migraciones automáticamente. Ejecútalas una vez:

```bash
make migrate
```

**⑤ Abre la documentación interactiva**

Visita **[http://localhost:8000/docs](http://localhost:8000/docs)** — la UI completa de Swagger con todos los endpoints está lista.

**⑥ Registra tu primer usuario administrador**

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@aeromind.com", "password": "secret123", "role": "ADMIN"}'
```

**⑦ Inicia sesión y obtén tu token JWT**

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@aeromind.com", "password": "secret123"}'
```

Copia el `access_token` de la respuesta y úsalo como token `Bearer` en el encabezado `Authorization` para todos los endpoints protegidos.

---

## 💻 Desarrollo Local

Para el desarrollo activo, ejecuta solo la base de datos en Docker y la API localmente para obtener recarga en caliente.

**① Inicia solo la base de datos**

```bash
docker compose up -d db
```

**② Instala las dependencias**

```bash
poetry install
```

**③ Cambia la URL de la base de datos en `.env`**

```env
# Comenta la URL de Docker y usa localhost en su lugar:
DATABASE_URL=postgresql+asyncpg://aeromind:aeromind@localhost:5432/aeromind
```

**④ Aplica las migraciones**

```bash
make migrate
```

**⑤ Inicia el servidor de desarrollo**

```bash
make dev
# → http://localhost:8000 con recarga automática
```

**⑥ Ejecuta la suite de pruebas**

```bash
make test          # ejecutar pruebas
make coverage      # pruebas + reporte de cobertura
```

---

## ⚙️ Variables de Entorno

| Variable                 | Requerida | Por defecto                   | Descripción                                |
| ------------------------ | --------- | ----------------------------- | ------------------------------------------ |
| `DATABASE_URL`           | ✅        | —                             | Cadena de conexión AsyncPG                 |
| `POSTGRES_USER`          | ✅        | —                             | Usuario PostgreSQL _(solo Docker)_         |
| `POSTGRES_PASSWORD`      | ✅        | —                             | Contraseña PostgreSQL _(solo Docker)_      |
| `POSTGRES_DB`            | ✅        | —                             | Nombre de la base de datos _(solo Docker)_ |
| `POSTGRES_PORT`          | ❌        | `5432`                        | Puerto PostgreSQL expuesto                 |
| `JWT_SECRET_KEY`         | ✅        | —                             | Secreto para firmar tokens JWT             |
| `JWT_ALGORITHM`          | ❌        | `HS256`                       | Algoritmo de firma JWT                     |
| `JWT_EXPIRATION_MINUTES` | ❌        | `60`                          | Validez del token en minutos               |
| `GOOGLE_API_KEY`         | ✅        | —                             | Clave de API de Google AI Studio           |
| `GOOGLE_EMBEDDING_MODEL` | ❌        | `models/gemini-embedding-001` | Modelo de embeddings Gemini                |
| `GOOGLE_LLM_MODEL`       | ❌        | `models/gemini-2.0-flash`     | Modelo LLM Gemini                          |

---

## 🔗 Endpoints de la API

### 🔐 Autenticación

| Método | Ruta             | Auth    | Descripción                           |
| ------ | ---------------- | ------- | ------------------------------------- |
| `POST` | `/auth/register` | Público | Registrar un nuevo usuario            |
| `POST` | `/auth/login`    | Público | Iniciar sesión y recibir un token JWT |

### ✈️ Vuelos

| Método | Ruta                   | Auth       | Descripción                                     |
| ------ | ---------------------- | ---------- | ----------------------------------------------- |
| `GET`  | `/flights`             | Cualquiera | Buscar vuelos (`origin`, `destination`, `date`) |
| `GET`  | `/flights/{flight_id}` | Cualquiera | Obtener un vuelo específico por ID              |

### 📋 Reservas

| Método | Ruta                       | Auth      | Descripción                              |
| ------ | -------------------------- | --------- | ---------------------------------------- |
| `GET`  | `/bookings/{booking_id}`   | Pasajero+ | Obtener una reserva por ID               |
| `GET`  | `/bookings/user/{user_id}` | Pasajero+ | Obtener todas las reservas de un usuario |

### 🧳 Equipaje

| Método | Ruta                         | Auth      | Descripción                                                       |
| ------ | ---------------------------- | --------- | ----------------------------------------------------------------- |
| `GET`  | `/baggage/{tag}`             | Pasajero+ | Rastrear equipaje por número de etiqueta                          |
| `POST` | `/baggage/{tag}/report-lost` | Pasajero+ | Reportar equipaje perdido _(crea una incidencia automáticamente)_ |

### ⚠️ Incidencias

| Método | Ruta         | Auth      | Descripción                  |
| ------ | ------------ | --------- | ---------------------------- |
| `POST` | `/incidents` | Operador+ | Crear una nueva incidencia   |
| `GET`  | `/incidents` | Operador+ | Listar todas las incidencias |

### 📚 Documentos _(RAG)_

| Método | Ruta                | Auth       | Descripción                                   |
| ------ | ------------------- | ---------- | --------------------------------------------- |
| `POST` | `/documents/ingest` | Admin      | Ingerir un documento en el almacén vectorial  |
| `POST` | `/documents/search` | Cualquiera | Búsqueda semántica sobre documentos ingeridos |

### 🤖 Chat _(IA)_

| Método | Ruta    | Auth      | Descripción                               |
| ------ | ------- | --------- | ----------------------------------------- |
| `POST` | `/chat` | Pasajero+ | Enviar un mensaje al sistema multi-agente |

**Ejemplo:**

```json
// Solicitud
{ "message": "¿Cuál es el estado del vuelo AM-201?" }

// Respuesta
{
  "response": "El vuelo AM-201 sale de BOG a las 08:30 y llega a MDE a las 09:20. Estado: A TIEMPO.",
  "agent": "flight_agent"
}
```

### 🏥 Salud

| Método | Ruta      | Auth    | Descripción                          |
| ------ | --------- | ------- | ------------------------------------ |
| `GET`  | `/health` | Público | Verificación del estado del servicio |

---

## 👤 Roles de Usuario

| Rol            | Nivel de Acceso                                    |
| -------------- | -------------------------------------------------- |
| 🧑 `PASSENGER` | Chat, rastreo de equipaje, ver reservas            |
| 🛂 `OPERATOR`  | Todo lo anterior + gestión de incidencias          |
| 👑 `ADMIN`     | Acceso completo incluyendo ingestión de documentos |

---

## 🤖 El Sistema de IA

### Flujo Multi-Agente

```mermaid
sequenceDiagram
    actor U as 👤 Usuario
    participant O as 🧠 Orquestador
    participant A as 🤖 Agente Especializado
    participant G as ✨ Gemini LLM
    participant T as 🔧 Herramientas / RAG

    U->>O: POST /chat { message }
    O->>G: Clasificar intención (temperature=0)
    G-->>O: "flight_agent" | "baggage_agent" | "support_agent" | "security_agent"
    O->>A: run(message)

    loop Bucle Agéntico (hasta 5 rondas)
        A->>G: mensaje + declaraciones de herramientas
        G-->>A: function_call(nombre, args)
        A->>T: ejecutar herramienta
        T-->>A: resultado de herramienta (JSON)
        A->>G: function_response
    end

    G-->>A: respuesta de texto final
    A-->>U: { response, agent }
```

### Agentes Especializados

| Agente             | Maneja                                     | Herramientas                           |
| ------------------ | ------------------------------------------ | -------------------------------------- |
| ✈️ `FlightAgent`   | Búsquedas de vuelos y consultas de estado  | `search_flights`, `get_flight`         |
| 🧳 `BaggageAgent`  | Rastreo de equipaje y reportes de pérdida  | `track_baggage`, `report_lost_baggage` |
| 💬 `SupportAgent`  | Políticas, FAQs, asistencia general        | `search_policies` _(RAG)_              |
| 🔒 `SecurityAgent` | Procedimientos y regulaciones de seguridad | `search_policies` _(RAG)_              |

---

### 📚 Sistema RAG

El `SupportAgent` y el `SecurityAgent` fundamentan sus respuestas en documentos oficiales del aeropuerto mediante RAG.

```mermaid
flowchart LR
    subgraph Ingestion["📥 Ingestión (POST /documents/ingest)"]
        direction TB
        D["📄 Documento\nde texto plano"]
        C["Fragmentos\n500 chars · 50 solapamiento"]
        E["Embeddings\nGemini · 3072 dims"]
        D --> C --> E
    end

    DB[("🐘 pgvector")]
    E --> DB

    subgraph Retrieval["🔍 Recuperación (al momento del chat)"]
        direction TB
        Q["❓ Consulta del\nUsuario"]
        QE["Embedding de\nConsulta"]
        TOP["Top-5 fragmentos\nsimilitud coseno"]
        Q --> QE --> TOP
    end

    DB --> TOP
    TOP --> R["💬 Respuesta\nFundamentada"]
```

---

### 🔌 Servidor MCP

AeroMind expone un servidor **Model Context Protocol (MCP)** mediante [FastMCP](https://github.com/jlowin/fastmcp), permitiendo que cualquier cliente compatible con MCP (como Claude Desktop) llame directamente a las herramientas del aeropuerto.

| Herramienta           | Descripción                                        |
| --------------------- | -------------------------------------------------- |
| `search_flights`      | Buscar vuelos disponibles                          |
| `get_flight`          | Obtener detalles de un vuelo específico            |
| `get_booking`         | Obtener una reserva por ID                         |
| `get_user_bookings`   | Obtener todas las reservas de un usuario           |
| `track_baggage`       | Rastrear equipaje por etiqueta                     |
| `report_lost_baggage` | Reportar equipaje perdido                          |
| `create_incident`     | Crear una incidencia del aeropuerto                |
| `get_incidents`       | Listar todas las incidencias                       |
| `search_documents`    | Búsqueda semántica sobre documentos del aeropuerto |

---

## 📁 Estructura del Proyecto

```
aeromind-api/
├── app/
│   ├── agents/                  # 🤖 Sistema multi-agente
│   │   ├── base_agent.py        #    Clase base del bucle agéntico
│   │   ├── rag_agent.py         #    Base para agentes con capacidad RAG
│   │   ├── orchestrator.py      #    Clasificación de intención + enrutamiento
│   │   ├── flight_agent.py
│   │   ├── baggage_agent.py
│   │   ├── support_agent.py
│   │   └── security_agent.py
│   ├── api/
│   │   ├── routers/             # 🌐 Manejadores de rutas FastAPI
│   │   ├── auth.py              #    Middleware JWT
│   │   └── dependencies.py      #    Inyección de dependencias
│   ├── application/
│   │   ├── use_cases/           # 📋 Lógica de negocio (un archivo por caso de uso)
│   │   ├── ports/               #    Interfaces de repositorios y servicios
│   │   ├── dtos/                #    Objetos de Transferencia de Datos
│   │   └── exceptions/          #    Excepciones de nivel de aplicación
│   ├── domain/
│   │   ├── entities/            # 💎 Entidades centrales del negocio
│   │   └── exceptions/          #    Excepciones de nivel de dominio
│   ├── infrastructure/
│   │   ├── config/              # ⚙️  Configuración (pydantic-settings)
│   │   ├── database/            #    Modelos SQLAlchemy, sesión, base
│   │   ├── repositories/        #    Implementaciones concretas SQLAlchemy
│   │   └── services/            #    Implementaciones de Gemini, JWT, bcrypt
│   ├── mcp/
│   │   ├── server.py            # 🔌 Definición del servidor FastMCP
│   │   └── tools/               #    Un archivo por categoría de herramienta
│   └── main.py                  # 🚀 App FastAPI + manejadores de excepciones
├── migrations/                  # 🔄 Archivos de migración Alembic
├── tests/                       # 🧪 Suite de pruebas pytest
├── docker-compose.yml
├── Dockerfile
├── Makefile
├── pyproject.toml
└── .env.example
```

---

## 🧰 Comandos del Makefile

| Comando                    | Descripción                                            |
| -------------------------- | ------------------------------------------------------ |
| `make dev`                 | Iniciar servidor de desarrollo con recarga en caliente |
| `make test`                | Ejecutar la suite de pruebas                           |
| `make coverage`            | Ejecutar pruebas con reporte de cobertura              |
| `make lint`                | Linting con ruff                                       |
| `make type-check`          | Verificación de tipos con mypy                         |
| `make migrate`             | Aplicar todas las migraciones pendientes               |
| `make migrate-gen m="msg"` | Generar una nueva migración                            |
| `make migrate-down`        | Revertir la última migración                           |
| `make docker-up`           | Iniciar todos los servicios Docker                     |
| `make docker-down`         | Detener todos los servicios Docker                     |
| `make docker-logs`         | Seguir los logs de Docker                              |
| `make docker-build`        | Reconstruir las imágenes Docker                        |
| `make db-shell`            | Abrir una shell psql dentro del contenedor             |

---

## ⚡ CI/CD

Flujo de trabajo de GitHub Actions (`.github/workflows/ci.yml`) que se ejecuta en cada push y pull request:

```mermaid
flowchart LR
    Push["📤 git push /\nPull Request"] --> Lint["🔍 Lint\nruff check"]
    Lint --> Types["🔬 Verificación de tipos\nmypy"]
    Types --> Tests["🧪 Pruebas\npytest --cov"]
    Tests --> Done["✅ Todos los checks\npasaron"]
```

**Secretos de GitHub requeridos:**

| Secreto          | Descripción                                      |
| ---------------- | ------------------------------------------------ |
| `DATABASE_URL`   | Cadena de conexión de la base de datos de prueba |
| `JWT_SECRET_KEY` | Cualquier cadena aleatoria para las pruebas      |
| `GOOGLE_API_KEY` | Clave de API de Google AI Studio                 |

---

## 📄 Licencia

[MIT](LICENSE)
