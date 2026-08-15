# Chapter 6 — The applications people will use

**In one sentence:** three Angular apps share a look; the shell is the campus gate; admin is for people who run HR; self-service is for everyone else.

All screens below are **mocks** (static data). They are still the UX contract. If a later API cannot support a screen, we change the screen on purpose — we do not silently fetch 25,000 rows.

Full-size comps: [`docs/mockups/`](../mockups/README.md).

---

## The two people in the mocks

| Person | Role | App they live in |
|--------|------|------------------|
| **Priya Nair** | People Partner, London, EMEA | Shell + Admin Portal |
| **Marcus Holm** | Staff Engineer, Stockholm, EMEA | Shell + Employee Self-Service |

Tenant: **Aether Dynamics** (`AETHER-GLOBAL`). Region switcher shows **EMEA**. Headcount **25,412** is illustrative.

---

## HR Shell — the campus gate

Routes: `/login`, `/`  
App: `frontend/apps/hr-shell` · port 4200

**Sign in.** Company SSO, not a password form we store. Email and tenant ID are shown so IT can recognize the broker pattern (OIDC first, SAML backup). Continue lands on the command center in the mock (a real IdP redirect comes in Module A).

![SSO](../mockups/hr-shell-sso.png)

**Command center.** Good morning, KPIs, and two doors: Workforce operations (admin) and Employee workspace (self-service). Regional pulse is AMER / EMEA / APAC counts — in production those numbers come from analytics, not from joining shards in the request.

![Home](../mockups/hr-shell-home.png)

The top bar (search, tenant chip, region chip, avatar) stays as you move into remotes. That is the point of the shell.

---

## Admin Portal — run the workforce

Base route: `/admin` (inside the shell)  
App: `frontend/apps/admin-portal`

Sidebar: Overview, Directory, Org chart, Recruitment, Payroll, Access.

**Overview.** Same 25k-scale KPIs plus “attention required”: payroll cutoff, stale tax table, SAML cert expiry, DSAR queue. This is an operations cockpit, not a vanity dashboard.

![Dashboard](../mockups/admin-dashboard.png)

**Directory.** Search and filters (region, location, org, status). The copy says **virtualized** and **cursor page (no offset)** because a 25k-row table with `OFFSET` will melt. Export and Add employee are placeholders until Workforce APIs exist.

![Directory](../mockups/admin-directory.png)

**Org chart.** A tree, not a spreadsheet. Cards show name, title, location, team size. The handbook rule still applies: this forest is EMEA; an AMER manager would appear as a reference, not a SQL parent.

![Org](../mockups/admin-org-chart.png)

**Recruitment.** Kanban: Sourcing → Screen → Interview → Offer → Hired. Candidates carry requisition IDs. Hired is a stage in Talent; it is not the Workforce employee record.

![Recruitment](../mockups/admin-recruitment.png)

**Payroll.** Region runs as separate cards (AMER in progress, EMEA queued, APAC validating). Pay groups by jurisdiction and currency. A step list stands in for Spring Batch. The subtitle is the policy: *no cross-region posting*.

![Payroll](../mockups/admin-payroll.png)

**Identity & access.** Okta connected, Entra as SAML backup, 54 roles, 25k principals. The table is the RBAC story: People Partner vs Payroll Ops Lead vs Recruiter vs Engineering Manager vs Compliance Officer. Compliance “multi-read” means analytics projections, not raw shards.

![IAM](../mockups/admin-iam.png)

---

## Employee Self-Service — my HR

Base route: `/ess`  
App: `frontend/apps/employee-self-service`

**Workspace.** Snapshot: time-off balance, next payday, goals, last net pay. Quick actions go to time off, payslip, profile.

![Workspace](../mockups/ess-workspace.png)

**Profile.** Employment facts are read-only (Workforce owns them). Personal fields can request a correction — we do not let every employee overwrite master data without a process.

**Time off.** Calendar, balances, a draft request, history. Approver is the manager from Workforce.

![Time off](../mockups/ess-time-off.png)

**Payslip.** Document-style breakdown, period list, download. Footer states the data is stored in the EMEA shard. That sentence is a product requirement, not decoration.

![Payslip](../mockups/ess-payslip.png)

---

## What “done” looks like for these screens later

| Screen | Becomes done when… |
|--------|-------------------|
| Login | Real OIDC redirect, tenant resolved, region claim on the token |
| Directory | Cursor API + virtual scroll against EMEA (or chosen) shard |
| Org | Live tree from Workforce projections |
| Recruitment | Pipeline persisted in recruitment-service |
| Payroll | Batch jobs write run state; UI tails it |
| IAM | Roles and IdP bindings persist; JWT required on APIs |
| ESS payslip | PDF generated in-region; download authorized as self or payroll ops |

Until then, treat pixels as the spec.

---

**Previous:** [Chapter 5](05-data-regions-and-the-law.md) · **Next:** [Chapter 7 — Backend services, one by one](07-backend-services.md)
