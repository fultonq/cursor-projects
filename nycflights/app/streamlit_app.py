"""Interactive NYC Flights 2013 dashboard: EDA, missingness, dimensionality, delay ML."""

from __future__ import annotations

import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

# Package name is nycflights_ds (sibling of app/), not nycflights.nycflights_ds.
from bootstrap import ensure_nycflights_ds_on_path

ensure_nycflights_ds_on_path()

from nycflights_ds import prepare_dataset  # noqa: E402
from nycflights_ds.config import BUNDLE_PATH, METRICS_PATH  # noqa: E402
from nycflights_ds.dimensionality import (  # noqa: E402
    fit_pca,
    high_correlation_pairs,
    select_k_best,
    variance_table,
)
from nycflights_ds.eda import (  # noqa: E402
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
from nycflights_ds.features import modeling_frame  # noqa: E402
from nycflights_ds.load import missingness_frame  # noqa: E402
from nycflights_ds.model import load_bundle, predict_from_row, typical_row  # noqa: E402

sns.set_theme(style="whitegrid", context="notebook", palette="deep")
st.set_page_config(page_title="NYC Flights 2013", page_icon="✈️", layout="wide")


def _show(fig) -> None:
    st.pyplot(fig, clear_figure=True)
    plt.close(fig)


@st.cache_data(show_spinner="Loading and cleaning nycflights13…")
def load_frame(source: str) -> pd.DataFrame:
    return prepare_dataset(source)


@st.cache_resource(show_spinner=False)
def cached_bundle():
    if not BUNDLE_PATH.exists():
        return None
    return load_bundle()


def sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("Filters")
    origins = sorted(df["origin"].dropna().astype(str).unique())
    origin_sel = st.sidebar.multiselect("Origin", origins, default=origins)
    months = st.sidebar.slider("Month range", 1, 12, (1, 12))
    carriers = sorted(df["carrier"].dropna().astype(str).unique())
    default_carriers = carriers[:8] if len(carriers) > 8 else carriers
    carrier_sel = st.sidebar.multiselect("Carriers", carriers, default=default_carriers)
    operated_only = st.sidebar.checkbox("Operated flights only", value=True)

    out = df.loc[df["origin"].astype(str).isin(origin_sel)]
    out = out.loc[out["month"].between(months[0], months[1])]
    if carrier_sel:
        out = out.loc[out["carrier"].astype(str).isin(carrier_sel)]
    if operated_only and "operated" in out.columns:
        out = out.loc[out["operated"]]
    return out


def tab_overview(df: pd.DataFrame, filtered: pd.DataFrame) -> None:
    kpis = kpi_summary(filtered) if len(filtered) else kpi_summary(df)
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Flights in view", f"{int(kpis['n_flights']):,}")
    c2.metric("Cancel rate", f"{100 * kpis['cancel_rate']:.1f}%")
    c3.metric("Mean dep delay", f"{kpis['mean_dep_delay']:.1f} min")
    c4.metric("Dep delayed ≥15m", f"{100 * kpis['pct_dep_delayed']:.1f}%")
    c5.metric("Mean arr delay", f"{kpis['mean_arr_delay']:.1f} min")
    st.caption(
        "NYC outbound flights in 2013 (EWR, JFK, LGA). Delay models treat cancellations as a "
        "separate operational status — delay minutes are not imputed for flights that never left."
    )
    left, right = st.columns(2)
    with left:
        _show(plot_hourly_delay(filtered if len(filtered) else df))
    with right:
        _show(plot_origin_violin(filtered if len(filtered) else df))
    st.dataframe(
        filtered[
            [
                c
                for c in (
                    "month",
                    "day",
                    "origin",
                    "dest",
                    "carrier",
                    "airline_name",
                    "dep_delay",
                    "arr_delay",
                    "distance",
                    "status",
                )
                if c in filtered.columns
            ]
        ].head(25),
        use_container_width=True,
        hide_index=True,
    )


def tab_profile(df: pd.DataFrame) -> None:
    st.subheader("Characteristics and attributes")
    c1, c2, c3 = st.columns(3)
    c1.metric("Rows", f"{len(df):,}")
    c2.metric("Columns", f"{df.shape[1]}")
    c3.metric("Memory", f"{df.memory_usage(deep=True).sum() / 1e6:.1f} MB")

    miss = missingness_frame(df)
    left, right = st.columns([1.1, 1])
    with left:
        st.markdown("**Missingness after joins (before modeling row filters)**")
        _show(plot_missingness(miss))
    with right:
        st.markdown("**Dtypes and cardinality**")
        dtypes = pd.DataFrame(
            {
                "column": df.columns,
                "dtype": [str(t) for t in df.dtypes],
                "nunique": [df[c].nunique(dropna=True) for c in df.columns],
                "example": [df[c].dropna().iloc[0] if df[c].notna().any() else None for c in df.columns],
            }
        )
        st.dataframe(dtypes, use_container_width=True, hide_index=True, height=420)

    st.markdown("**NA policy**")
    st.markdown(
        """
- **Cancelled** (`dep_time` is NA): excluded from delay models; kept as `status='cancelled'`.
- **Diverted** (departed but `arr_delay` NA): excluded from arrival-delay models.
- **Weather**: origin × month median, then global `nanmedian`; `weather_missing` flag retained.
- **Aircraft year / seats**: median impute with `plane_age_missing`.
- **Wind gust**: dropped (mostly NA) and replaced with `wind_gust_reported`.
        """
    )
    st.dataframe(miss.head(25), use_container_width=True, hide_index=True)


def tab_eda(filtered: pd.DataFrame) -> None:
    if filtered.empty:
        st.warning("No rows match the current filters.")
        return
    choice = st.selectbox(
        "Chart",
        [
            "Delay distribution",
            "Delay by carrier",
            "Month × hour heatmap",
            "Cancellation rate",
            "Carrier on-time",
            "Distance vs air time",
            "Weather vs delay",
            "Numeric correlations",
        ],
    )
    if choice == "Delay distribution":
        col = st.radio("Target", ["dep_delay", "arr_delay"], horizontal=True)
        _show(plot_delay_distribution(filtered, col))
    elif choice == "Delay by carrier":
        _show(plot_delay_by_category(filtered, "carrier"))
    elif choice == "Month × hour heatmap":
        _show(plot_month_hour_heatmap(filtered))
    elif choice == "Cancellation rate":
        _show(plot_cancel_rate(filtered))
    elif choice == "Carrier on-time":
        try:
            _show(plot_carrier_ontime(filtered))
        except Exception:
            st.info("Not enough operated flights per carrier in this slice.")
    elif choice == "Distance vs air time":
        _show(plot_distance_airtime(filtered))
    elif choice == "Weather vs delay":
        _show(plot_weather_delay(filtered))
    else:
        cols = [
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
            if c in filtered.columns
        ]
        _show(plot_correlation_heatmap(filtered, cols))


def tab_dimensionality(df: pd.DataFrame) -> None:
    st.markdown(
        "Leakage-safe numeric features only. Actual `dep_time` / `arr_time` / `air_time` are "
        "excluded from departure models because they are outcomes, not predictors."
    )
    X, y = modeling_frame(df, target="dep_delay")
    num = X.select_dtypes(include=[np.number])
    left, right = st.columns(2)
    with left:
        st.markdown("**Near-zero variance**")
        st.dataframe(variance_table(num).head(12), use_container_width=True, hide_index=True)
        st.markdown("**|r| ≥ 0.85 pairs**")
        pairs = high_correlation_pairs(num, threshold=0.85)
        st.dataframe(pairs if not pairs.empty else pd.DataFrame({"note": ["none"]}), use_container_width=True, hide_index=True)
    with right:
        pca = fit_pca(num, n_components=min(8, num.shape[1]))
        _show(plot_pca_scree(pca["explained_variance_ratio"]))
        st.markdown("**SelectKBest (f_regression) vs departure delay**")
        selected = select_k_best(num, y, k=10, problem="regression")
        st.dataframe(selected["scores"].head(10), use_container_width=True, hide_index=True)


def tab_predict(df: pd.DataFrame) -> None:
    bundle = cached_bundle()
    if bundle is None:
        st.warning("No trained bundle yet. From `nycflights/` run `python -m nycflights_ds train`.")
        return

    origins = sorted(df["origin"].dropna().astype(str).unique())
    dests = sorted(df["dest"].dropna().astype(str).unique())
    carriers = sorted(df["carrier"].dropna().astype(str).unique())
    c1, c2, c3 = st.columns(3)
    origin = c1.selectbox("Origin", origins, index=origins.index("JFK") if "JFK" in origins else 0)
    dest = c2.selectbox("Destination", dests, index=min(dests.index("LAX") if "LAX" in dests else 0, len(dests) - 1))
    carrier = c3.selectbox("Carrier", carriers)
    c4, c5, c6, c7 = st.columns(4)
    month = c4.slider("Month", 1, 12, 7)
    day = c5.slider("Day", 1, 28, 15)
    hour = c6.slider("Scheduled hour", 0, 23, 8)
    minute = c7.slider("Minute", 0, 59, 0)

    row = typical_row(df, origin=origin, dest=dest, carrier=carrier, month=month, hour=hour, day=day, minute=minute)
    with st.expander("Weather & aircraft (defaults = historical median for this slot)", expanded=False):
        w1, w2, w3, w4 = st.columns(4)
        row["temp"] = w1.number_input("Temp (°F)", value=float(row.get("temp", 55) or 55))
        row["wind_speed"] = w2.number_input("Wind speed", value=float(row.get("wind_speed", 8) or 8))
        row["visib"] = w3.number_input("Visibility (mi)", value=float(row.get("visib", 10) or 10))
        row["precip"] = w4.number_input("Precip", value=float(row.get("precip", 0) or 0))
        row["distance"] = st.number_input("Distance (miles)", value=float(row.get("distance", 1000) or 1000))

    known_dep = st.checkbox("I already know the departure delay (better arrival forecast)", value=False)
    if known_dep:
        row["dep_delay"] = st.slider("Observed departure delay (min)", -20, 180, 10)

    preds = predict_from_row(bundle, row)
    m1, m2, m3 = st.columns(3)
    m1.metric("Predicted dep delay", f"{preds['pred_dep_delay']:.1f} min")
    m2.metric("Predicted arr delay", f"{preds['pred_arr_delay']:.1f} min")
    m3.metric("P(dep delay ≥ 15 min)", f"{100 * preds['p_dep_delayed']:.1f}%")
    st.caption("Gradient boosting models trained on Jan–Oct 2013 and scored on Nov–Dec.")


def tab_models() -> None:
    if METRICS_PATH.exists():
        metrics = json.loads(METRICS_PATH.read_text())
    elif BUNDLE_PATH.exists():
        metrics = load_bundle()["metrics"]
    else:
        st.warning("Train models first: `python -m nycflights_ds train`")
        return

    st.markdown(
        "Holdout is **temporal** (months 1–10 train, 11–12 test) so November weather and "
        "holiday schedules cannot leak into training. HistGradientBoosting is the production "
        "estimator; Ridge / logistic regression are linear baselines."
    )
    for target, label in (
        ("dep_delay", "Departure delay (minutes)"),
        ("arr_delay", "Arrival delay (minutes, uses dep_delay)"),
        ("dep_delayed", "Departure delayed ≥ 15 min"),
    ):
        st.subheader(label)
        block = metrics[target]
        cols = st.columns(2)
        for i, name in enumerate(("hgb", "linear")):
            with cols[i]:
                st.markdown(f"**{name}**  ·  n_train={block['n_train']:,}  n_test={block['n_test']:,}")
                pretty = {k: v for k, v in block[name].items() if k != "report"}
                st.json(pretty)

    bundle = cached_bundle()
    if bundle and bundle.get("dep_delay_importances"):
        st.subheader("Linear |coefficient| — departure delay")
        imp = pd.DataFrame(bundle["dep_delay_importances"])
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(data=imp.head(15), y="feature", x="importance", ax=ax, color="#4C78A8")
        ax.set_title("Ridge absolute coefficients (transformed space)")
        fig.tight_layout()
        _show(fig)


def main() -> None:
    st.title("✈️ NYC Flights 2013")
    st.caption("pandas · numpy · seaborn · scikit-learn · Streamlit")

    source = st.sidebar.radio("Dataset", ["raw", "sample"], index=0, help="raw = full 336,776 flights (downloaded on first use)")
    df = load_frame(source)
    filtered = sidebar_filters(df)
    st.sidebar.markdown(f"{len(filtered):,} rows after filters")

    overview, profile, eda, dim, predict, models = st.tabs(
        ["Overview", "Profile & NA", "EDA", "Dimensionality", "Predict", "Model lab"]
    )
    with overview:
        tab_overview(df, filtered)
    with profile:
        tab_profile(df)
    with eda:
        tab_eda(filtered)
    with dim:
        tab_dimensionality(df)
    with predict:
        tab_predict(df)
    with models:
        tab_models()


if __name__ == "__main__":
    main()
