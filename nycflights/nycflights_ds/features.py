"""Feature engineering with vectorized pandas / numpy (no row-wise apply)."""

from __future__ import annotations

import numpy as np
import pandas as pd

from .clean import hhmm_to_minutes
from .config import ARR_DELAY_EXTRA, DEP_DELAY_FEATURES


def _cyclical(values: np.ndarray, period: float) -> tuple[np.ndarray, np.ndarray]:
    radians = 2.0 * np.pi * values / period
    return np.sin(radians), np.cos(radians)


def add_calendar_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    date = pd.to_datetime(
        dict(year=2013, month=out["month"].astype(int), day=out["day"].astype(int)),
        errors="coerce",
    )
    out["weekday"] = date.dt.weekday.astype("int8")  # Monday=0
    out["is_weekend"] = (out["weekday"] >= 5).astype(np.int8)
    month = out["month"].to_numpy(dtype=float)
    out["season"] = np.select(
        [np.isin(month, [12, 1, 2]), np.isin(month, [3, 4, 5]), np.isin(month, [6, 7, 8])],
        ["winter", "spring", "summer"],
        default="fall",
    )
    hour_sin, hour_cos = _cyclical(out["hour"].to_numpy(dtype=float), 24.0)
    month_sin, month_cos = _cyclical(out["month"].to_numpy(dtype=float), 12.0)
    out["hour_sin"] = hour_sin
    out["hour_cos"] = hour_cos
    out["month_sin"] = month_sin
    out["month_cos"] = month_cos
    return out


def add_schedule_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    hour = out["hour"].to_numpy(dtype=float)
    out["part_of_day"] = np.select(
        [hour < 6, hour < 12, hour < 18],
        ["night", "morning", "afternoon"],
        default="evening",
    )
    if "dep_time" in out.columns:
        out["dep_minutes"] = hhmm_to_minutes(out["dep_time"])
    if "arr_time" in out.columns:
        out["arr_minutes"] = hhmm_to_minutes(out["arr_time"])
    out["sched_dep_minutes"] = out["hour"].astype(float) * 60 + out["minute"].astype(float)
    return out


def add_delay_labels(df: pd.DataFrame, threshold: int = 15) -> pd.DataFrame:
    out = df.copy()
    if "dep_delay" in out.columns:
        out["dep_delayed"] = (out["dep_delay"] >= threshold).astype("float")
        out.loc[out["cancelled"], "dep_delayed"] = np.nan
    if "arr_delay" in out.columns:
        out["arr_delayed"] = (out["arr_delay"] >= threshold).astype("float")
        out.loc[out["cancelled"] | out["diverted"], "arr_delayed"] = np.nan
    return out


def add_route_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["route"] = out["origin"].astype(str) + "-" + out["dest"].astype(str)
    if {"orig_lat", "orig_lon", "dest_lat", "dest_lon"}.issubset(out.columns):
        # Haversine in miles — sanity-check against the provided `distance`.
        lat1 = np.radians(out["orig_lat"].to_numpy(dtype=float))
        lon1 = np.radians(out["orig_lon"].to_numpy(dtype=float))
        lat2 = np.radians(out["dest_lat"].to_numpy(dtype=float))
        lon2 = np.radians(out["dest_lon"].to_numpy(dtype=float))
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
        out["haversine_miles"] = 3958.8 * 2 * np.arcsin(np.sqrt(np.clip(a, 0, 1)))
    return out


def engineer(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.pipe(add_calendar_features)
        .pipe(add_schedule_features)
        .pipe(add_delay_labels)
        .pipe(add_route_features)
    )


def modeling_frame(
    df: pd.DataFrame,
    *,
    target: str,
    extra_features: tuple[str, ...] = (),
) -> tuple[pd.DataFrame, pd.Series]:
    """Return X, y with leakage-safe columns only. Drops cancelled/diverted rows."""
    work = df.copy()
    if target in {"dep_delay", "dep_delayed"}:
        work = work.loc[work["operated"] & work[target].notna()]
        feature_names = list(DEP_DELAY_FEATURES) + list(extra_features)
    elif target in {"arr_delay", "arr_delayed"}:
        work = work.loc[work["operated"] & ~work["diverted"] & work[target].notna()]
        feature_names = list(DEP_DELAY_FEATURES) + list(ARR_DELAY_EXTRA) + list(extra_features)
    else:
        raise ValueError(f"Unknown target: {target}")

    cols = list(dict.fromkeys(c for c in feature_names if c in work.columns))
    X = work[cols].copy()
    y = work[target].astype(float)
    return X, y
