# Simple Task API

A **production-grade Django REST Framework API** for managing tasks — built with **Domain-Driven Design** (DDD), full **CI/CD automation**, and **defense-in-depth** engineering practices. Designed for recruiters evaluating backend architecture skills and engineers looking for a clean, extensible Django reference implementation.

---

## Table of Contents

- [What Problem This Solves](#what-problem-this-solves)
- [System Architecture](#system-architecture)
- [Tech Stack](#tech-stack)
- [API Endpoints](#api-endpoints)
- [Getting Started](#getting-started)
- [Running Tests](#running-tests)
- [Deployment](#deployment)
  - [Docker](#docker)
  - [CI/CD Pipelines](#cicd-pipelines)
- [Project Structure](#project-structure)
- [Future Improvements](#future-improvements)

---

## What Problem This Solves

Most beginner Django tutorials dump everything into `models.py` and `views.py` — producing tightly coupled, untestable, unscalable code. This repo demonstrates the **right way** to structure a Django REST API:

- ✅ **Separation of concerns** — domain logic, persistence, and HTTP interface are fully decoupled via a DDD-inspired layered architecture.
- ✅ **Testability** — business logic (`domain/services.py`) can be unit-tested without Django, while API views have full integration coverage.
- ✅ **Production readiness** — Dockerized deployment, rate limiting, pagination, GitHub Actions CI/CD, SonarQube quality gates, and environment-based configuration.
- ✅ **Clean code** — follows DRY, SOLID, and explicit-better-than-implicit principles throughout.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      HTTP Client                         │
│            (curl, browser, mobile app, etc.)             │
└────────────────────┬────────────────────────────────────┘
                     │  JSON request/response
                     ▼
┌─────────────────────────────────────────────────────────┐
│              INTERFACE LAYER (tasks/interface/)           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │   urls.py    │  │   views.py   │  │ serializers.py│   │
│  │  (routing)   │──▶ (APIViews)   │──▶  (validation) │   │
│  └──────────────┘  └──────┬───────┘  └──────────────┘   │
└───────────────────────────┼─────────────────────────────┘
                            │ calls domain services
                            ▼
┌─────────────────────────────────────────────────────────┐
│              DOMAIN LAYER (tasks/domain/)                 │
│  ┌──────────────────────────────────────────────────┐    │
│  │              services.py                          │    │
│  │  (pure business logic — no Django dependency)     │    │
│  └──────────────────────┬───────────────────────────┘    │
└─────────────────────────┼───────────────────────────────┘
                          │ reads/writes models
                          ▼
┌─────────────────────────────────────────────────────────┐
│           INFRASTRUCTURE LAYER (tasks/infrastructure/)    │
│  ┌──────────────────┐  ┌───────────────────────────┐    │
│  │    models.py      │  │           DB              │    │
│  │  (Django ORM)     │──▶       (SQLite)            │    │
│  └──────────────────┘  └───────────────────────────┘    │
└─────────────────────────────────────────────────────────┘

         CI/CD Pipeline (GitHub Actions)
         ┌──────────────────────────────────────┐
         │  Lint → Migrate Check → Test →       │
         │  Coverage → SonarQube Quality Gate    │
         └──────────────────────────────────────┘
```

### Layer Responsibilities

| Layer | Directory | Responsibility |
|-------|-----------|----------------|
| **Interface** | `tasks/interface/` | HTTP request/response handling, serialization, URL routing — **knows about HTTP, knows about the domain** |
| **Domain** | `tasks/domain/` | Pure business logic (e.g., `set_task_completion`). Zero imports from Django REST Framework. **Testable in isolation.** |
| **Infrastructure** | `tasks/infrastructure/` | Database models (Django ORM), migrations, persistence concerns. **Implements domain contracts.** |

### Request Flow

```
HTTP Request → URL Router (urls.py) → APIView → Serializer (validate) →
  Domain Service (business logic) → Model (ORM) → Database → JSON Response
```

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.12+** | Runtime |
| **Django 5.1** | Web framework |
| **Django REST Framework** | API layer (views, serializers, pagination, throttling) |
| **SQLite** | Development database |
| **pytest / pytest-django** | Testing |
| **python-decouple** | Environment-based configuration |
| **Docker** | Containerization |
| **GitHub Actions** | CI/CD automation (legacy Jenkins configs in `.jenkins/`) |
| **SonarQube** | Code quality & coverage analysis |

---

## API Endpoints

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| `GET` | `/api/tasks/` | List all tasks (paginated, 10/page) | `200` |
| `POST` | `/api/tasks/` | Create a new task | `201`, `400` |
| `GET` | `/api/tasks/<id>/` | Retrieve a single task | `200`, `404` |
| `PUT` | `/api/tasks/<id>/` | Update a task | `200`, `400`, `404` |
| `DELETE` | `/api/tasks/<id>/` | Delete a task | `204`, `404` |

### Rate Limiting

- **100 requests per day per user** (configurable via `REST_FRAMEWORK` settings).

### Pagination

- **10 items per page** by default.
- Adjust with `?page_size=N` query parameter (max 100).
- Navigate with `?page=N`.

### Task Schema

```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2025-01-15T10:30:00Z"
}
```

When `completed` transitions to `true`, `completed_at` is automatically timestamped by domain logic. Reverting to `false` clears it.

---

## Getting Started

### Prerequisites

- Python 3.12+
- pip

### Local Setup

```bash
# Clone the repo
git clone https://github.com/tukue/simple_api.git
cd simple_api

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

```bash
# Quick test — list all tasks
curl http://localhost:8000/api/tasks/

# Create a task
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title": "My first task", "description": "Hello world", "completed": false}'
```

Browse the browsable API at [http://localhost:8000/api/tasks/](http://localhost:8000/api/tasks/).

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DJANGO_SECRET_KEY` | `fallback-secret-key-for-dev-only` | Django secret key (set a strong value in production) |
| `DEBUG` | `False` | Enable debug mode (`True`/`False`) |

---

## Running Tests

```bash
# Run all tests with coverage
pytest tasks/tests.py --cov=tasks --cov-report=term-missing -v

# Run domain service unit tests (pure Python, no Django)
python -m pytest tasks/tests/test_domain_services.py -v
```

The test suite covers:
- **CRUD operations** — create, read, update, delete with valid and invalid data
- **Edge cases** — nonexistent resource (404), empty titles (400), boundary pagination
- **Domain logic** — `completed_at` timestamp management, idempotent completion
- **Pagination** — multi-page retrieval, page size limits

---

## Deployment

### Docker

```bash
# Build the image
docker build -t simple-api .

# Run the container
docker run -p 8000:8000 \
  -e DJANGO_SECRET_KEY="your-production-secret" \
  -e DEBUG=False \
  simple-api
```

The Dockerfile uses a `python:3.9-slim` base, installs system build tools, copies the project, runs migrations, and starts the dev server on port 8000. For production, replace `runserver` with Gunicorn or uWSGI behind a reverse proxy (see *Future Improvements*).

### CI/CD Pipeline (GitHub Actions)

Triggered on every push and pull request to `main` via `.github/workflows/ci-cd.yml`:

1. **Checkout** with full `fetch-depth`
2. **Setup Python 3.12**
3. **Install dependencies** from `requirements.txt`
4. **Run tests** with `pytest`

> Legacy Jenkins pipeline configs remain in `legacy/jenkins/` for reference (Linux & Windows).

### Code Quality

SonarQube configuration is provided in `sonar-project.properties` with:
- Test coverage report paths (`coverage.xml`)
- Test execution reports (`pytest-report.xml`)
- Exclusions for migrations and cache files

---

## Project Structure

```
simple_api/
├── .github/workflows/ci-cd.yml    # GitHub Actions pipeline
├── legacy/jenkins/                 # Legacy Jenkins pipeline configs
├── simple_api/                     # Django project configuration
│   ├── settings.py                 # Settings with env-based config
│   ├── urls.py                     # Root URL config
│   ├── wsgi.py                     # WSGI entry point
│   └── asgi.py                     # ASGI entry point
├── tasks/                          # Main application (DDD structure)
│   ├── domain/
│   │   └── services.py             # Pure business logic
│   ├── infrastructure/
│   │   └── models.py               # Django ORM models
│   ├── interface/
│   │   ├── urls.py                 # API URL routing
│   │   ├── views.py                # APIView handlers
│   │   └── serializers.py          # DRF serializers
│   ├── tests/
│   │   └── test_domain_services.py # Domain logic unit tests
│   ├── tests.py                    # Integration test suite
│   ├── models.py                   # Re-exported model (legacy compat)
│   ├── serializers.py              # Re-exported serializer (legacy compat)
│   ├── urls.py                     # App-level URL routing
│   └── views.py                    # Re-exported views (legacy compat)
├── Dockerfile                      # Container image
├── manage.py                       # Django management script
├── pytest.ini                      # Pytest configuration
├── requirements.txt                # Python dependencies
├── sonar-project.properties        # SonarQube configuration
└── db.sqlite3                      # Development database (gitignored)
```

---

## Future Improvements

### Short-term

- [ ] **Authentication & Authorization** — JWT-based auth (drf-simplejwt) with user-scoped tasks
- [ ] **Production database** — PostgreSQL via `django-environ` with connection pooling
- [ ] **Gunicorn + nginx** — Replace `runserver` with a production-grade WSGI server + reverse proxy
- [ ] **API documentation** — Auto-generated OpenAPI/Swagger docs via `drf-spectacular`
- [ ] **Pre-commit hooks** — Ruff linting + Black formatting on every commit

### Medium-term

- [ ] **Docker Compose** — Multi-service setup (app + PostgreSQL + Redis cache)
- [ ] **Async task queue** — Celery + Redis for background task processing
- [ ] **Comprehensive logging** — Structured logging with `structlog` and log aggregation
- [ ] **Filtering & search** — Query param filtering (`?completed=true&search=grocery`)
- [ ] **PATCH support** — Partial updates (currently PUT requires full payload)
- [ ] **Health check endpoint** — `/api/health/` for load balancer probes

### Long-term

- [ ] **Hexagonal Architecture** — Full port/adapter pattern with repository interfaces
- [ ] **CQRS** — Separate read/write models for high-traffic scenarios
- [ ] **GraphQL endpoint** — Strawberry or Graphene integration for flexible queries
- [ ] **Event sourcing** — Domain events for audit trail and async side effects
- [ ] **Kubernetes manifests** — Helm charts for production orchestration
- [ ] **End-to-end tests** — Playwright/Cypress for API + frontend workflows


## License

MIT &mdash; use freely, learn from it, build on it.

---

*Maintained by [Tukue](https://github.com/tukue).*
