# Bounded Contexts — 25k Global Workforce

Canonical DDD map. Phase 1 scaffold only; no service implementation until approval.

Isolation key on every aggregate: `(tenantId, regionCode)`. Physical data lives in a PostgreSQL shard per region. Cross-region reads go through published events or an explicit read model — never SQL joins.

## Shared Kernel (`com.globalhr.common`)

Value objects only — no workflow:

| Type | Meaning |
|------|---------|
| `TenantId` | Legal employer / brand partition |
| `RegionCode` | `AMER` \| `EMEA` \| `APAC` — shard + residency |
| `EmployeeId` | Opaque workforce identifier (issued by Workforce) |
| `CorrelationId` | Request/event trace |
| `Money` | Amount + ISO-4217 currency |
| `AuditMeta` | actor, at, source |

Kernel types may be copied as published-language contracts. Do not share JPA entities across contexts.

---

## 1. Identity & Access (IAM) — `auth-service`

**Purpose.** Authenticate principals, authorize actions, bind enterprise IdPs.

**Core aggregates.** `Tenant`, `Principal`, `Role`, `PermissionSet`, `IdpBinding`, `Session`.

**Invariants.**
- A principal belongs to exactly one tenant.
- Roles are tenant-scoped; 50+ job roles via permission sets, not hardcoded enums.
- Region is a claim, not a tenant. Data residency is enforced by region claim + shard router.
- SSO: OIDC (primary) and SAML 2.0 (enterprise IdP). Auth-service is the OAuth2 resource-server + client broker, not the IdP of record.

**Ubiquitous language.** Principal (not User), Role, Permission, IdP, Session.

**Upstream.** None (system of record for identity).
**Downstream.** All other BCs consume JWT + `X-Tenant-Id` / `X-Region`.

**Kafka.** `hr.iam.principal-provisioned`, `hr.iam.role-changed`, `hr.iam.session-revoked`.

---

## 2. Workforce (Employee Directory) — `employee-service`

**Purpose.** Employee master data, assignments, org structure.

**Core aggregates.** `Employee`, `Assignment`, `Position`, `OrgUnit`, `Location`.

**Invariants.**
- Employee identity is issued here; IAM Principal may reference `EmployeeId`.
- Org chart is a forest per tenant+region. Cross-region manager links are correlation IDs, not FKs.
- PII stays in-region. Search index (Phase 2: Elasticsearch) is a region-local read model.

**Ubiquitous language.** Employee, Assignment, OrgUnit, Position, Location.

**Upstream.** IAM (authz). Talent Acquisition (hire events).
**Downstream.** Compensation, Notifications, Analytics.

**Kafka.** `hr.workforce.employee-hired`, `hr.workforce.employee-transferred`, `hr.workforce.org-changed`.

---

## 3. Compensation (Payroll & Benefits) — `payroll-service`

**Purpose.** Pay calculation, benefits eligibility, tax jurisdiction.

**Core aggregates.** `PayrollCalendar`, `PayrollRun`, `PayElement`, `BenefitPlan`, `TaxJurisdiction`, `PayResult`.

**Invariants.**
- Never owns employee master; subscribes to Workforce events.
- Multi-currency via `Money`. FX rates are input, not calculated here.
- Tax jurisdiction is a first-class aggregate (country + subdivision + treaty).
- Monthly runs are Spring Batch (Phase 2); saga = run per region, never a global 2PC.

**Upstream.** Workforce.
**Downstream.** Notifications (payslip available), Analytics.

**Kafka.** `hr.compensation.run-started`, `hr.compensation.run-completed`, `hr.compensation.payslip-ready`.

---

## 4. Talent Acquisition — `recruitment-service`

**Purpose.** Requisitions, candidates, interviews, offers.

**Core aggregates.** `Requisition`, `Candidate`, `Application`, `Interview`, `Offer`.

**Invariants.**
- Candidates are not employees. Hire publishes `hr.talent.offer-accepted`; Workforce creates `Employee`.
- Requisition org/position IDs are Workforce references (anti-corruption layer).

**Upstream.** IAM, Workforce (org/position catalog).
**Downstream.** Workforce (hire), Notifications.

**Kafka.** `hr.talent.requisition-opened`, `hr.talent.offer-accepted`, `hr.talent.application-withdrawn`.

---

## 5. Workforce Communications — `notification-service`

**Purpose.** Templated, preference-aware delivery (mail, push, in-app).

**Core aggregates.** `NotificationTemplate`, `Delivery`, `ChannelPreference`.

**Invariants.**
- Generic downstream BC. No HR business rules.
- Honor region for data residency of message bodies (PII).

**Kafka (consume).** All `hr.*.*` events that map to a template. **Produce:** `hr.notify.delivered`, `hr.notify.failed`.

---

## 6. Compliance & People Analytics (Phase 2)

Not a runtime module in Phase 1. Observes domain events into an append-only audit store (GDPR/CCPA) and a real-time dashboard projection (WebSocket). Owned as a separate BC so operational services stay write-optimized.

---

## What is out of bounds

| Temptation | Rule |
|------------|------|
| Shared `Employee` JPA entity | Forbidden. Published language + events. |
| Cross-region reporting SQL | Use Analytics read model. |
| Authz checks only at gateway | Defense in depth; each service validates JWT + tenant + region. |
| Global payroll saga | Region-local batch; compensate via events. |
