# Chapter 8 — Security without the whitepaper

**In one sentence:** the company signs people in; we check the badge on every door; tenant and region are part of the badge, not an afterthought.

---

## Who owns passwords? Not us.

Employees already have a corporate identity. The platform **brokers**:

- **OIDC** (primary) — e.g. Okta
- **SAML 2.0** (backup) — e.g. Entra ID

`auth-service` will be the OAuth2 resource-server helper and the place we store **IdP bindings per tenant**, roles, and sessions. It will not store a parallel password file.

The login mock is that contract in pixels. Module A turns it on.

---

## Three facts on every business request

1. **Authorization: Bearer &lt;JWT&gt;** — signature, issuer, audience, expiry.
2. **X-Tenant-Id** — must match the tenant in the token. A caller cannot “pick another company.”
3. **X-Region** — must match a supported region and the session’s claim. A caller cannot “pick AMER because the report needs it.”

`X-Correlation-Id` is for support and tracing. If the browser omits it, the filter mints one.

The Angular `ApiClient` already attaches the three isolation headers. When JWT is on, it will attach the bearer token too. Apps still must not talk past the gateway.

---

## Defense in depth

The gateway will terminate TLS, apply rate limits, and route. That is necessary and **insufficient**.

Each service:

- validates the JWT when `hr.security.jwt.enabled=true`,
- checks tenant/region,
- opens the **matching** database, not “whichever DataSource is primary.”

If someone misconfigures the gateway to forward a request without a token, the service must still reject it. “The mesh will handle it” is how HR platforms leak.

---

## Roles: fifty is a feature, not a smell

HR organizations do not live on Admin vs User. The mocks show a slice:

- People Partner — directory read/write assignments
- Payroll Ops Lead — run payroll, read payslips
- Recruiter — requisitions and draft offers
- Engineering Manager — directory read, offer approve
- Compliance Officer — audit read, DSAR export (from projections)

Permission sets are data, not Java enums that need a release to add “Benefits Analyst.” Role assignment is tenant-scoped. A People Partner in tenant Aether is powerless in tenant OtherCo.

Region still sits *beside* the role. A Payroll Ops Lead with an EMEA claim cannot execute the AMER run.

---

## What is open on a developer laptop (and must close)

| Setting | Local Phase 1 | Shared / prod |
|---------|---------------|----------------|
| `hr.security.jwt.enabled` | `false` | `true` |
| OIDC issuer | unset | real issuer URI |
| Actuator | health, info, prometheus | lock down or network-restrict |
| `_ping` | public | public or mesh-only |

Never commit IdP client secrets. `.env.example` lists names only.

---

## Sessions and revocation

When IAM is real, `hr.iam.session-revoked` is how we tell everyone a badge is dead (laptop lost, leaver). Gateways and services should not wait for JWT expiry if a revocation list or introspection says no. Until that exists, do not build a custom session table in payroll “just in case.”

---

## Practical review questions

- Does this endpoint work with only a gateway check? If yes, fail the review.
- Can a token for EMEA read AMER by changing a header? If yes, fail the review.
- Did we log a payslip body? If yes, fail the review.
- Is a new role a code change? Prefer configuration.

---

**Previous:** [Chapter 7](07-backend-services.md) · **Next:** [Chapter 9 — Running it on a laptop](09-running-it-locally.md)
