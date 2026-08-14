"""Seaborn / matplotlib EDA helpers. Each function returns a Figure for Streamlit."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid", context="talk", palette="deep")


def _figure(width: float = 10, height: float = 5.5) -> tuple[plt.Figure, plt.Axes]:
    fig, ax = plt.subplots(figsize=(width, height))
    return fig, ax


def maybe_sample(df: pd.DataFrame, n: int = 12_000, random_state: int = 42) -> pd.DataFrame:
    if len(df) <= n:
        return df
    return df.sample(n=n, random_state=random_state)


def plot_missingness(missing_df: pd.DataFrame) -> plt.Figure:
    data = missing_df.loc[missing_df["n_missing"] > 0].head(20)
    fig, ax = _figure()
    if data.empty:
        ax.set_title("No missing values")
        return fig
    sns.barplot(data=data, x="pct_missing", y="column", ax=ax, color="#4C78A8")
    ax.set_xlabel("% missing")
    ax.set_ylabel("")
    ax.set_title("Missingness by column")
    fig.tight_layout()
    return fig


def plot_delay_distribution(df: pd.DataFrame, col: str = "dep_delay") -> plt.Figure:
    data = df.loc[df[col].notna(), col].to_numpy(dtype=float)
    clipped = data[(data > np.nanpercentile(data, 1)) & (data < np.nanpercentile(data, 99))]
    fig, ax = _figure()
    sns.histplot(clipped, bins=60, kde=True, ax=ax, color="#4C78A8")
    ax.axvline(0, color="#333", linestyle="--", linewidth=1)
    ax.axvline(15, color="#E45756", linestyle="--", linewidth=1, label="FAA 15-min delay")
    ax.set_xlabel(col.replace("_", " "))
    ax.set_title(f"Distribution of {col.replace('_', ' ')} (1st–99th percentile)")
    ax.legend()
    fig.tight_layout()
    return fig


def plot_delay_by_category(df: pd.DataFrame, category: str, col: str = "dep_delay") -> plt.Figure:
    work = df.loc[df[col].notna(), [category, col]]
    order = work.groupby(category, observed=True)[col].median().sort_values().index
    fig, ax = _figure(width=11, height=5.5)
    sns.boxplot(data=work, x=category, y=col, order=order, ax=ax, showfliers=False)
    ax.axhline(15, color="#E45756", linestyle="--", linewidth=1)
    ax.set_title(f"{col.replace('_', ' ')} by {category}")
    ax.tick_params(axis="x", rotation=35)
    fig.tight_layout()
    return fig


def plot_hourly_delay(df: pd.DataFrame, col: str = "dep_delay") -> plt.Figure:
    grouped = (
        df.loc[df[col].notna()]
        .groupby("hour", observed=True)[col]
        .agg(mean="mean", median="median", n="size")
        .reset_index()
    )
    fig, ax = _figure()
    sns.lineplot(data=grouped, x="hour", y="mean", marker="o", ax=ax, label="mean")
    sns.lineplot(data=grouped, x="hour", y="median", marker="s", ax=ax, label="median")
    ax.axhline(15, color="#E45756", linestyle="--", linewidth=1, label="15 min")
    ax.set_title("Departure delay by scheduled hour")
    ax.set_ylabel("minutes")
    fig.tight_layout()
    return fig


def plot_month_hour_heatmap(df: pd.DataFrame, col: str = "dep_delay") -> plt.Figure:
    pivot = (
        df.loc[df[col].notna()]
        .pivot_table(index="month", columns="hour", values=col, aggfunc="mean", observed=True)
    )
    fig, ax = _figure(width=12, height=5)
    sns.heatmap(pivot, cmap="YlOrRd", ax=ax, cbar_kws={"label": "mean delay (min)"})
    ax.set_title("Mean departure delay: month × scheduled hour")
    fig.tight_layout()
    return fig


def plot_origin_violin(df: pd.DataFrame, col: str = "dep_delay") -> plt.Figure:
    work = df.loc[df[col].notna() & (df[col].abs() < 120), ["origin", col]]
    fig, ax = _figure()
    sns.violinplot(data=work, x="origin", y=col, ax=ax, inner="quartile", cut=0)
    ax.set_title("Delay shape by NYC origin airport")
    fig.tight_layout()
    return fig


def plot_distance_airtime(df: pd.DataFrame) -> plt.Figure:
    work = maybe_sample(df.dropna(subset=["distance", "air_time"]))
    fig, ax = _figure()
    sns.scatterplot(
        data=work,
        x="distance",
        y="air_time",
        hue="origin",
        alpha=0.35,
        s=18,
        ax=ax,
    )
    ax.set_title("Air time vs distance")
    fig.tight_layout()
    return fig


def plot_weather_delay(df: pd.DataFrame) -> plt.Figure:
    work = maybe_sample(df.dropna(subset=["visib", "dep_delay", "wind_speed"]))
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    sns.scatterplot(data=work, x="visib", y="dep_delay", alpha=0.25, s=14, ax=axes[0], color="#4C78A8")
    axes[0].set_title("Visibility vs departure delay")
    sns.scatterplot(data=work, x="wind_speed", y="dep_delay", alpha=0.25, s=14, ax=axes[1], color="#F58518")
    axes[1].set_title("Wind speed vs departure delay")
    fig.tight_layout()
    return fig


def plot_correlation_heatmap(df: pd.DataFrame, columns: list[str]) -> plt.Figure:
    corr = df[columns].corr(numeric_only=True)
    fig, ax = _figure(width=10, height=8)
    sns.heatmap(corr, cmap="vlag", center=0, ax=ax, square=True, linewidths=0.3)
    ax.set_title("Numeric feature correlations")
    fig.tight_layout()
    return fig


def plot_cancel_rate(df: pd.DataFrame) -> plt.Figure:
    rates = (
        df.groupby(["month", "origin"], observed=True)["cancelled"]
        .mean()
        .mul(100)
        .reset_index(name="cancel_pct")
    )
    fig, ax = _figure()
    sns.lineplot(data=rates, x="month", y="cancel_pct", hue="origin", marker="o", ax=ax)
    ax.set_ylabel("% cancelled")
    ax.set_title("Cancellation rate by month and origin")
    fig.tight_layout()
    return fig


def plot_carrier_ontime(df: pd.DataFrame) -> plt.Figure:
    work = df.loc[df["operated"] & df["dep_delayed"].notna()]
    stats = (
        work.groupby("airline_name", observed=True)
        .agg(n=("dep_delayed", "size"), delayed=("dep_delayed", "mean"), mean_delay=("dep_delay", "mean"))
        .query("n >= 200")
        .sort_values("delayed")
        .reset_index()
    )
    stats["on_time"] = 100 * (1 - stats["delayed"])
    fig, ax = _figure(width=11, height=6)
    if stats.empty:
        ax.set_title("Not enough operated flights per carrier in this slice")
        fig.tight_layout()
        return fig
    sns.barplot(data=stats, y="airline_name", x="on_time", ax=ax, color="#54A24B")
    ax.set_xlabel("On-time departure % (delay < 15 min)")
    ax.set_ylabel("")
    ax.set_title("Carrier on-time performance (n ≥ 200 operated flights)")
    fig.tight_layout()
    return fig


def plot_pca_scree(explained: list[float]) -> plt.Figure:
    fig, ax = _figure()
    xs = np.arange(1, len(explained) + 1)
    ax.bar(xs, explained, color="#4C78A8", label="individual")
    ax.plot(xs, np.cumsum(explained), marker="o", color="#E45756", label="cumulative")
    ax.set_xlabel("Principal component")
    ax.set_ylabel("Explained variance ratio")
    ax.set_title("PCA scree plot")
    ax.legend()
    fig.tight_layout()
    return fig


def kpi_summary(df: pd.DataFrame) -> dict[str, float]:
    operated = df.loc[df["operated"]]
    return {
        "n_flights": float(len(df)),
        "n_operated": float(operated.shape[0]),
        "cancel_rate": float(df["cancelled"].mean()),
        "mean_dep_delay": float(operated["dep_delay"].mean()),
        "median_dep_delay": float(operated["dep_delay"].median()),
        "pct_dep_delayed": float(operated["dep_delayed"].mean()),
        "mean_arr_delay": float(operated["arr_delay"].mean()),
        "pct_arr_delayed": float(operated["arr_delayed"].mean()),
        "mean_distance": float(df["distance"].mean()),
    }
