# Chapter 5 — Data, regions, and the law

**In one sentence:** a tenant is *who the employer is*; a region is *where the data is allowed to sit*. Every row, cache key, and event must know both.

If you remember one chapter after a week, remember this one.

---

## Tenant is not region

| | Tenant | Region |
|--|--------|--------|
| Question it answers | Which company/brand is this? | Which residency shard is this? |
| Example | `AETHER-GLOBAL` | `EMEA` |
| Header | `X-Tenant-Id` | `X-Region` |
| Typical mistake | Using “Europe” as a tenant | Using tenant as a way to fake residency |

A single tenant (one employer) **will** have employees in AMER, EMEA, and APAC at the same time. Those people do not share a PostgreSQL instance. They share a company, a login broker, and an employee-ID scheme.

A principal’s token carries a region *claim*: this session is allowed to work in EMEA. The gateway and every service must refuse a request that says tenant Aether but then tries to read the AMER shard “because the manager is in New York.” Cross-region *relationships* are IDs and events, not joins.

---

## Three databases on a laptop, three in spirit in production

Local Docker Compose:

| Name | Region | Host port | Database |
|------|--------|-----------|----------|
| postgres-amer | AMER | 5432 | `hr_amer` |
| postgres-emea | EMEA | 5433 | `hr_emea` |
| postgres-apac | APAC | 5434 | `hr_apac` |

Every business table is expected to include `tenant_id` and `region_code`. Tenant filtering is row-level (you never show tenant B to tenant A). Region is also the **connection**: the app picks the DataSource from `X-Region`. There is no “default” business database that quietly absorbs mis-routed traffic.

Phase 2 will add a `RegionDataSourceRouter`. Until then, the Compose file exists so nobody designs a schema that only works on one Postgres.

Production is the same idea with adult operations: backups, encryption, peering, and **no accidental replica** that copies EMEA PII into an AMER analytics cluster unless legal has a written basis.

---

## Why we ban cross-region SQL

A global headcount query that unions three shards inside a request:

- fails when one region is down, and takes the UI with it,
- tempts engineers to move data “to the reporting DB” without classification,
- cannot honor residency (the query *is* the leak).

The allowed path: each region emits events; **Analytics** (Phase 2) builds a number that may be slightly stale. Managers would rather see “headcount as of 14:02 UTC” than a join that is wrong *and* illegal.

---

## Redis

Cache keys look like `{tenant}:{region}:{bounded-context}:{id}`.

Sessions and hot directory snippets belong here. A cache that omits region will eventually serve a London payslip to a New York session. TTL everything. Do not use Redis as a second system of record.

---

## Kafka

Locally there is one broker so a laptop can breathe. In production, prefer **region-local clusters**. Only event types that are allowed to leave a region should be replicated, and that list is a compliance artifact, not a developer convenience.

- Topic: `hr.<domain>.<event>` — e.g. `hr.workforce.employee-hired`
- Headers: `tenantId`, `region`, `correlationId`
- Partition key: `tenantId` (so one employer’s events stay ordered enough to reason about)
- Payload: CloudEvents JSON with a published DTO, **never** a JPA entity dump
- Phase 2: transactional **outbox** in each service so “save employee” and “tell payroll” do not drift

---

## Personal data

Assume anything in Workforce, Compensation, Talent, or Notifications may be personal data.

Consequences:

- Payslip PDFs and email bodies stay in-region (the ESS mock says this out loud for a reason).
- Directory search indexes are region-local when they arrive.
- Deletion / DSAR is “find this person in this tenant+region, and the projections that copied them,” not “grep the monolith.”
- Compliance’s audit log is append-only and fed from events, so operational DBs can stay slim.

GDPR and CCPA are not a footer on the login page. They are why the shard exists.

---

## Search and org chart (coming later)

- **Search:** Elasticsearch (or similar) per region, fed from Workforce events. The UI virtual-scrolls; the API uses cursors, never `OFFSET 20000`.
- **Org chart:** adjacency list in Workforce plus a materialized path or similar projection for fast trees. Cross-region manager links stay as IDs.

---

**Previous:** [Chapter 4](04-how-the-system-is-shaped.md) · **Next:** [Chapter 6 — The applications people will use](06-the-applications.md)
