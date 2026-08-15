# Chapter 3 — The business, in six parts

**In one sentence:** HR is not one domain. It is six, and they are allowed to disagree about the word “person.”

This chapter is the one to walk through on a whiteboard with a product owner. Code names are in parentheses so engineers can find the service later.

---

## A story that uses all six

Marcus applies for Staff Engineer (Talent). Priya, a People Partner, is not involved yet.

Leila is in interview. An offer is accepted. **Talent does not create an employee row.** It publishes “offer accepted.” **Workforce** creates Marcus as an employee in the EMEA shard and gives him `EMP-188204`.

**IAM** already had, or now has, a principal that may log in. That principal is not the employee record; it *points at* the employee ID.

On payday, **Compensation** does not read Workforce’s tables. It already received “employee hired / assignment changed” events and keeps its own idea of a *payee*. It runs EMEA only. When the run completes, **Communications** emails Marcus that a payslip is waiting. **Compliance** (later) records that a payslip containing PII was produced in-region.

If we had used one `Person` table for all of that, payroll would have been afraid to deploy, and GDPR deletion would have been a guessing game.

---

## 1. Identity and access (IAM) — `auth-service`

**Job:** answer “who is this?” and “may they do that?”

IAM talks about **principals**, not users. A principal is a login identity bound to one tenant. It might be an employee, a contractor’s admin account, or a service. Region is a *claim on the token* (where this session is allowed to work), not a second company.

Roles are not a hardcoded enum of five strings. The brief is **50+ distinct job roles**, expressed as permission sets (directory:read, payroll:run, offer:approve, and so on). That is how a People Partner and a Payroll Ops Lead can share a UI shell without sharing power.

SSO: the company already has Okta or Entra. This service is the **broker** (OIDC primary, SAML backup). It is not trying to become the corporate IdP.

---

## 2. Workforce — `employee-service`

**Job:** the employee master. If Workforce and payroll disagree about someone’s title, Workforce wins.

This is names, assignments, positions, org units, locations. The org chart is a **forest per tenant and region**. A manager in AMER for someone in EMEA is a correlation, not a foreign key that crosses shards.

PII stays in the region that owns the employee. Search at 25k+ scale is a later, region-local index — not `SELECT *` through the gateway.

---

## 3. Compensation — `payroll-service`

**Job:** calculate pay and benefits under real-world tax geography.

Compensation is allergic to owning HR master data. Internally it maps incoming workforce events into a **payee**. Money is always amount + currency. Tax jurisdiction is a first-class thing (country, subdivision, treaty), not a string on the employee.

Monthly runs are batches (Spring Batch in Phase 2), **one run per region**. There is no two-phase commit around the planet.

---

## 4. Talent acquisition — `recruitment-service`

**Job:** requisitions, candidates, interviews, offers.

A candidate is not an employee. That sentence is worth repeating in every design review. The moment of truth is `offer-accepted`, after which Workforce hires. Requisitions refer to Workforce positions through an anti-corruption layer — Talent copies the IDs it needs; it does not import Workforce entities.

---

## 5. Workforce communications — `notification-service`

**Job:** send the message. Do not decide HR policy.

This service maps event types to templates (mail, push, in-app) and respects channel preferences. Message bodies often contain PII, so they follow the same region rules as everyone else. If you feel tempted to put “only notify if the manager approved the raise” here, that logic belongs upstream.

---

## 6. Compliance and people analytics — not a Phase 1 process

**Job:** watch the river of events. Do not slow the operational services.

Audit logs for GDPR/CCPA, dashboards, global counts — these are projections. They may be eventually consistent. They may never reach into payroll’s live tables “just this once.”

---

## Shared language (the only things everyone may copy)

A small **shared kernel** is allowed: tenant ID, region code, employee ID, correlation ID, money. These are values, not tables. Copying a `TenantId` into a JSON event is fine. Publishing a JPA `@Entity` to another team is not.

---

## Who is upstream of whom

```text
IAM  (issues the badge)
  │
  ├── Workforce  ←── Talent (hire)
  │      │
  │      └── Compensation
  │
  └── everyone ──── Notifications
  └── everyone’s events ──── Analytics (later)
```

“Upstream” means: they publish facts others depend on. Compensation is not allowed to invent employees. Talent is not allowed to invent pay.

---

**Previous:** [Chapter 2](02-what-we-have-today.md) · **Next:** [Chapter 4 — How the system is shaped](04-how-the-system-is-shaped.md)
