"""Ensure `import nycflights_ds` and `import nycflights.nycflights_ds` both work."""

from __future__ import annotations

import sys
from pathlib import Path

from nycflights_ds.compat import install_nycflights_alias


def ensure_nycflights_ds_on_path() -> Path:
    project_root = Path(__file__).resolve().parents[1]
    repo_root = project_root.parent
    for candidate in (str(project_root), str(repo_root)):
        if candidate not in sys.path:
            sys.path.insert(0, candidate)
    install_nycflights_alias()
    import nycflights_ds  # noqa: F401

    return project_root
