# Glossary

Words we use on purpose. If a pull request invents a synonym, prefer this list.

| Term | Plain meaning |
|------|----------------|
| **Aggregate** | A cluster of data we treat as one thing for rules (e.g. an Employee, a PayrollRun). |
| **Anti-corruption layer (ACL)** | A small translator so team B does not import team A’s objects. |
| **Bounded context** | A part of the business with its own language and database (IAM, Workforce, …). |
| **Claim** | A fact inside a login token, such as region = EMEA. |
| **CloudEvents** | A standard JSON envelope for Kafka payloads. |
| **Compensation** | The payroll and benefits domain (`payroll-service`). |
| **Config Server** | Process that hands YAML to the others (:8888). |
| **Correlation ID** | A unique string that follows a request across services for support. |
| **Cursor pagination** | “Give me the next slice after this token,” not “page 400.” |
| **Defense in depth** | Gateway *and* each service check identity. |
| **DSAR** | Data Subject Access Request — a person asking what we hold on them. |
| **EmployeeId** | Opaque workforce identifier, issued only by Workforce. |
| **Eureka** | Phone book of running services (:8761). |
| **Gateway** | The HTTP front door (:8080). Browsers should not skip it. |
| **IAM** | Identity and access management (`auth-service`). |
| **IdP** | Identity provider (Okta, Entra). They own the password. |
| **Isolation key** | `(tenantId, regionCode)` on every business record. |
| **Kafka** | The log we use to say “this happened.” |
| **Module Federation** | Webpack feature: shell loads admin and ESS as plugins. |
| **Nx** | The tool that manages the Angular monorepo. |
| **OIDC** | Modern SSO protocol (tokens). Primary path. |
| **Outbox** | Table in the same transaction as business data; a publisher reads it so events are not lost. |
| **Payee** | Compensation’s internal view of someone we pay — not the Workforce entity. |
| **Principal** | A login identity. Not automatically an employee. |
| **Published language** | The JSON we are willing to show other teams. |
| **Region** | AMER, EMEA, or APAC — where data lives. |
| **Remote** | An Angular app loaded by the shell. |
| **Residency** | Legal requirement that data stay in a geography. |
| **Resource server** | An API that accepts JWTs rather than logging you in itself. |
| **SAML** | Older SSO protocol. Enterprise backup. |
| **Shard** | One physical database for one region. |
| **Shared kernel** | Tiny types everyone may copy (IDs, money). |
| **Shell** | `hr-shell` — chrome, login, top-level routes. |
| **Spring Batch** | The planned engine for monthly payroll runs. |
| **Stub** | A service that boots and pings but has no domain logic. |
| **Talent** | Recruitment domain (`recruitment-service`). |
| **Tenant** | A legal employer / brand on this software. |
| **Virtual scroll** | UI technique: only render the rows on screen, even if there are 25k. |
| **Workforce** | Employee master domain (`employee-service`). |

---

[Back to the handbook](README.md)
