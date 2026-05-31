# Simple Task API

A **production-grade Django REST Framework API** for task management — built with **Domain-Driven Design** (DDD), full **CI/CD automation**, and documented **architecture tradeoffs**. Designed as a reference implementation for engineers evaluating backend architecture skills.

---

## Table of Contents

- [Business Problem](#business-problem)
- [System Architecture](#system-architecture)
- [Tradeoff System Design](#tradeoff-system-design)
- [Tech Stack](#tech-stack)
- [API Endpoints](#api-endpoints)
- [Getting Started](#getting-started)
- [Running Tests](#running-tests)
- [Deployment](#deployment)
- [Project Structure](#project-structure)
- [Future Improvements](#future-improvements)

---

## Business Problem

**Who this is for:** Backend engineers, technical interviewers, and teams who need a concise, real-world example of a well-architected Django REST API.

**The problem:** Most Django tutorials and beginner projects dump all logic into `models.py` and `views.py`. This produces tightly coupled code that is difficult to test, maintain, or scale. Teams inheriting such codebases face high technical debt, low test coverage, and fear of refactoring.

**What this solves:**

- **Structured architecture** — A DDD-inspired layered pattern (Interface → Domain → Infrastructure) that enforces separation of concerns from day one.
- **Testable business logic** — `domain/services.py` has zero Django imports. Core rules can be unit-tested in pure Python (no database, no HTTP).
- **Production readiness** — Dockerized deployment, rate limiting, pagination, GitHub Actions CI/CD, and environment-based configuration.
- **Demonstrates tradeoffs** — Every architectural choice is documented with its alternatives and rationale (see [Tradeoff System Design](#tradeoff-system-design)).

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        HTTP Client                                  │
│              (curl, browser, mobile app, API client)                │
└─────────────────────────┬───────────────────────────────────────────┘
                          │ JSON request/response
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     INTERFACE LAYER (tasks/interface/)               │
│                                                                      │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────────────┐   │
│  │    urls.py      │  │   views.py     │  │   serializers.py     │   │
│  │  URL routing    │─▶│  APIView       │──▶│  JSON validation     │   │
│  │  /api/tasks/    │  │  + pagination  │  │  + deserialization   │   │
│  └────────────────┘  └───────┬────────┘  └──────────────────────┘   │
│                              │                                       │
│  Responsibility: HTTP concerns only. Parses requests, validates      │
│  input, formats responses. Never contains business rules.            │
└──────────────────────────────┼───────────────────────────────────────┘
                               │ calls domain service
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       DOMAIN LAYER (tasks/domain/)                    │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                     services.py                                │   │
│  │  Pure business logic — zero Django/DRF imports                │   │
│  │  e.g. set_task_completion(task, completed) → manages          │   │
│  │  completed_at timestamp based on completion state             │   │
│  └──────────────────────┬───────────────────────────────────────┘   │
│                                                                      │
│  Responsibility: All business rules live here. Can be unit-tested    │
│  without a database, without an HTTP request, without Django.        │
└──────────────────────────┼───────────────────────────────────────────┘
                           │ reads/writes ORM models
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   INFRASTRUCTURE LAYER (tasks/infrastructure/)       │
│                                                                      │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐   │
│  │    models.py      │  │   admin.py       │  │  SQLite / DB     │   │
│  │  Django ORM       │  │  Django Admin    │  │  persistence     │   │
│  │  Task model       │──▶│  registration    │──▶│                  │   │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘   │
│                                                                      │
│  Responsibility: Database models, migrations, persistence.           │
│  Implements the contracts defined implicitly by domain services.     │
│  The Task.save() method calls into domain logic via set_task_completion.│
└─────────────────────────────────────────────────────────────────────┘

                    ┌─────────────────────────────────────┐
                    │       CI/CD Pipeline (GitHub Actions) │
                    │  ┌─────┐ ┌──────┐ ┌────┐ ┌──────┐ │
                    │  │Lint │ │Migrate│ │Test│ │Coverage││
                    │  └─────┘ └──────┘ └────┘ └──────┘ │
                    └─────────────────────────────────────┘

                    ┌─────────────────────────────────────┐
                    │       Deployment (Docker)             │
                    │  ┌──────────┐                        │
                    │  │ Gunicorn │──▶ Port 8000            │
                    │  │ + Django│                          │
                    │  └──────────┘                        │
                    └─────────────────────────────────────┘
```

### Request Flow

```
HTTP Request
  → urls.py routes to APIView
    → Serializer validates input (400 if invalid)
      → View calls domain service (business logic)
        → Model.save() triggers ORM persistence
          → Database write
            → Serializer formats response
              → JSON response returned
```

### Layer Responsibilities

| Layer | Directory | Responsibility | Django Dependency |
|-------|-----------|----------------|-------------------|
| **Interface** | `tasks/interface/` | HTTP request/response, serialization, routing | Yes (DRF) |
| **Domain** | `tasks/domain/` | Pure business logic (`set_task_completion`) | **None** |
| **Infrastructure** | `tasks/infrastructure/` | ORM models, DB migrations, persistence | Yes (Django) |

---

## Tradeoff System Design

Every architecture is a set of tradeoffs. Below are the key decisions made in this project, the alternatives considered, and the reasoning behind each choice.

### 1. DDD-Inspired Layering vs Flat Django Structure

| | Layered (chosen) | Flat (alternative) |
|---|---|---|
| **Approach** | Separate `interface/`, `domain/`, `infrastructure/` packages | Single `models.py` + `views.py` |
| **Pros** | Business logic is testable in isolation; clear boundaries; easy to swap DB or HTTP layer | Faster to write initially; fewer files |
| **Cons** | More boilerplate; indirection for simple CRUD | Tight coupling; hard to test; fear of refactoring |
| **When to reconsider** | Prototypes or < 5 endpoints where speed matters most | Teams > 2 devs or expected lifespan > 3 months |

**Verdict:** Layering wins for any project expected to live beyond a hackathon. The cost is upfront structure; the payoff is maintainability.

### 2. APIView vs ViewSet (DRF)

| | APIView (chosen) | ModelViewSet (alternative) |
|---|---|---|
| **Approach** | Explicit `get()`, `post()`, `put()`, `delete()` methods | DRF router generates all CRUD automatically |
| **Pros** | Full control; explicit URL-to-method mapping; easier to reason about | 70% less code for standard CRUD |
| **Cons** | More repetitive code | Magic routing; harder to customise; implicit behaviour |
| **When to reconsider** | API with > 10 standard CRUD endpoints | Non-standard actions or complex validation |

**Verdict:** APIView is chosen for explicitness. In a larger project, ViewSets with custom mixins strike a better balance.

### 3. SQLite vs PostgreSQL

| | SQLite (chosen) | PostgreSQL (alternative) |
|---|---|---|
| **Approach** | File-based DB (default Django) | Separate database server |
| **Pros** | Zero setup; no external dependency; perfect for dev/CI | Concurrent writes; JSON fields; production standard |
| **Cons** | No concurrency; no schema-level users; not production-suitable | Requires Docker/install; migration overhead |
| **When to reconsider** | As soon as you deploy to production | Local dev if you want parity with prod |

**Verdict:** SQLite for development speed; PostgreSQL is the first production upgrade (see [Future Improvements](#future-improvements)).

### 4. Django REST Framework vs Raw Django

| | DRF (chosen) | Raw Django (alternative) |
|---|---|---|
| **Approach** | Use DRF views, serializers, pagination, throttling | Manual JSON parsing, `JsonResponse`, custom pagination |
| **Pros** | Battle-tested; browsable API; built-in throttling/pagination | Zero dependency; full control; lighter footprint |
| **Cons** | Heavy dependency ("magic"); learning curve for non-DRF devs | Reinvent wheels; bugs in edge cases |
| **When to reconsider** | API-first projects that already use Django | Microservices where every dependency matters |

**Verdict:** DRF is the industry standard for Django APIs. The productivity gain far outweighs the dependency cost.

### 5. Single Docker Container vs Docker Compose

| | Single Container (chosen) | Docker Compose (alternative) |
|---|---|---|
| **Approach** | One `Dockerfile`, single `docker run` command | Multi-service: app + PostgreSQL + Redis + nginx |
| **Pros** | Simple; one command to run; minimal overhead | Production-like environment; service isolation |
| **Cons** | No DB/queue separation; not production topology | Complexity; resource usage; learning curve |
| **When to reconsider** | Any deployment beyond a single VM | Local dev that needs to match production |

**Verdict:** Single container is right for this scope. Docker Compose is the natural next step (see [Future Improvements](#future-improvements)).

### 6. Offline Domain Tests vs Full Integration Tests

| | Both (chosen) | One or the Other |
|---|---|---|
| **Domain tests** (`test_domain_services.py`) | Pure unittest; no Django; no DB; runs in milliseconds | Catches business logic bugs instantly |
| **Integration tests** (`tests.py`) | Django TestCase; full request/response cycle | Catches serialization, routing, and DB issues |
| **Verdict:** Running both is minimal overhead and catches different failure modes. Domain tests fail fast (milliseconds) for logic; integration tests validate the full stack.

### 7. Rate Limiting Strategy

| | UserRateThrottle (chosen) | AnonRateThrottle / ScopedRateThrottle |
|---|---|---|
| **Approach** | 100 requests/day per user | Per-IP for anonymous; per-endpoint for granular control |
| **Pros** | Simple; works out of box with DRF | More granular control |
| **Cons** | No differentiation between auth states | More configuration |
| **When to reconsider** | Once you add auth (JWT/session) | Public endpoints need IP-based limits |

**Verdict:** `UserRateThrottle` is a reasonable default. Swap to a mix of `AnonRateThrottle` + `UserRateThrottle` when auth is added.

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
| **GitHub Actions** | CI/CD automation |
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
git clone https://github.com/tukue/simple_api.git
cd simple_api

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
```

```bash
curl http://localhost:8000/api/tasks/

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
docker build -t simple-api .

docker run -p 8000:8000 \
  -e DJANGO_SECRET_KEY="your-production-secret" \
  -e DEBUG=False \
  simple-api
```

### CI/CD Pipeline (GitHub Actions)

Triggered on every push and pull request to `main` via `.github/workflows/ci-cd.yml`:

1. Checkout with full `fetch-depth`
2. Setup Python 3.12
3. Install dependencies from `requirements.txt`
4. Run tests with `pytest`

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
