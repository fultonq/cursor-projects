from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from nycflights_ds.clean import clean, flag_operational_status, hhmm_to_minutes, impute_weather
from nycflights_ds.features import engineer, modeling_frame
from nycflights_ds.load import missingness_frame, profile
from nycflights_ds.model import hgb_pipeline, linear_pipeline, typical_row


def _mini_tables() -> dict[str, pd.DataFrame]:
    flights = pd.DataFrame(
        {
            "year": [2013, 2013, 2013, 2013, 2013],
            "month": [1, 1, 6, 11, 12],
            "day": [1, 2, 10, 15, 20],
            "dep_time": [517.0, np.nan, 800.0, 1805.0, 2400.0],
            "sched_dep_time": [515, 600, 800, 1800, 2359],
            "dep_delay": [2.0, np.nan, 40.0, -3.0, 5.0],
            "arr_time": [830.0, np.nan, 1100.0, np.nan, 200.0],
            "sched_arr_time": [819, 800, 1030, 2100, 159],
            "arr_delay": [11.0, np.nan, 25.0, np.nan, -8.0],
            "carrier": ["UA", "AA", "B6", "UA", "DL"],
            "flight": [1545, 100, 200, 300, 400],
            "tailnum": ["N1", "N2", "N1", "N3", "N1"],
            "origin": ["EWR", "JFK", "LGA", "EWR", "JFK"],
            "dest": ["IAH", "LAX", "BOS", "IAH", "ATL"],
            "air_time": [227.0, np.nan, 45.0, np.nan, 110.0],
            "distance": [1400, 2475, 184, 1400, 760],
            "hour": [5, 6, 8, 18, 23],
            "minute": [15, 0, 0, 0, 59],
            "time_hour": pd.to_datetime(
                [
                    "2013-01-01 05:00:00",
                    "2013-01-02 06:00:00",
                    "2013-06-10 08:00:00",
                    "2013-11-15 18:00:00",
                    "2013-12-20 23:00:00",
                ]
            ),
        }
    )
    airlines = pd.DataFrame(
        {"carrier": ["UA", "AA", "B6", "DL"], "name": ["United", "American", "JetBlue", "Delta"]}
    )
    airports = pd.DataFrame(
        {
            "faa": ["EWR", "JFK", "LGA", "IAH", "LAX", "BOS", "ATL"],
            "name": list("abcdefg"),
            "lat": [40.7, 40.6, 40.8, 29.9, 33.9, 42.3, 33.6],
            "lon": [-74.1, -73.7, -73.8, -95.3, -118.4, -71.0, -84.4],
            "alt": [18, 13, 11, 97, 125, 20, 1026],
            "tz": [-5] * 7,
            "dst": ["A"] * 7,
            "tzone": ["America/New_York"] * 7,
        }
    )
    planes = pd.DataFrame(
        {
            "tailnum": ["N1", "N2", "N3"],
            "year": [2004.0, np.nan, 1998.0],
            "type": ["jet"] * 3,
            "manufacturer": ["AIRBUS"] * 3,
            "model": ["A320"] * 3,
            "engines": [2, 2, 2],
            "seats": [180, 150, 160],
            "speed": [np.nan, np.nan, np.nan],
            "engine": ["Turbo-fan", "Turbo-fan", "Turbo-jet"],
        }
    )
    weather = pd.DataFrame(
        {
            "origin": ["EWR", "JFK", "LGA", "EWR", "JFK"],
            "year": [2013] * 5,
            "month": [1, 1, 6, 11, 12],
            "day": [1, 2, 10, 15, 20],
            "hour": [5, 6, 8, 18, 23],
            "temp": [39.0, np.nan, 72.0, 45.0, 30.0],
            "dewp": [26.0, 20.0, 60.0, 30.0, 20.0],
            "humid": [50.0, 40.0, 80.0, 55.0, 60.0],
            "wind_dir": [270.0, 180.0, 90.0, 200.0, 10.0],
            "wind_speed": [10.0, 8.0, 12.0, np.nan, 15.0],
            "wind_gust": [np.nan, np.nan, 20.0, np.nan, np.nan],
            "precip": [0.0, 0.1, 0.0, 0.0, 0.2],
            "pressure": [1012.0, 1010.0, np.nan, 1015.0, 1020.0],
            "visib": [10.0, 4.0, 10.0, 10.0, 8.0],
            "time_hour": flights["time_hour"],
        }
    )
    return {
        "flights": flights,
        "airlines": airlines,
        "airports": airports,
        "planes": planes,
        "weather": weather,
    }


