"""Shim so ``from nycflights.nycflights_ds import ...`` works from this project dir."""

from __future__ import annotations

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from nycflights_ds.compat import install_nycflights_alias

install_nycflights_alias()
