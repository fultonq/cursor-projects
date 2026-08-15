# Chapter 9 — Running it on a laptop

**In one sentence:** Docker for data, Maven for Java, Nx for Angular, IntelliJ if you want all the services at once.

Assumed workstation: a recent Mac (the original brief was M4 Max) or Linux, JDK 21, Node 20+, Docker. IntelliJ IDEA 2026+ is optional but configured.

---

## 1. Data plane

From the repo root:

```bash
docker compose -f infra/docker-compose.yml up -d
```

You now have Postgres on 5432/5433/5434, Redis 6379, Kafka 9092. Default user/password are in Compose and `.env.example` (`hr` / `hr`). That is fine for local and **forbidden** for anything on a network.

Stop with `docker compose -f infra/docker-compose.yml down`. Add `-v` only if you intend to wipe volumes.

---

## 2. Backend

```bash
cd backend
./mvnw test          # compile + unit/context tests
```

Start order if you do it by hand:

1. config-server  
2. service-registry  
3. api-gateway  
4. any domain services you need  

```bash
./mvnw -pl infrastructure/config-server spring-boot:run
```

Repeat `-pl` for the others, each in its own terminal, or use IntelliJ.

**IntelliJ:** open the repository (or import `backend/pom.xml`). Shared run configs live in `.idea/runConfigurations/`:

- **Platform — Infra** — config, Eureka, gateway  
- **Platform — All Services** — infra plus all five domain stubs  

Code style (Java 4-space, TypeScript 2-space, 140-character Java margin) is in `.idea/codeStyles/` and `.editorconfig`.

---

## 3. Frontend

```bash
cd frontend
npm install
npx nx serve hr-shell
```

Shell: http://localhost:4200  

Useful routes once the mock pages are loaded:

| URL | Screen |
|-----|--------|
| `/login` | SSO |
| `/` | Command center |
| `/admin` | Admin overview |
| `/admin/directory` | Directory |
| `/admin/org` | Org chart |
| `/admin/recruitment` | Pipeline |
| `/admin/payroll` | Payroll runs |
| `/admin/access` | IAM |
| `/ess` | Employee workspace |
| `/ess/profile` | Profile |
| `/ess/time-off` | Time off |
| `/ess/payslips` | Payslip |

Remotes can be served alone:

```bash
npx nx serve admin-portal            # :4201
npx nx serve employee-self-service   # :4202
```

The shell’s Module Federation dev server is what you want for “feels like production navigation.”

---

## Port map (print this)

| What | Port |
|------|------|
| Config Server | 8888 |
| Eureka | 8761 |
| Gateway | 8080 |
| auth / employee / payroll / recruitment / notification | 8081–8085 |
| hr-shell | 4200 |
| admin-portal | 4201 |
| employee-self-service | 4202 |
| Postgres AMER / EMEA / APAC | 5432 / 5433 / 5434 |
| Redis | 6379 |
| Kafka | 9092 |

---

## What green looks like

- `./mvnw test` exits 0. You will see five Spring Boot test banners; that is the context-load tests.
- Eureka dashboard at http://localhost:8761 shows registered apps when they are running.
- `curl -s http://localhost:8081/api/v1/auth/_ping` → `{"service":"auth-service","status":"up"}` (direct). Through the gateway: `http://localhost:8080/api/v1/auth/_ping` once both are up.
- Shell loads; `/admin` and `/ess` show the mock sidebars.

If a service hangs on startup, it is often waiting on Eureka or a JWT issuer. Phase 1 config disables JWT; tests disable Eureka. A mis-copied `issuer-uri` pointing at a dead Keycloak will block a real boot — that is why we did not put a fake issuer in shared config.

---

## What not to do locally

- Point the Angular app at `:8082` “to skip the gateway.”
- Run a single Postgres and “add a region column later.”
- Commit `application-local.yml` or `.env` with secrets.
- Check in `target/`, `node_modules/`, or `dist/` (see `.gitignore` / `.claudeignore`).

---

**Previous:** [Chapter 8](08-security.md) · **Next:** [Chapter 10 — How we deliver from here](10-how-we-deliver.md)
