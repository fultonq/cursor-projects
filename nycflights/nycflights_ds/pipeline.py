"""Load → clean → engineer in one call."""

from .clean import clean
from .features import engineer
from .load import load_tables


def prepare_dataset(source: str = "raw"):
    """Load → join/clean/impute → engineer features. Returns a modeling-ready frame."""
    tables = load_tables(source)
    return engineer(clean(tables))
