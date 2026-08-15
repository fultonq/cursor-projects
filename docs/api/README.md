# API conventions

Read this file on demand. Do not inline specs into chat.

## HTTP

- Public ingress: Spring Cloud Gateway `:8080`.
- Service ports: auth `8081`, employee `8082`, payroll `8083`, recruitment `8084`, notification `8085`.
- Base path: `/api/v1/<bc>/...`
- Headers (required on business APIs): `Authorization: Bearer`, `X-Tenant-Id`, `X-Region`, `X-Correlation-Id`.
- Errors: RFC 7807 `application/problem+json`.
- Pagination: cursor (`?cursor=&limit=`) for directory-scale lists; never offset for 25k+ collections.

## Kafka

Topic pattern `hr.<bc>.<event>`. Payload = CloudEvents JSON, data = published language DTO (not JPA).

## OpenAPI

Per-service `src/main/resources/openapi.yaml` is added when that service is implemented (Phase 2). Until then this file is the contract baseline.
