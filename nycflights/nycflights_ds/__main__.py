"""CLI: python -m nycflights_ds [download|profile|prepare|eda|train]."""

from __future__ import annotations

import argparse
import json

import matplotlib

matplotlib.use("Agg")

from nycflights_ds import prepare_dataset
from nycflights_ds.config import DATA_PROCESSED, FIGURES_DIR, MODELS_DIR
from nycflights_ds.eda import (
    kpi_summary,
    plot_cancel_rate,
    plot_carrier_ontime,
    plot_correlation_heatmap,
    plot_delay_by_category,
    plot_delay_distribution,
    plot_distance_airtime,
    plot_hourly_delay,
    plot_missingness,
    plot_month_hour_heatmap,
    plot_origin_violin,
    plot_pca_scree,
    plot_weather_delay,
)
from nycflights_ds.load import download_tables, load_tables, missingness_frame, profile, write_sample
from nycflights_ds.dimensionality import fit_pca
from nycflights_ds.model import train_bundle


def _save_fig(fig, name: str) -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    path = FIGURES_DIR / name
    fig.savefig(path, dpi=120, bbox_inches="tight")
    fig.clear()


def cmd_download(args: argparse.Namespace) -> None:
    paths = download_tables(force=args.force)
    tables = load_tables("raw")
    write_sample(tables)
    print("Downloaded:")
    for name, path in paths.items():
        print(f"  {name}: {path} ({path.stat().st_size / 1e6:.1f} MB)")
    print("Wrote data/sample for tests and demos.")


def cmd_profile(args: argparse.Namespace) -> None:
    tables = load_tables(args.source)
    for name, df in tables.items():
        info = profile(df, name=name)
        print(f"\n=== {name} ===")
        print(f"shape: {info['n_rows']:,} × {info['n_cols']}  memory: {info['memory_mb']} MB")
        miss = missingness_frame(df)
        miss = miss.loc[miss["n_missing"] > 0]
        if miss.empty:
            print("no missing values")
        else:
            print(miss.head(12).to_string(index=False))


def cmd_prepare(args: argparse.Namespace) -> None:
    df = prepare_dataset(args.source)
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    out = DATA_PROCESSED / "flights_enriched.parquet"
    df.to_parquet(out, index=False)
    kpis = kpi_summary(df)
    print(json.dumps(kpis, indent=2))
    print(f"Wrote {out}  shape={df.shape}")


def cmd_eda(args: argparse.Namespace) -> None:
    df = prepare_dataset(args.source)
    miss = missingness_frame(df)
    _save_fig(plot_missingness(miss), "missingness.png")
    _save_fig(plot_delay_distribution(df, "dep_delay"), "dep_delay_hist.png")
    _save_fig(plot_delay_distribution(df, "arr_delay"), "arr_delay_hist.png")
    _save_fig(plot_delay_by_category(df, "carrier"), "delay_by_carrier.png")
    _save_fig(plot_hourly_delay(df), "delay_by_hour.png")
    _save_fig(plot_month_hour_heatmap(df), "month_hour_heatmap.png")
    _save_fig(plot_origin_violin(df), "origin_violin.png")
    _save_fig(plot_distance_airtime(df), "distance_airtime.png")
    _save_fig(plot_weather_delay(df), "weather_delay.png")
    _save_fig(plot_cancel_rate(df), "cancel_rate.png")
    if "airline_name" in df.columns:
        _save_fig(plot_carrier_ontime(df), "carrier_ontime.png")
    corr_cols = [
        c
        for c in (
            "dep_delay",
            "arr_delay",
            "distance",
            "air_time",
            "hour",
            "temp",
            "wind_speed",
            "precip",
            "visib",
            "plane_age",
        )
        if c in df.columns
    ]
    _save_fig(plot_correlation_heatmap(df, corr_cols), "correlation.png")
    pca_cols = [c for c in ("hour", "distance", "temp", "humid", "wind_speed", "visib", "plane_age", "seats") if c in df.columns]
    pca = fit_pca(df[pca_cols].dropna(), n_components=min(6, len(pca_cols)))
    _save_fig(plot_pca_scree(pca["explained_variance_ratio"]), "pca_scree.png")
    print(f"Wrote figures to {FIGURES_DIR}")


def cmd_train(args: argparse.Namespace) -> None:
    df = prepare_dataset(args.source)
    sample = None if args.full else args.sample_size
    bundle = train_bundle(df, sample_size=sample, persist=True)
    print(json.dumps(bundle["metrics"], indent=2, default=str))
    print(f"Saved bundle to {MODELS_DIR}")


def main() -> None:
    parser = argparse.ArgumentParser(prog="nycflights_ds")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_dl = sub.add_parser("download", help="Fetch nycflights13 CSVs")
    p_dl.add_argument("--force", action="store_true")
    p_dl.set_defaults(func=cmd_download)

    p_pr = sub.add_parser("profile", help="Print shape, dtypes, missingness")
    p_pr.add_argument("--source", default="raw", choices=("raw", "sample"))
    p_pr.set_defaults(func=cmd_profile)

    p_prep = sub.add_parser("prepare", help="Clean, join, engineer, write parquet")
    p_prep.add_argument("--source", default="raw", choices=("raw", "sample"))
    p_prep.set_defaults(func=cmd_prepare)

    p_eda = sub.add_parser("eda", help="Write seaborn figures under reports/figures")
    p_eda.add_argument("--source", default="raw", choices=("raw", "sample"))
    p_eda.set_defaults(func=cmd_eda)

    p_tr = sub.add_parser("train", help="Fit delay models on a Jan–Oct / Nov–Dec split")
    p_tr.add_argument("--source", default="raw", choices=("raw", "sample"))
    p_tr.add_argument("--sample-size", type=int, default=60_000)
    p_tr.add_argument("--full", action="store_true", help="Use all training rows")
    p_tr.set_defaults(func=cmd_train)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
