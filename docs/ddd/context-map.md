# Context Map

```
                    ┌─────────────┐
                    │  IAM        │  upstream / OIDC+SAML
                    │  auth-svc   │
                    └──────┬──────┘
           JWT + tenant/region claims
                           │
         ┌─────────────────┼──────────────────┐
         ▼                 ▼                  ▼
 ┌───────────────┐  ┌──────────────┐   ┌─────────────┐
 │ Workforce     │  │ Talent Acq.  │   │ Notify      │
 │ employee-svc  │◄─│ recruit-svc  │──►│ notify-svc  │
 └───────┬───────┘  └──────────────┘   └──────▲──────┘
         │ hire / org events                  │
         ▼                                    │
 ┌───────────────┐                            │
 │ Compensation  │────────────────────────────┘
 │ payroll-svc   │
 └───────┬───────┘
         │ domain events (all BCs)
         ▼
 ┌───────────────┐
 │ Compliance &  │  Phase 2 — audit + dashboards
 │ Analytics     │
 └───────────────┘
```

## Relationships

| Upstream | Downstream | Pattern |
|----------|------------|---------|
| IAM | * | Conformist (JWT published language) |
| Workforce | Compensation | Customer/Supplier (employee + assignment events) |
| Talent | Workforce | Customer/Supplier (`offer-accepted` → hire) |
| * | Notify | Published Language (template keys) |
| * | Analytics | Open-host (event log; ACL in analytics) |

## Anti-corruption layers

- `payroll-service` maps `hr.workforce.employee-*` → internal `Payee`.
- `recruitment-service` maps Workforce `PositionId` / `OrgUnitId` → `Requisition` refs.
- `notification-service` maps event type → template code; never imports other domains.

## Trust boundaries

Gateway (`:8080`) terminates TLS, rate-limits, and routes. Each service still:

1. Validates JWT (issuer, audience, tenant).
2. Rejects missing/mismatched `X-Tenant-Id` / `X-Region`.
3. Routes persistence through the region shard (see `docs/architecture/data-strategy.md`).
