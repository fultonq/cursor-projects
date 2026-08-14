from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def test_canonical_and_namespaced_imports():
    from nycflights_ds.compat import install_nycflights_alias

    install_nycflights_alias()
    from nycflights.nycflights_ds import prepare_dataset
    from nycflights.nycflights_ds.config import BUNDLE_PATH, YEAR
    from nycflights_ds import prepare_dataset as canonical

    assert YEAR == 2013
    assert callable(prepare_dataset)
    assert callable(canonical)
    assert BUNDLE_PATH.name == "delay_bundle.joblib"


def test_namespaced_import_without_compat_helper():
    """Matches Streamlit's rewritten import: from nycflights.nycflights_ds import ..."""
    from nycflights.nycflights_ds import prepare_dataset
    from nycflights.nycflights_ds.config import YEAR

    assert YEAR == 2013
    assert callable(prepare_dataset)
