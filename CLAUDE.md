# Global HR Platform

Java 21, Spring Boot 3.5, Angular 18+, Nx MF. Multi-tenant, region-sharded PG, Kafka, Redis.

## Trees
- `backend/`: Maven. Services `auth|employee|payroll|recruitment|notification`. Infra `gateway|eureka|config`.
- `frontend/`: Nx. Apps `hr-shell|admin-portal|employee-self-service`. Libs `ui|data-access|util`.
- `docs/`: DDD + APIs. `/read` on demand; never paste into chat.

## Java
`com.globalhr.<bc>.{api|application|domain|infrastructure}`
Require `X-Tenant-Id`, `X-Region`. No cross-region SQL. Kafka `hr.<bc>.<event>`.

## Angular
Prefix `hr`. Standalone + signals. One feature/lib per PR.

## Agents
One service OR one Angular module per turn. Diffs, not full files. After each: `/clear`.
Ignore `target,build,node_modules,.git,*.log,dist,coverage` (`.claudeignore`).
Sonnet=code; Haiku=DTO/CSS; Opus=DDD/sagas.
Phase 2 only after approval.
