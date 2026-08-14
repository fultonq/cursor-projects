"""Paths, dataset URLs, and modeling constants for NYC Flights 2013."""

from __future__ import annotations

from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
ROOT = PACKAGE_DIR.parent

DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
DATA_SAMPLE = ROOT / "data" / "sample"
MODELS_DIR = ROOT / "models"
FIGURES_DIR = ROOT / "reports" / "figures"
METRICS_PATH = MODELS_DIR / "metrics.json"
BUNDLE_PATH = MODELS_DIR / "delay_bundle.joblib"

TABLES = ("flights", "airlines", "airports", "planes", "weather")
RDATASETS_BASE = "https://vincentarelbundock.github.io/Rdatasets/csv/nycflights13"

# FAA on-time threshold: a flight is delayed if it departs/arrives 15+ minutes late.
DELAY_THRESHOLD_MIN = 15
RANDOM_STATE = 42
YEAR = 2013

# Time-based holdout: train on Jan–Oct, evaluate on Nov–Dec (no future leakage).
TRAIN_MONTHS = tuple(range(1, 11))
TEST_MONTHS = (11, 12)

LOW_CARD_CATEGORICALS = ("origin", "carrier", "engine_type", "season", "part_of_day")
HIGH_CARD_CATEGORICALS = ("dest",)
NUMERIC_FEATURES = (
    "month",
    "day",
    "hour",
    "minute",
    "distance",
    "weekday",
    "is_weekend",
    "hour_sin",
    "hour_cos",
    "month_sin",
    "month_cos",
    "plane_age",
    "seats",
    "engines",
    "temp",
    "dewp",
    "humid",
    "wind_speed",
    "precip",
    "pressure",
    "visib",
    "orig_alt",
    "dest_alt",
    "precip_missing",
    "pressure_missing",
    "plane_age_missing",
    "weather_missing",
)
DEP_DELAY_FEATURES = NUMERIC_FEATURES + LOW_CARD_CATEGORICALS + HIGH_CARD_CATEGORICALS
ARR_DELAY_EXTRA = ("dep_delay",)
