# Global HR Platform

Enterprise HR platform for 25k+ concurrent users across regions.

**Stack:** Java 21 · Spring Boot 3.5 · Spring Cloud 2025.0 · Angular 18+ · Nx Module Federation · PostgreSQL · Kafka · Redis

Phase 1 is **architecture and scaffold only**. Domain services are stubs. Phase 2 (IAM, directory, payroll, analytics) requires explicit approval.

## Repository

| Path | Role |
|------|------|
| `backend/` | Multi-module Maven reactor (services + Spring Cloud infra) |
| `frontend/` | Nx workspace (shell + micro-frontends + shared libs) |
| `docs/` | Bounded contexts, context map, API conventions (read on demand) |
| `infra/docker-compose.yml` | Local Postgres (per region), Redis, Kafka |
| `.idea/` | Shared IntelliJ code style + compound Run/Debug configs |

## Quick start (local)

```bash
# Data plane
docker compose -f infra/docker-compose.yml up -d

# Backend (from IntelliJ: run "Platform — All Services", or)
cd backend && ./mvnw -q -pl infrastructure/config-server,infrastructure/service-registry,infrastructure/api-gateway,services/auth-service spring-boot:run

# Frontend
cd frontend && npm install && npx nx serve hr-shell
```

Ports: Config `8888` · Eureka `8761` · Gateway `8080` · Auth `8081` · Employee `8082` · Payroll `8083` · Recruitment `8084` · Notification `8085` · Shell `4200`.

## Conventions

See [`CLAUDE.md`](CLAUDE.md) (agent rules), [`docs/ddd/bounded-contexts.md`](docs/ddd/bounded-contexts.md) (domain map), and [`docs/mockups/README.md`](docs/mockups/README.md) (application screens).
