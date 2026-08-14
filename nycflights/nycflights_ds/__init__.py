"""NYC Flights 2013 analysis package: pandas cleaning, EDA, and sklearn delay models."""

from nycflights_ds.clean import clean
from nycflights_ds.features import engineer
from nycflights_ds.load import load_tables, profile

__all__ = ["clean", "engineer", "load_tables", "prepare_dataset", "profile"]


def prepare_dataset(source: str = "raw"):
    """Load → join/clean/impute → engineer features. Returns a modeling-ready frame."""
    tables = load_tables(source)
    return engineer(clean(tables))
