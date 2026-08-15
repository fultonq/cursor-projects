# Data strategy (Phase 1)

## PostgreSQL — shard by region

| Shard | Region | Local port | Database |
|-------|--------|------------|----------|
| `pg-amer` | `AMER` | 5432 | `hr_amer` |
| `pg-emea` | `EMEA` | 5433 | `hr_emea` |
| `pg-apac` | `APAC` | 5434 | `hr_apac` |

Every table includes `tenant_id` + `region_code`. Row-level tenant filter is mandatory; region is also the connection key.

Routing: `RegionDataSourceRouter` (Phase 2) selects the DataSource from `X-Region`. No default DS for business queries.

## Redis

Key layout: `{tenant}:{region}:{bc}:{id}`. TTL on sessions and directory projections. Never cache across regions.

## Kafka

- Cluster: single local broker for dev; production = region-local clusters + replicator for allowed event types.
- Topic: `hr.<bc>.<event>`.
- Headers: `tenantId`, `region`, `correlationId`.
- Partition key: `tenantId`.
- Outbox in each service (Phase 2) for at-least-once publish.

## Search / analytics (not in Phase 1 runtime)

- Directory search: region-local Elasticsearch (Module B).
- Org chart: adjacency list in Workforce + materialized path projection.
- Compliance audit: append-only store fed from the event log (Module D).
