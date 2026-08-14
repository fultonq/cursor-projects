"""Ensure `import nycflights_ds` works no matter where Streamlit is launched from.

Editors sometimes rewrite imports to ``nycflights.nycflights_ds`` because the
project directory is named ``nycflights``. The installable package is
``nycflights_ds`` (this folder). We put that folder on ``sys.path`` and, if
needed, alias the namespaced import.
"""

from __future__ import annotations

import sys
from pathlib import Path


def ensure_nycflights_ds_on_path() -> Path:
    project_root = Path(__file__).resolve().parents[1]
    repo_root = project_root.parent
    for candidate in (str(project_root), str(repo_root)):
        if candidate not in sys.path:
            sys.path.insert(0, candidate)

    try:
        import nycflights_ds  # noqa: F401
        return project_root
    except ModuleNotFoundError:
        pass

    try:
        import nycflights.nycflights_ds as _pkg  # type: ignore[no-redef]
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            "Cannot import nycflights_ds. From the nycflights/ directory run "
            "`pip install -e .` or `PYTHONPATH=. streamlit run app/streamlit_app.py`."
        ) from exc
    sys.modules.setdefault("nycflights_ds", _pkg)
    return project_root
