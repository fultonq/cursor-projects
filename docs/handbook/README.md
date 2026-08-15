# Global HR Platform — Handbook

**Audience:** senior developers, engineering managers, and product/operations leads  
**Reading time:** about 45–60 minutes cover to cover; 15 minutes if you read the manager path  
**Status of the software:** Phase 1 — architecture, running stubs, and clickable mock screens. Not a live HR system.

This is the document you hand to someone joining the program. It explains *what* we are building, *why* the design looks this way, *what is real today*, and *what must not be done* as we grow.

Technical maps (bounded contexts, Kafka names, API header lists) still live under `docs/ddd/` and `docs/architecture/`. This handbook is the narrative. Read this first.

---

## How to read this book

| If you are… | Read |
|-------------|------|
| A manager or product lead | [Chapter 1](01-why-this-exists.md), [2](02-what-we-have-today.md), [3](03-the-business-in-six-parts.md), [6](06-the-applications.md), [10](10-how-we-deliver.md) |
| A senior engineer joining the backend | All chapters, then `docs/ddd/bounded-contexts.md` |
| A senior engineer joining the frontend | Chapters 1–2, [4](04-how-the-system-is-shaped.md), [6](06-the-applications.md), [9](09-running-it-locally.md) |
| Security / compliance | Chapters [5](05-data-regions-and-the-law.md) and [8](08-security.md) |

Unfamiliar words are collected in the [glossary](glossary.md).

---

## Chapters

1. [Why this platform exists](01-why-this-exists.md) — the problem, the bet, and what we refuse to build  
2. [What we have today](02-what-we-have-today.md) — honest inventory of scaffold vs product  
3. [The business, in six parts](03-the-business-in-six-parts.md) — domains in plain English  
4. [How the system is shaped](04-how-the-system-is-shaped.md) — services, gateway, and the three apps  
5. [Data, regions, and the law](05-data-regions-and-the-law.md) — tenant vs region, shards, events  
6. [The applications people will use](06-the-applications.md) — screens, journeys, mock data  
7. [Backend services, one by one](07-backend-services.md) — what each process is for  
8. [Security without the whitepaper](08-security.md) — SSO, roles, and defense in depth  
9. [Running it on a laptop](09-running-it-locally.md) — Docker, Maven, IntelliJ, Nx  
10. [How we deliver from here](10-how-we-deliver.md) — Phase 2, teams, risks, decisions  

[Glossary](glossary.md)
