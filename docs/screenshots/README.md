# Running application screenshots

Captured from the live static demo (`python3 deploy/web/serve.py`, then Chrome headless at `http://127.0.0.1:4173`). These are the **running app**, not the earlier design comps.

| Screen | File |
|--------|------|
| Command center | [home.png](home.png) |
| SSO | [login.png](login.png) |
| Admin overview | [admin.png](admin.png) |
| Employee self-service | [ess.png](ess.png) |
| Directory table (5,280 people, hot-linked names) | [directory_table.png](directory_table.png) |
| Profile modal from a table click | [directory_profile_modal.png](directory_profile_modal.png) |
| Directory photo grid | [directory_grid.png](directory_grid.png) |
| Profile modal from a grid click | [directory_grid_profile_modal.png](directory_grid_profile_modal.png) |

To recapture:

```bash
python3 deploy/web/serve.py
google-chrome --headless=new --window-size=1440,900 --screenshot=docs/screenshots/home.png http://127.0.0.1:4173/
```
