"""Missing-value handling, operational flags, joins, and dtype cleanup."""

from __future__ import annotations

import numpy as np
import pandas as pd

from .config import YEAR


def hhmm_to_minutes(series: pd.Series) -> pd.Series:
    """Convert HHMM / HMM clock values (e.g. 517, 2400) to minutes past midnight."""
    clock = pd.to_numeric(series, errors="coerce")
    hours = np.floor_divide(clock, 100)
    minutes = np.mod(clock, 100)
    # BTS encodes midnight as 2400.
    overflow = hours >= 24
    hours = hours.where(~overflow, hours - 24)
    return hours * 60 + minutes


def flag_operational_status(flights: pd.DataFrame) -> pd.DataFrame:
    """Cancelled / diverted / operated — NA delays are not missing-at-random."""
    out = flights.copy()
    out["cancelled"] = out["dep_time"].isna()
    out["diverted"] = (~out["cancelled"]) & out["arr_delay"].isna()
    out["operated"] = ~out["cancelled"]
    out["status"] = np.select(
        [out["cancelled"], out["diverted"]],
        ["cancelled", "diverted"],
        default="operated",
    )
    return out


def _rename_airports(airports: pd.DataFrame, prefix: str, key: str) -> pd.DataFrame:
    renamed = airports.rename(columns={c: f"{prefix}{c}" if c != "faa" else key for c in airports.columns})
    keep = [key, f"{prefix}name", f"{prefix}lat", f"{prefix}lon", f"{prefix}alt", f"{prefix}tzone"]
    return renamed[keep]


def assemble_flight_table(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Left-join airlines, plane metadata, airports, and hourly weather."""
    flights = flag_operational_status(tables["flights"])
    airlines = tables["airlines"].rename(columns={"name": "airline_name"})
    planes = (
        tables["planes"]
        .rename(
            columns={
                "year": "plane_year",
                "type": "plane_type",
                "model": "plane_model",
                "engine": "engine_type",
            }
        )
        .drop(columns=["speed"], errors="ignore")
    )
    origin_ap = _rename_airports(tables["airports"], "orig_", "origin")
    dest_ap = _rename_airports(tables["airports"], "dest_", "dest")

    weather_keep = [
        "origin",
        "year",
        "month",
        "day",
        "hour",
        "temp",
        "dewp",
        "humid",
        "wind_dir",
        "wind_speed",
        "wind_gust",
        "precip",
        "pressure",
        "visib",
    ]
    weather = tables["weather"][weather_keep]

    assembled = (
        flights.merge(airlines, on="carrier", how="left")
        .merge(planes, on="tailnum", how="left")
        .merge(origin_ap, on="origin", how="left")
        .merge(dest_ap, on="dest", how="left")
        .merge(weather, on=["origin", "year", "month", "day", "hour"], how="left")
    )
    return assembled


def add_missing_indicators(df: pd.DataFrame, columns: tuple[str, ...]) -> pd.DataFrame:
    out = df.copy()
    for col in columns:
        if col in out.columns:
            out[f"{col}_missing"] = out[col].isna().astype(np.int8)
    return out


def impute_weather(df: pd.DataFrame) -> pd.DataFrame:
    """Median impute weather by origin × month, then global median; keep indicators."""
    out = df.copy()
    weather_cols = ["temp", "dewp", "humid", "wind_speed", "precip", "pressure", "visib", "wind_dir"]
    present = [c for c in weather_cols if c in out.columns]
    out["weather_missing"] = out[present].isna().any(axis=1).astype(np.int8) if present else 0

    grouped = out.groupby(["origin", "month"], observed=True)
    for col in present:
        out[col] = out[col].fillna(grouped[col].transform(lambda s: s.median()))
        out[col] = out[col].fillna(np.nanmedian(out[col].to_numpy(dtype=float)))
    if "wind_gust" in out.columns:
        # Almost entirely missing — collapse to a binary gust-reported flag.
        out["wind_gust_reported"] = out["wind_gust"].notna().astype(np.int8)
        out = out.drop(columns=["wind_gust"])
    return out


def impute_plane_fields(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if "plane_year" in out.columns:
        out["plane_age_missing"] = out["plane_year"].isna().astype(np.int8)
        median_year = float(np.nanmedian(out["plane_year"].to_numpy(dtype=float)))
        out["plane_year"] = out["plane_year"].fillna(median_year)
        out["plane_age"] = (YEAR - out["plane_year"]).clip(lower=0, upper=60)
    if "seats" in out.columns:
        out["seats"] = out["seats"].fillna(out["seats"].median())
    if "engines" in out.columns:
        out["engines"] = out["engines"].fillna(out["engines"].median())
    if "engine_type" in out.columns:
        out["engine_type"] = out["engine_type"].astype("string").fillna("Unknown")
    return out


def drop_constant_and_id_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Dimensionality: remove IDs, constants, and columns that are functions of others."""
    drop = [
        "year",  # always 2013 in this dataset
        "flight",  # high-cardinality identifier, not a useful categorical
        "tailnum",
        "time_hour",
        "plane_type",
        "plane_model",
        "manufacturer",
        "orig_name",
        "dest_name",
        "orig_tzone",
        "dest_tzone",
        "sched_dep_time",  # redundant with hour/minute
        "sched_arr_time",
    ]
    return df.drop(columns=[c for c in drop if c in df.columns], errors="ignore")


def clip_delay_outliers(df: pd.DataFrame, cols: tuple[str, ...] = ("dep_delay", "arr_delay")) -> pd.DataFrame:
    """Winsorize extreme delays for *modeling* copies; EDA keeps the raw tails."""
    out = df.copy()
    for col in cols:
        if col not in out.columns:
            continue
        values = out[col].to_numpy(dtype=float)
        lo, hi = np.nanpercentile(values, [0.5, 99.5])
        out[f"{col}_clipped"] = np.clip(values, lo, hi)
    return out


def clean(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """End-to-end assemble → NA strategy → indicators → drop unused dimensions."""
    assembled = assemble_flight_table(tables)
    cleaned = (
        assembled.pipe(add_missing_indicators, ("precip", "pressure", "visib", "temp"))
        .pipe(impute_weather)
        .pipe(impute_plane_fields)
        .pipe(drop_constant_and_id_columns)
    )
    return cleaned
