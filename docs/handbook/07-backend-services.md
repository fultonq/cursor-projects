# Chapter 7 — Backend services, one by one

**In one sentence:** eight Java processes, two shared libraries, one Maven reactor; domain services are empty on purpose.

Parent coordinates: `backend/pom.xml` — group `com.globalhr`, version `1.0.0-SNAPSHOT`.

---

## How the reactor is grouped

```text
backend/
  libs/
    common      types + isolation filter
    security    JWT resource server (optional)
  infrastructure/
    config-server
    service-registry
    api-gateway
  services/
    auth-service
    employee-service
    payroll-service
    recruitment-service
    notification-service
```

Aggregators (`libs`, `infrastructure`, `services`) are `pom` packaging. You almost never run those; you run a child.

`./mvnw` (Maven Wrapper 3.9.9) is checked in so nobody needs a global Maven install.

---

## Shared libraries

### `common`

Value objects: `TenantId`, `RegionCode` (only AMER / EMEA / APAC), `EmployeeId`, `CorrelationId`, `Money`.

`TenantContext` is a thread-local so a request can be stamped once and read in repositories later.

`IsolationHeadersFilter` reads `X-Tenant-Id`, `X-Region`, `X-Correlation-Id`. Health and `_ping` skip the filter so load balancers do not need a tenant. Missing tenant/region on a *business* call should become a hard 400 in Phase 2; today the filter only *sets* context when both headers exist.

Registered via Spring Boot auto-configuration (servlet apps only). The gateway is WebFlux and does not load this filter — isolation is re-checked in each servlet service.

### `security`

Two filter chains:

- `hr.security.jwt.enabled=true` → OAuth2 resource server, everything authenticated except actuator and `_ping`.
- default / `false` → permit all, so a laptop without Okta still boots.

Do not “leave it false” in any shared environment. The switch exists for Phase 1 ergonomics.

---

## Infrastructure processes

**Config Server (:8888).** Native profile, configs on the classpath under `config/`. Shared `application.yml` currently turns JWT off. Each service still has a local `application.yml` and `spring.config.import: optional:configserver:...` so a missing config server does not brick a unit test.

**Service registry (:8761).** Eureka. The server does not register with itself.

**API gateway (:8080).** Spring Cloud Gateway. Routes by path prefix to `lb://<service>`. This is the only URL the Angular `ApiClient` should ever see (via the shell’s reverse proxy or an environment URI).

---

## Domain services (stubs)

Each has:

- a `*Application` class,
- a `PingController` on `/api/v1/<short-name>/_ping`,
- a context-load test with config and Eureka switched off.

| Service | Port | Ping | Bounded context |
|---------|------|------|-----------------|
| auth-service | 8081 | `/api/v1/auth/_ping` | IAM |
| employee-service | 8082 | `/api/v1/employee/_ping` | Workforce |
| payroll-service | 8083 | `/api/v1/payroll/_ping` | Compensation |
| recruitment-service | 8084 | `/api/v1/recruitment/_ping` | Talent |
| notification-service | 8085 | `/api/v1/notification/_ping` | Communications |

When you implement a service, grow it *inside that module*: `api` (HTTP), `application` (use cases), `domain` (aggregates), `infrastructure` (JPA, Kafka). Do not add a sixth service for “shared employees.” That is how we get a distributed monolith.

OpenAPI files (`openapi.yaml`) are added **per service when that service becomes real**. Until then, `docs/api/README.md` is the contract baseline: Bearer token, three isolation headers, RFC 7807 errors, cursor pagination.

---

## HTTP habits worth enforcing in review

- Public path: `/api/v1/<context>/...`
- Errors: `application/problem+json`
- Directory-scale lists: `?cursor=&limit=` — never `?page=400`
- Correlation ID: accept inbound or mint one; always echo it back

---

## What a “first real endpoint” should look like

Example: Workforce “get employee.”

1. Controller in `employee-service` under `com.globalhr.employee.api`.
2. Require tenant + region headers; 400 if absent.
3. Load from the EMEA (or claimed) DataSource only.
4. Return a DTO, not an entity.
5. If the employee moved region, do not follow them with a second SQL hop; return a code the UI can understand.

Anything larger than that belongs in a design note in `docs/`, not in a surprise pull request.

---

**Previous:** [Chapter 6](06-the-applications.md) · **Next:** [Chapter 8 — Security without the whitepaper](08-security.md)
