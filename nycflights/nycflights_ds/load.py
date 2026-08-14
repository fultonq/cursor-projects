"""Download, load, and profile nycflights13 tables with pandas."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from nycflights_ds.config import DATA_RAW, DATA_SAMPLE, RDATASETS_BASE, TABLES

FLIGHT_DTYPES: dict[str, str] = {
    "year": "int16",
    "month": "int8",
    "day": "int8",
    "sched_dep_time": "int16",
    "sched_arr_time": "int16",
    "flight": "int16",
    "hour": "int8",
    "minute": "int8",
    "distance": "int16",
    "carrier": "string",
    "tailnum": "string",
    "origin": "string",
    "dest": "string",
}


def table_url(name: str) -> str:
    return f"{RDATASETS_BASE}/{name}.csv"


def download_tables(dest: Path | None = None, *, force: bool = False) -> dict[str, Path]:
    """Fetch the five nycflights13 CSVs into data/raw (idempotent)."""
    dest = dest or DATA_RAW
    dest.mkdir(parents=True, exist_ok=True)
    paths: dict[str, Path] = {}
    for name in TABLES:
        path = dest / f"{name}.csv"
        paths[name] = path
        if path.exists() and not force:
            continue
        df = pd.read_csv(table_url(name))
        df = _drop_rownames(df)
        df.to_csv(path, index=False)
    return paths


def _drop_rownames(df: pd.DataFrame) -> pd.DataFrame:
    if "rownames" in df.columns:
        return df.drop(columns=["rownames"])
    unnamed = [c for c in df.columns if str(c).startswith("Unnamed")]
    return df.drop(columns=unnamed) if unnamed else df


def _read_csv(path: Path) -> pd.DataFrame:
    kwargs: dict[str, Any] = {}
    if path.stem == "flights":
        kwargs["dtype"] = FLIGHT_DTYPES
        kwargs["parse_dates"] = ["time_hour"]
    elif path.stem == "weather":
        kwargs["parse_dates"] = ["time_hour"]
    return _drop_rownames(pd.read_csv(path, **kwargs))


def load_tables(source: str | Path = "raw") -> dict[str, pd.DataFrame]:
    """Load flights, airlines, airports, planes, and weather.

    Parameters
    ----------
    source:
        ``raw`` (full download), ``sample`` (committed subset), a directory of
        CSVs, or ``processed`` (single parquet produced by the pipeline).
    """
    if source == "processed":
        from nycflights_ds.config import DATA_PROCESSED

        path = DATA_PROCESSED / "flights_enriched.parquet"
        if not path.exists():
            raise FileNotFoundError(f"Processed table missing: {path}")
        return {"flights_enriched": pd.read_parquet(path)}

    if source == "raw":
        download_tables()
        directory = DATA_RAW
    elif source == "sample":
        directory = DATA_SAMPLE
    else:
        directory = Path(source)

    tables = {name: _read_csv(directory / f"{name}.csv") for name in TABLES}
    return tables


def memory_mb(df: pd.DataFrame) -> float:
    return float(df.memory_usage(deep=True).sum() / 1e6)


def downcast_flights(df: pd.DataFrame) -> pd.DataFrame:
    """Reduce dimensionality of the *storage* representation via dtypes."""
    out = df.copy()
    for col in ("carrier", "origin", "dest", "tailnum"):
        if col in out.columns:
            out[col] = out[col].astype("category")
    for col in out.select_dtypes(include=["float64"]).columns:
        out[col] = pd.to_numeric(out[col], downcast="float")
    for col in out.select_dtypes(include=["int64", "int32"]).columns:
        out[col] = pd.to_numeric(out[col], downcast="integer")
    return out


def profile(df: pd.DataFrame, *, name: str = "frame") -> dict[str, Any]:
    """Characteristics and attributes: shape, dtypes, missingness, cardinality."""
    missing_count = df.isna().sum()
    missing_pct = (100 * missing_count / max(len(df), 1)).round(3)
    nunique = df.nunique(dropna=True)
    numeric = df.select_dtypes(include=[np.number])
    summary = (
        numeric.describe(percentiles=[0.01, 0.05, 0.5, 0.95, 0.99]).T
        if not numeric.empty
        else pd.DataFrame()
    )
    return {
        "name": name,
        "n_rows": int(df.shape[0]),
        "n_cols": int(df.shape[1]),
        "memory_mb": round(memory_mb(df), 3),
        "columns": list(df.columns),
        "dtypes": {c: str(t) for c, t in df.dtypes.items()},
        "missing_count": missing_count.to_dict(),
        "missing_pct": missing_pct.to_dict(),
        "nunique": nunique.to_dict(),
        "numeric_summary": summary.reset_index().rename(columns={"index": "column"}).to_dict(
            orient="records"
        ),
        "head": df.head(5).astype(object).where(df.head(5).notna(), None).to_dict(orient="records"),
    }


def missingness_frame(df: pd.DataFrame) -> pd.DataFrame:
    count = df.isna().sum()
    out = pd.DataFrame(
        {
            "column": count.index,
            "n_missing": count.to_numpy(),
            "pct_missing": np.round(100 * count.to_numpy() / max(len(df), 1), 3),
            "dtype": [str(df[c].dtype) for c in count.index],
            "nunique": [int(df[c].nunique(dropna=True)) for c in count.index],
        }
    )
    return out.sort_values(["n_missing", "column"], ascending=[False, True]).reset_index(drop=True)


def write_sample(
    tables: dict[str, pd.DataFrame],
    dest: Path | None = None,
    *,
    n_flights: int = 2500,
    seed: int = 42,
) -> Path:
    """Persist a tiny real subset so tests and demos run without the full CSV."""
    dest = dest or DATA_SAMPLE
    dest.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    flights = tables["flights"]
    idx = rng.choice(len(flights), size=min(n_flights, len(flights)), replace=False)
    sample = flights.iloc[np.sort(idx)].copy()
    sample.to_csv(dest / "flights.csv", index=False)

    carriers = sample["carrier"].dropna().unique()
    tailnums = sample["tailnum"].dropna().unique()
    origins = sample["origin"].dropna().unique()
    dests = pd.Index(sample["dest"].dropna().unique())
    faa_keep = pd.Index(origins).append(dests).unique()

    tables["airlines"].query("carrier in @carriers").to_csv(dest / "airlines.csv", index=False)
    tables["airports"].query("faa in @faa_keep").to_csv(dest / "airports.csv", index=False)
    tables["planes"].query("tailnum in @tailnums").to_csv(dest / "planes.csv", index=False)

    keys = sample[["origin", "year", "month", "day", "hour"]].drop_duplicates()
    weather = tables["weather"].merge(keys, on=["origin", "year", "month", "day", "hour"], how="inner")
    weather.to_csv(dest / "weather.csv", index=False)
    return dest
