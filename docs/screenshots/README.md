# Running application screenshots

Captured from the live static demo (`python3 deploy/web/serve.py`, then Chrome headless at `http://127.0.0.1:4173`). These are the **running app**, not the earlier design comps.

| Screen | File |
|--------|------|
| Command center | [home.png](home.png) |
| SSO | [login.png](login.png) |
| Admin overview | [admin.png](admin.png) |
| Employee self-service | [ess.png](ess.png) |
| Directory (5,280 people) | [directory.png](directory.png) |
| Profile modal | [directory-profile.png](directory-profile.png) |

To recapture:

```bash
python3 deploy/web/serve.py
google-chrome --headless=new --window-size=1440,900 --screenshot=docs/screenshots/home.png http://127.0.0.1:4173/
```
