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
| Page 1 · 100 per page | [directory_page1_pager.png](directory_page1_pager.png) |
| Page 2 (101–200) | [directory_page2.png](directory_page2.png) |
| Search Smith | [directory_search_smith.png](directory_search_smith.png) |
| Reset filters | [directory_reset.png](directory_reset.png) |
| Ava Watkson profile | [directory_watkson_modal.png](directory_watkson_modal.png) |
| Grid · 100 per page | [directory_grid_100.png](directory_grid_100.png) |
| Priya profile with department, salary, credentials, social | [directory_priya_profile_fields.png](directory_priya_profile_fields.png) |
| Ava profile extra fields | [directory_watkson_profile_fields.png](directory_watkson_profile_fields.png) |
| Diego Cruze MXN salary | [directory_cruze_profile_fields.png](directory_cruze_profile_fields.png) |
| Time-off Vacation balance | [ess_time_off_vacation_balance.png](ess_time_off_vacation_balance.png) |
| Time-off Jury Duty | [ess_time_off_jury_duty.png](ess_time_off_jury_duty.png) |
| Remote work (no leave deduction) | [ess_time_off_remote.png](ess_time_off_remote.png) |
| Time-off submitted | [ess_time_off_submitted.png](ess_time_off_submitted.png) |

To recapture:

```bash
python3 deploy/web/serve.py
google-chrome --headless=new --window-size=1440,900 --screenshot=docs/screenshots/home.png http://127.0.0.1:4173/
```
