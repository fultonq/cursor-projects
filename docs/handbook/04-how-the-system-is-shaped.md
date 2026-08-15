# Chapter 4 — How the system is shaped

**In one sentence:** browsers talk to one front door; that door fans out to small Java services; the UI is one shell with two product apps plugged in.

You do not need to love microservices to accept this shape. You need 25k concurrent users, several HR products, and regional data. A single deployable would make those three things fight.

---

## The picture

```text
  Employee / HR / Recruiter browsers
                 │
                 ▼
         hr-shell  (Angular, :4200)
           ├── admin-portal     (loaded as a remote)
           └── employee-self-service
                 │
                 │  HTTPS, never straight to a service
                 ▼
         API Gateway  (:8080)
                 │
     ┌───────────┼───────────┬────────────┐
     ▼           ▼           ▼            ▼
  auth:8081  employee:8082  payroll:8083  …
                 │
      Eureka (:8761)   Config (:8888)
                 │
     Postgres×3     Redis      Kafka
     AMER EMEA APAC
```

Two extra processes are not “business”:

- **Config Server** hands each service its YAML (native classpath in local dev; Git-backed in a later environment).
- **Eureka** is the phone book. The gateway says `lb://payroll-service` instead of hard-coding `localhost:8083`.

---

## Why the frontend is three apps, not one

HR admin and employee self-service have different users, release cadences, and risk. If we ship them as one giant Angular app:

- a self-service visual tweak waits on an admin payroll change,
- the JavaScript bundle grows without bound,
- teams collide in one routing tree.

**Module Federation** (Nx + webpack) lets the **shell** own login chrome, search, tenant/region badges, and top-level routes (`/admin`, `/ess`). The admin and ESS apps are **remotes**: they expose their routes and load inside the shell. You can still serve a remote alone on :4201 / :4202 while developing.

Shared code goes in libraries, not copy-paste:

| Library | Holds |
|---------|--------|
| `ui` | Look and feel, page header, theme |
| `data-access` | HTTP to the **gateway only**, isolation headers |
| `util` | Tiny helpers |

Apps must not call `http://localhost:8082` from the browser. That would bypass the front door, CORS policy, and future WAF rules.

---

## Why the backend is many processes, not one JAR

Each bounded context from Chapter 3 is a Spring Boot application. They share *libraries* (`common`, `security`), not a database.

Infrastructure is separate so domain teams do not run Eureka as a hobby:

| Process | Port | Role |
|---------|------|------|
| config-server | 8888 | Central configuration |
| service-registry | 8761 | Eureka |
| api-gateway | 8080 | Routes `/api/v1/auth/**`, `/employee/**`, … |
| auth-service | 8081 | IAM |
| employee-service | 8082 | Workforce |
| payroll-service | 8083 | Compensation |
| recruitment-service | 8084 | Talent |
| notification-service | 8085 | Communications |

Today each domain service is a stub: it boots, registers (when Eureka is up), and answers `/api/v1/<name>/_ping`. That is enough to prove the wiring. It is not enough to process a hire.

---

## Synchronous vs asynchronous

**Questions** travel HTTP: “get this payslip,” “search this page of the directory.” Prefer staying **inside one region**.

**Facts** travel Kafka: “employee hired,” “payroll run completed,” “offer accepted.” The topic name is `hr.<domain>.<event>`. Headers carry tenant, region, and a correlation ID so a trace can be followed in logs.

If a developer reaches for a REST call to *change* another domain’s state, they should stop and publish an event instead. REST between services is for queries, and even then it is a last resort.

---

## Where code lives in the repo

```text
backend/     Java / Maven
frontend/    Angular / Nx
infra/       docker-compose (local data only)
docs/        this handbook + DDD + mockups
.idea/       shared IntelliJ style and run configs
```

Java packages follow `com.globalhr.<context>.{api|application|domain|infrastructure}` once a service grows past the stub. Do not invent a seventh layer without a reason.

---

**Previous:** [Chapter 3](03-the-business-in-six-parts.md) · **Next:** [Chapter 5 — Data, regions, and the law](05-data-regions-and-the-law.md)
