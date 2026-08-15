# Chapter 10 — How we deliver from here

**In one sentence:** freeze the shape, fund one module at a time, and do not start payroll engineering until identity and workforce events are boring.

---

## The delivery rule that already exists

Phase 2 is gated. The written order is:

| Module | Name | Why this order |
|--------|------|----------------|
| A | Identity and access | Nothing else can be trusted without a real principal, tenant, and region claim |
| B | Global employee directory | Payroll and talent need a stable `EmployeeId` and org |
| C | Payroll and benefits | Needs payees from workforce events; batches are high blast radius |
| D | Analytics and compliance | Needs a river of events worth recording |

Skipping to C because “finance is the sponsor” produces a second employee master inside payroll. We have seen that movie.

UI work can proceed **in parallel as mocks** (it already has). Live data on a screen still follows A→B→C.

---

## Suggested team seams (not org-chart law)

| Team | Owns | Does not own |
|------|------|----------------|
| Platform | Gateway, Eureka, config, observability, region router | HR rules |
| Identity | auth-service, IdP contracts, RBAC model | Employee PII |
| Workforce | employee-service, directory UI, org chart | Pay calculation |
| Talent | recruitment-service, pipeline UI | Creating employees |
| Compensation | payroll-service, batch, tax tables | Employee master |
| Experience | shell, ESS, design system | Direct DB access |
| Compliance (later) | audit store, DSAR exports, dashboards | Operational writes |

Two teams may share a library (`common`, `ui`). They may not share a table.

---

## How engineers should change the code

These rules are also in `CLAUDE.md` for agents; humans should follow the spirit:

- One service **or** one Angular feature per pull request when the change is large.
- Prefer diffs over rewriting whole files.
- Put long API specs and DDD maps in `docs/` — do not paste them into every ticket.
- After a module is done, drop the giant log/stack-trace context; the next chat should `/read` a doc instead.
- Package names: `com.globalhr.<context>.<layer>`.
- Selector prefix: `hr`. Standalone components, signals for new state.

---

## Decisions already made (do not relitigate weekly)

1. Java 21 / Spring Boot 3.5 / Spring Cloud 2025.0 on the server.  
2. Angular 18 / Nx 19 / Module Federation on the client.  
3. PostgreSQL shard per region; Redis; Kafka events.  
4. Eureka for local service discovery (Consul was the alternative; we picked Eureka for laptop simplicity).  
5. OIDC primary, SAML backup.  
6. Cursor pagination for big lists.  
7. JWT off only on developer machines.

If you want to change one of these, write a one-page ADR in `docs/` and get it signed. Do not sneak Consul in beside Eureka “for a spike” that never dies.

---

## Risks worth funding attention

| Risk | What it looks like | Mitigation |
|------|--------------------|------------|
| Distributed monolith | Every PR touches four services | Context map; ACL reviews |
| Residency leak | “Just replicate EMEA to the US search cluster” | Region in the key; compliance on the replicator allow-list |
| Fake SSO forever | JWT stays false in staging | Environment checklist in Module A |
| Batch blast radius | One job updates all regions | One run per region; compensate with events |
| 25k list in the browser | Offset pagination, no virtual scroll | Cursor API + virtual scroll in Module B |
| Eventual consistency surprise | Payslip UI before payroll commit | Outbox + explicit “not ready” states |
| Agent / vendor sprawl | Five chat sessions, five styles | This handbook + `CLAUDE.md` |

---

## Open questions (managers can close these)

1. **Who is the IdP of record** in production — Okta, Entra, both, by tenant?  
2. **How many legal tenants** on day one — one global brand or many subsidiaries as tenants?  
3. **Which event types may cross a region boundary?** Write the list before Kafka replicator exists.  
4. **Who operates payroll calendars** — HR ops, finance, or a shared service?  
5. **Retention:** how long do payslips and audit events live, per region?  
6. **Support model:** does a global helpdesk see all regions (via analytics) or file tickets that stay in-region?

Until (1) and (2) are answered, Module A can still build the broker, but it cannot pick production issuer URLs.

---

## What to approve next

A sensible steering-committee motion:

> Approve Module A (IAM): OIDC/SAML broker, tenant+region claims, RBAC storage, JWT on in every non-local environment. Directory and payroll remain mock until A is in a staging-like environment.

Everything in this repository is ready for that conversation. It is not ready to replace the current HR suite.

---

**Previous:** [Chapter 9](09-running-it-locally.md) · **Start:** [Handbook home](README.md) · **Glossary:** [glossary.md](glossary.md)
