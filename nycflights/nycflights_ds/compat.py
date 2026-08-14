"""Map ``nycflights.nycflights_ds`` to the real ``nycflights_ds`` package.

Streamlit / IDE rewrites often turn ``nycflights_ds`` into
``nycflights.nycflights_ds`` because the project folder is named nycflights.
"""

from __future__ import annotations

import importlib
import importlib.abc
import importlib.machinery
import importlib.util
import sys

_ALIAS_PREFIX = "nycflights.nycflights_ds"
_REAL_PREFIX = "nycflights_ds"


class _AliasLoader(importlib.abc.Loader):
    def __init__(self, real_name: str) -> None:
        self.real_name = real_name

    def create_module(self, spec):  # noqa: ANN001
        return importlib.import_module(self.real_name)

    def exec_module(self, module) -> None:  # noqa: ANN001
        return None


class _AliasFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path, target=None):  # noqa: ANN001
        if fullname != _ALIAS_PREFIX and not fullname.startswith(_ALIAS_PREFIX + "."):
            return None
        real_name = _REAL_PREFIX + fullname[len(_ALIAS_PREFIX) :]
        real_spec = importlib.util.find_spec(real_name)
        if real_spec is None:
            return None
        locations = list(real_spec.submodule_search_locations or [])
        spec = importlib.machinery.ModuleSpec(
            fullname,
            _AliasLoader(real_name),
            origin=real_spec.origin,
            is_package=bool(locations),
        )
        spec.submodule_search_locations = locations
        return spec


def install_nycflights_alias() -> None:
    if not any(isinstance(finder, _AliasFinder) for finder in sys.meta_path):
        sys.meta_path.insert(0, _AliasFinder())