@pytest.fixture
def tables() -> dict[str, pd.DataFrame]:
    return _mini_tables()


@pytest.fixture
def prepared(tables) -> pd.DataFrame:
    return engineer(clean(tables))


def test_hhmm_midnight_and_morning():
    converted = hhmm_to_minutes(pd.Series([517, 2400, 5]))
    assert converted.tolist() == [5 * 60 + 17, 0, 5]


def test_cancelled_and_diverted_flags(tables):
    flagged = flag_operational_status(tables["flights"])
    assert bool(flagged.loc[1, "cancelled"])
    assert bool(flagged.loc[3, "diverted"])
    assert flagged["status"].tolist() == ["operated", "cancelled", "operated", "diverted", "operated"]


def test_weather_impute_fills_numeric_na(tables):
    assembled = clean(tables)
    assert assembled["temp"].isna().sum() == 0
    assert assembled["wind_speed"].isna().sum() == 0
    assert "wind_gust" not in assembled.columns
    assert "weather_missing" in assembled.columns


def test_profile_and_missingness_shape(tables):
    info = profile(tables["flights"], name="flights")
    assert info["n_rows"] == 5
    assert "dep_delay" in info["missing_pct"]
    miss = missingness_frame(tables["flights"])
    assert miss.loc[miss["column"] == "dep_time", "n_missing"].iloc[0] == 1


def test_engineer_cyclical_and_labels(prepared):
    assert {"hour_sin", "hour_cos", "month_sin", "season", "dep_delayed"}.issubset(prepared.columns)
    operated = prepared.loc[prepared["operated"]]
    assert operated["dep_delayed"].isna().sum() == 0
    delayed_row = operated.loc[operated["dep_delay"] == 40].iloc[0]
    assert delayed_row["dep_delayed"] == 1.0


def test_modeling_frame_excludes_cancellations_and_leakage(prepared):
    X, y = modeling_frame(prepared, target="dep_delay")
    assert len(X) == 4  # one cancelled row dropped
    for leaked in ("dep_time", "arr_time", "arr_delay", "air_time", "dep_minutes"):
        assert leaked not in X.columns
    X_arr, y_arr = modeling_frame(prepared, target="arr_delay")
    assert "dep_delay" in X_arr.columns
    assert len(X_arr) == 3  # cancelled + diverted dropped


def test_linear_and_hgb_fit_predict_on_tiny_frame(prepared):
    # Repeat rows so both month splits and estimators have enough data.
    big = pd.concat([prepared] * 40, ignore_index=True)
    train = big.loc[big["month"] <= 10]
    test = big.loc[big["month"] >= 11]
    X_train, y_train = modeling_frame(train, target="dep_delay")
    X_test, y_test = modeling_frame(test, target="dep_delay")
    X_test = X_test.reindex(columns=X_train.columns)
    ridge = linear_pipeline(list(X_train.columns))
    hgb = hgb_pipeline(list(X_train.columns))
    ridge.fit(X_train, y_train)
    hgb.fit(X_train, y_train)
    pred_r = ridge.predict(X_test)
    pred_h = hgb.predict(X_test)
    assert pred_r.shape == (len(X_test),)
    assert pred_h.shape == (len(X_test),)
    assert np.isfinite(pred_r).all()
    assert np.isfinite(pred_h).all()


def test_typical_row_overrides(prepared):
    row = typical_row(prepared, origin="EWR", dest="IAH", carrier="UA", month=1, hour=5)
    assert row["origin"] == "EWR"
    assert row["part_of_day"] == "night"
    assert "hour_sin" in row.index
