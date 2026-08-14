# Frontend — Nx Module Federation

| App | Role | Port |
|-----|------|------|
| `hr-shell` | Host container (layout, auth bootstrap, routing) | 4200 |
| `admin-portal` | Remote — HR admin | 4201 |
| `employee-self-service` | Remote — ESS | 4202 |

Libs: `ui` (shared components), `data-access` (HTTP + signal stores), `util`.

```bash
npm install
npx nx serve hr-shell
```

Shell loads remotes at `/admin` and `/ess`. Phase 2 implements feature modules — one lib per turn.
