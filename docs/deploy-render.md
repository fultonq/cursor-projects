# Deploy to Render

The live demo is a **static site** of the Aether HR mock screens (login, admin, self-service). It does not start the eight Java processes, Eureka, Kafka, or regional Postgres — those stay local (`infra/docker-compose.yml`).

## One-click (your Render account)

1. Open **[New Blueprint](https://dashboard.render.com/blueprint/new)**.
2. Connect the GitHub repo `fultonq/cursor-projects`.
3. Set:
   - **Blueprint path:** `render.yaml`
   - **Branch:** `cursor/hr-platform-render-be44` (or `main` after this PR merges)
4. Click **Deploy Blueprint**.

Render will create a static site named `aether-hr` and give it a URL like `https://aether-hr.onrender.com`.

## Screenshots of the running demo

See [`docs/screenshots/`](screenshots/README.md) — command center, SSO, admin, and self-service, taken from the live local server.

## What gets deployed

| Resource | Type | Source |
|----------|------|--------|
| `aether-hr` | Static site (free) | `deploy/web/` |

SPA routes (`/admin`, `/ess`, …) rewrite to `index.html`.

## After merge to main

Edit `render.yaml` and drop the `branch:` override (or set `branch: main`) so production tracks the default branch.

## Why not all microservices?

A full mesh on Render would be eight Java web services plus Postgres, Redis, and Kafka. That is paid, slow to boot, and Eureka does not fit Render’s DNS. Use this site for the product walkthrough; run Java locally for service work.
