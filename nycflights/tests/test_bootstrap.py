from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(APP))

from bootstrap import ensure_nycflights_ds_on_path  # noqa: E402


def test_bootstrap_imports_nycflights_ds():
    ensure_nycflights_ds_on_path()
    import nycflights_ds
    from nycflights_ds import prepare_dataset
    from nycflights_ds.config import BUNDLE_PATH, YEAR

    assert YEAR == 2013
    assert callable(prepare_dataset)
    assert nycflights_ds.__file__
    assert BUNDLE_PATH.name == "delay_bundle.joblib"


def test_namespaced_import_alias_after_bootstrap():
    """Editors sometimes rewrite imports to nycflights.nycflights_ds."""
    ensure_nycflights_ds_on_path()
    from nycflights.nycflights_ds import prepare_dataset as namespaced
    from nycflights_ds import prepare_dataset as canonical

    assert callable(namespaced)
    assert callable(canonical)
