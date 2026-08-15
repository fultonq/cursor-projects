# Chapter 1 — Why this platform exists

**In one sentence:** we need one HR platform that can serve a global company of 25,000+ people *at the same time*, without mixing one country’s employee data into another country’s database.

---

## The problem we are actually solving

A company of this size does not have “an HR app.” It has several overlapping jobs that all look like HR from a distance:

- Prove who someone is, and what they are allowed to do (identity and access).
- Keep a trustworthy list of who works here, where, and for whom (the employee directory and org chart).
- Hire people without confusing *candidates* with *employees* (recruitment).
- Pay people correctly under many tax systems and currencies (payroll and benefits).
- Tell people that something happened — a payslip is ready, an interview is booked (notifications).
- Show that we handled personal data lawfully (audit, GDPR, CCPA).

If we put all of that in one database and one codebase, two things go wrong fast.

First, **change becomes dangerous**. A payroll tax fix in Singapore should not require a freeze of the London org-chart team. At 25,000 concurrent users, a bad deploy in one area takes everyone down.

Second, **the law gets in the way of the schema**. European employee records cannot casually sit next to American ones “because the report was easier.” Residency is not a filter you apply later. It is a place data *lives*.

This platform is the bet that we can keep one product family — one login, one look, one set of employee IDs — while keeping the *systems of record* separate enough to scale, to ship independently, and to stay on the right side of privacy rules.

---

## Who it is for

| Audience | What they need from the platform |
|----------|----------------------------------|
| Employees | Self-service: profile, time off, payslips, benefits |
| People partners / HR ops | Directory, org, cases, hiring support |
| Recruiters and hiring managers | Requisitions, pipeline, offers |
| Payroll operations | Calendars, runs, tax jurisdictions, payslips |
| Security / IAM | SSO, roles (50+ job roles), session control |
| Compliance / legal | Audit trail, residency guarantees, DSAR-ready logs |
| Engineering | Clear service boundaries so teams can ship without stepping on each other |

The mock screens use a fictional tenant called **Aether Dynamics** so the UI has a face. The architecture is meant for a real global employer.

---

## Design goals (the ones that actually constrain us)

1. **25,000+ people using the system at once**, not 25,000 rows in a spreadsheet. Lists, search, and payroll batches must be designed for that size from day one (cursor pagination, virtual scrolling, region-local search later).
2. **More than one region at the same time.** We model three: AMER, EMEA, APAC. Each region is a shard of PostgreSQL. Production will look like that, only with real operations around it.
3. **More than one legal employer (tenant)** on the same software. A tenant is a company/brand partition. A region is *not* a tenant. Mixing those two ideas is the most expensive mistake this program can make.
4. **Company SSO**, not a homegrown password database. Okta/Entra (OIDC) is the primary path; SAML is the enterprise backup.
5. **Independent delivery.** Payroll can batch overnight without blocking the directory team from shipping a search fix.

---

## What we refuse to build

These are not taste preferences. They are load-bearing “no”s:

- **We will not share one `Employee` database table across payroll, recruitment, and the directory.** Other domains may *refer* to an employee ID. They may not own the employee record.
- **We will not join EMEA and AMER in SQL to make a global headcount report.** Global numbers come from events and an analytics read model (Phase 2), not from stretching a transaction across oceans.
- **We will not run one giant payroll saga that locks every region.** Each region’s monthly run is its own batch. If APAC fails, EMEA can still complete.
- **We will not put authorization only at the front door.** The API gateway routes traffic. Every service still checks the token, the tenant, and the region.
- **We will not treat a candidate as an employee.** A person becomes an employee when an offer is accepted and Workforce says so.

If a design review proposes any of the above “just for the MVP,” the answer is still no. An MVP that trains the organization on the wrong data model costs more than a slower, correct scaffold.

---

## The shape of the bet

Think of this as **one campus, several buildings**, not one warehouse.

- The **campus** is the Global HR Platform: shared login, shared visual language, shared IDs (`TenantId`, `RegionCode`, `EmployeeId`).
- The **buildings** are bounded contexts: Identity, Workforce, Compensation, Talent, Communications, and later Compliance/Analytics.
- **Walkways** between buildings are HTTP for questions and Kafka events for “something happened.” Nobody tunnels into another building’s filing cabinets.

Chapter 3 explains those buildings in business language. Chapter 4 explains the wiring.

---

**Next:** [Chapter 2 — What we have today](02-what-we-have-today.md)
