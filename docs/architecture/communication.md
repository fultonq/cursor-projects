# Communication protocols

## Sync

- Browser → Gateway → service. No browser-to-service calls.
- Service-to-service REST only for request/response queries inside the same region (OpenFeign + Eureka). Prefer events for state changes.

## Async

- Domain events on Kafka. Producer uses transactional outbox (Phase 2).
- Notifications are always async.

## Frontend

- `hr-shell` is the Module Federation host (auth, layout, routing).
- `admin-portal` and `employee-self-service` are remotes.
- Shared lib `data-access` owns HTTP + NgRx/Signals stores. Apps do not call APIs directly.
