# Backend — Global HR Platform

Multi-module Maven reactor. Domain services are **stubs** (health + `/_ping` only).

```
backend/
  libs/common            shared kernel (TenantId, RegionCode, isolation filter)
  libs/security          OAuth2 resource-server auto-config (OIDC JWT)
  infrastructure/        config-server :8888, eureka :8761, gateway :8080
  services/              auth :8081, employee :8082, payroll :8083,
                         recruitment :8084, notification :8085
```

```bash
./mvnw -q verify
./mvnw -pl infrastructure/config-server spring-boot:run
```

IntelliJ: import `backend/pom.xml`, then run **Platform — All Services**.
