# Chapter 2 — What we have today

**In one sentence:** you can compile the backend, open mock screens in the frontend, and run regional databases locally — but you cannot yet hire someone, pay someone, or sign in with a real company IdP.

This chapter exists so nobody briefs a steering committee as if the product were live.

---

## The two clocks

There is a **program clock** and a **code clock**. They are not the same.

| Clock | What it means |
|-------|----------------|
| Program | A multi-year HR platform for a global workforce |
| Code (today) | Phase 1: structure, conventions, clickable UI, empty services |

Phase 2 — real IAM, directory, payroll engine, analytics — **does not start until it is explicitly approved**. That is a delivery control, not a documentation footnote.

---

## What is real (you can prove it)

**Backend**

- A Maven multi-module project on **Java 21**, **Spring Boot 3.5.15**, **Spring Cloud 2025.0.3**.
- Five domain services and three infrastructure processes that **start** and answer health / `_ping`.
- Shared libraries: tenant/region types, an isolation header filter, and an OAuth2 resource-server switch (JWT is **off** until IAM is implemented).
- Unit and context-load tests that pass (`./mvnw test` in `backend/`).
- IntelliJ run configurations so a developer can start the set from one compound config.

**Frontend**

- An Nx workspace with three Angular 18 applications: a shell, an admin portal, and employee self-service.
- Module Federation wiring: the shell is the host; the other two are remotes.
- Mock pages with a consistent theme and static “Aether Dynamics” data.
- Shared libraries for UI, HTTP access, and small utilities.

**Local data plane**

- Docker Compose: three Postgres instances (AMER / EMEA / APAC), Redis, and Kafka.
- These are for local development. They are not a production topology.

**Documentation**

- Domain map, context map, data strategy, API conventions, mock screenshots, and this handbook.

---

## What is theatre (on purpose)

| You will see… | It means… |
|---------------|-----------|
| Pretty admin dashboards with 25,412 headcount | Hard-coded mock numbers |
| SSO screen with Okta/SAML copy | Visual contract. No IdP is connected |
| Payroll “62% complete” | A picture of a future batch UI |
| `/_ping` on each service | The process is alive. The domain is not |
| `hr.security.jwt.enabled: false` | Local services will start without Keycloak/Okta |

The screenshots in `docs/mockups/` are **design comps**. The Angular routes are **the same screens as clickable HTML**. Neither talks to payroll math or a real employee store.

---

## What is deliberately not here yet

These were named as Phase 2 modules and then stopped:

- **Module A — IAM:** real OIDC/SAML, 50+ roles, tenant provisioning.
- **Module B — Directory:** Elasticsearch/Cassandra search, virtual scroll against live data, live org chart.
- **Module C — Payroll:** Spring Batch monthly runs, multi-currency, multi-tax.
- **Module D — Analytics & compliance:** WebSocket dashboards, GDPR/CCPA audit log as a product.

Also not here: Kubernetes manifests, production IdP config, real secrets, CI/CD beyond what GitHub already provides, and a working `npm` lockfile install in this repository’s cloud agents (the frontend is scaffolded; `npm install` is the developer’s first local step).

---

## How to talk about status in a meeting

Use this wording:

> “Phase 1 is complete as an architecture scaffold. Services boot. The three applications have mock user journeys. No personal data is processed. The next funded increment is Module A (identity), which unlocks everything else.”

Avoid:

> “We have a global HR platform in production.”  
> “Payroll is implemented.”  
> “SSO works.”

Those statements will become true only after the matching Phase 2 work is done and tested.

---

## Why ship a scaffold at all?

Because the expensive mistakes happen in the *shape*, not in the 200th payroll rule.

If every team invents its own `User` table, its own idea of “region,” and its own way to call APIs, we will spend a year untangling it. Phase 1 freezes:

- package and module names,
- tenant + region on every request,
- which service owns employees vs pay vs candidates,
- how the three UIs fit together,
- how a laptop boots the same topology.

That is the deliverable. Treat it as a contract, not as unfinished decoration.

---

**Previous:** [Chapter 1](01-why-this-exists.md) · **Next:** [Chapter 3 — The business, in six parts](03-the-business-in-six-parts.md)
