"""Scikit-learn pipelines for departure/arrival delay regression and classification."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier, HistGradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    classification_report,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler, TargetEncoder
from sklearn.utils.class_weight import compute_sample_weight

from .config import (
    BUNDLE_PATH,
    DELAY_THRESHOLD_MIN,
    HIGH_CARD_CATEGORICALS,
    LOW_CARD_CATEGORICALS,
    METRICS_PATH,
    MODELS_DIR,
    RANDOM_STATE,
    TEST_MONTHS,
    TRAIN_MONTHS,
)
from .features import modeling_frame


def time_split(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    train = df.loc[df["month"].isin(TRAIN_MONTHS)]
    test = df.loc[df["month"].isin(TEST_MONTHS)]
    return train, test


def _categoricals(columns: list[str]) -> tuple[list[str], list[str]]:
    low = [c for c in LOW_CARD_CATEGORICALS if c in columns]
    high = [c for c in HIGH_CARD_CATEGORICALS if c in columns]
    return low, high


def _numerics(columns: list[str]) -> list[str]:
    cat = set(LOW_CARD_CATEGORICALS + HIGH_CARD_CATEGORICALS)
    return [c for c in columns if c not in cat]


def linear_pipeline(columns: list[str], *, classification: bool = False) -> Pipeline:
    """Ridge / logistic baseline: impute, scale, OHE low-card, target-encode dest."""
    num = _numerics(columns)
    low, high = _categoricals(columns)
    numeric_pipe = Pipeline(
        [
            ("impute", SimpleImputer(strategy="median")),
            ("scale", StandardScaler()),
        ]
    )
    low_pipe = Pipeline(
        [
            ("impute", SimpleImputer(strategy="most_frequent")),
            ("ohe", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )
    transformers = [("num", numeric_pipe, num), ("low", low_pipe, low)]
    if high:
        transformers.append(
            (
                "high",
                TargetEncoder(target_type="continuous" if not classification else "binary"),
                high,
            )
        )
    pre = ColumnTransformer(transformers, remainder="drop")
    model = (
        LogisticRegression(max_iter=400, class_weight="balanced", random_state=RANDOM_STATE)
        if classification
        else Ridge(alpha=2.0)
    )
    return Pipeline([("pre", pre), ("model", model)])


def hgb_pipeline(columns: list[str], *, classification: bool = False) -> Pipeline:
    """HistGradientBoosting with ordinal-encoded categoricals (native NA on numerics)."""
    num = _numerics(columns)
    cats = [c for c in LOW_CARD_CATEGORICALS + HIGH_CARD_CATEGORICALS if c in columns]
    cat_pipe = Pipeline(
        [
            (
                "ord",
                OrdinalEncoder(
                    handle_unknown="use_encoded_value",
                    unknown_value=-1,
                    encoded_missing_value=-1,
                ),
            )
        ]
    )
    pre = ColumnTransformer(
        [("num", "passthrough", num), ("cat", cat_pipe, cats)],
        remainder="drop",
    )
    cat_idx = list(range(len(num), len(num) + len(cats)))
    if classification:
        model = HistGradientBoostingClassifier(
            max_depth=6,
            max_iter=80,
            learning_rate=0.08,
            l2_regularization=0.1,
            categorical_features=cat_idx,
            random_state=RANDOM_STATE,
        )
    else:
        model = HistGradientBoostingRegressor(
            max_depth=6,
            max_iter=80,
            learning_rate=0.08,
            l2_regularization=0.1,
            categorical_features=cat_idx,
            random_state=RANDOM_STATE,
        )
    return Pipeline([("pre", pre), ("model", model)])


def _regression_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    return {
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "r2": float(r2_score(y_true, y_pred)),
        "baseline_mae": float(mean_absolute_error(y_true, np.full_like(y_true, np.mean(y_true), dtype=float))),
    }


def _classification_metrics(y_true: np.ndarray, proba: np.ndarray) -> dict[str, Any]:
    pred = (proba >= 0.5).astype(int)
    metrics: dict[str, Any] = {
        "accuracy": float(accuracy_score(y_true, pred)),
        "roc_auc": float(roc_auc_score(y_true, proba)),
        "average_precision": float(average_precision_score(y_true, proba)),
        "positive_rate": float(np.mean(y_true)),
    }
    metrics["report"] = classification_report(y_true, pred, output_dict=True, zero_division=0)
    return metrics


def _fit_pair(
    train: pd.DataFrame,
    test: pd.DataFrame,
    *,
    target: str,
    extra: tuple[str, ...] = (),
    classification: bool = False,
) -> dict[str, Any]:
    X_train, y_train = modeling_frame(train, target=target, extra_features=extra)
    X_test, y_test = modeling_frame(test, target=target, extra_features=extra)
    X_test = X_test.reindex(columns=X_train.columns)

    linear = linear_pipeline(list(X_train.columns), classification=classification)
    hgb = hgb_pipeline(list(X_train.columns), classification=classification)
    linear.fit(X_train, y_train)
    if classification:
        weights = compute_sample_weight("balanced", y_train)
        hgb.fit(X_train, y_train, model__sample_weight=weights)
    else:
        hgb.fit(X_train, y_train)

    y_test_np = y_test.to_numpy(dtype=float)
    if classification:
        lin_scores = _classification_metrics(y_test_np, linear.predict_proba(X_test)[:, 1])
        hgb_scores = _classification_metrics(y_test_np, hgb.predict_proba(X_test)[:, 1])
    else:
        lin_scores = _regression_metrics(y_test_np, linear.predict(X_test))
        hgb_scores = _regression_metrics(y_test_np, hgb.predict(X_test))

    return {
        "linear": linear,
        "hgb": hgb,
        "metrics": {"linear": lin_scores, "hgb": hgb_scores, "n_train": int(len(X_train)), "n_test": int(len(X_test))},
        "features": list(X_train.columns),
        "importances": _linear_importances(linear),
    }


def _linear_importances(pipe: Pipeline, top_n: int = 20) -> list[dict[str, Any]]:
    """Absolute coefficients from the linear baseline, aligned to transformed names."""
    pre = pipe.named_steps["pre"]
    model = pipe.named_steps["model"]
    if not hasattr(model, "coef_"):
        return []
    names = pre.get_feature_names_out()
    coef = np.ravel(model.coef_)
    n = min(len(names), len(coef))
    return (
        pd.DataFrame({"feature": names[:n], "importance": np.abs(coef[:n])})
        .sort_values("importance", ascending=False)
        .head(top_n)
        .to_dict(orient="records")
    )


def train_bundle(
    df: pd.DataFrame,
    *,
    sample_size: int | None = 80_000,
    persist: bool = True,
) -> dict[str, Any]:
    """Train dep-delay, arr-delay, and dep-delay classification models."""
    work = df
    train, test = time_split(work)
    if sample_size is not None and len(train) > sample_size:
        train = train.sample(n=sample_size, random_state=RANDOM_STATE)

    dep_reg = _fit_pair(train, test, target="dep_delay")
    arr_reg = _fit_pair(train, test, target="arr_delay")
    dep_clf = _fit_pair(train, test, target="dep_delayed", classification=True)

    bundle = {
        "dep_delay": dep_reg,
        "arr_delay": arr_reg,
        "dep_delayed": dep_clf,
        "threshold": DELAY_THRESHOLD_MIN,
        "train_months": TRAIN_MONTHS,
        "test_months": TEST_MONTHS,
        "sample_size": sample_size,
    }
    metrics = {
        "dep_delay": dep_reg["metrics"],
        "arr_delay": arr_reg["metrics"],
        "dep_delayed": dep_clf["metrics"],
        "threshold": DELAY_THRESHOLD_MIN,
        "train_months": list(TRAIN_MONTHS),
        "test_months": list(TEST_MONTHS),
        "sample_size": sample_size,
    }
    if persist:
        MODELS_DIR.mkdir(parents=True, exist_ok=True)
        joblib.dump(
            {
                "dep_delay_hgb": dep_reg["hgb"],
                "arr_delay_hgb": arr_reg["hgb"],
                "dep_delayed_hgb": dep_clf["hgb"],
                "dep_delay_linear": dep_reg["linear"],
                "arr_delay_linear": arr_reg["linear"],
                "dep_delayed_linear": dep_clf["linear"],
                "dep_delay_features": dep_reg["features"],
                "arr_delay_features": arr_reg["features"],
                "dep_delayed_features": dep_clf["features"],
                "dep_delay_importances": dep_reg["importances"],
                "arr_delay_importances": arr_reg["importances"],
                "dep_delayed_importances": dep_clf["importances"],
                "metrics": metrics,
            },
            BUNDLE_PATH,
        )
        METRICS_PATH.write_text(json.dumps(metrics, indent=2, default=str))
    bundle["metrics"] = metrics
    return bundle


def load_bundle(path: Path | None = None) -> dict[str, Any]:
    path = path or BUNDLE_PATH
    if not path.exists():
        raise FileNotFoundError(f"Model bundle not found at {path}. Run: python -m nycflights_ds train")
    return joblib.load(path)


def typical_row(
    df: pd.DataFrame,
    *,
    origin: str,
    dest: str,
    carrier: str,
    month: int,
    hour: int,
    day: int = 15,
    minute: int = 0,
) -> pd.Series:
    """Median numeric features + requested categoricals for a what-if prediction."""
    slot = df.loc[
        (df["origin"] == origin)
        & (df["dest"] == dest)
        & (df["carrier"] == carrier)
        & (df["month"] == month)
        & (df["hour"] == hour)
    ]
    if slot.empty:
        slot = df.loc[(df["origin"] == origin) & (df["dest"] == dest)]
    if slot.empty:
        slot = df
    values = slot.median(numeric_only=True).to_dict()
    values.update(
        {
            "origin": origin,
            "dest": dest,
            "carrier": carrier,
            "month": month,
            "day": day,
            "hour": hour,
            "minute": minute,
            "season": {
                12: "winter",
                1: "winter",
                2: "winter",
                3: "spring",
                4: "spring",
                5: "spring",
                6: "summer",
                7: "summer",
                8: "summer",
            }.get(int(month), "fall"),
            "part_of_day": "night"
            if hour < 6
            else "morning"
            if hour < 12
            else "afternoon"
            if hour < 18
            else "evening",
            "is_weekend": 1 if pd.Timestamp(year=2013, month=int(month), day=int(day)).weekday() >= 5 else 0,
            "weekday": pd.Timestamp(year=2013, month=int(month), day=int(day)).weekday(),
        }
    )
    hour_sin, hour_cos = np.sin(2 * np.pi * hour / 24), np.cos(2 * np.pi * hour / 24)
    month_sin, month_cos = np.sin(2 * np.pi * month / 12), np.cos(2 * np.pi * month / 12)
    values["hour_sin"] = float(hour_sin)
    values["hour_cos"] = float(hour_cos)
    values["month_sin"] = float(month_sin)
    values["month_cos"] = float(month_cos)
    if "engine_type" in df.columns:
        mode = slot["engine_type"].mode()
        values["engine_type"] = str(mode.iloc[0]) if not mode.empty else "Unknown"
    return pd.Series(values)


def predict_from_row(bundle: dict[str, Any], row: pd.Series) -> dict[str, float]:
    dep_X = pd.DataFrame([row]).reindex(columns=bundle["dep_delay_features"])
    arr_X = pd.DataFrame([row]).reindex(columns=bundle["arr_delay_features"])
    clf_X = pd.DataFrame([row]).reindex(columns=bundle["dep_delayed_features"])
    dep = float(bundle["dep_delay_hgb"].predict(dep_X)[0])
    if "dep_delay" in arr_X.columns and arr_X["dep_delay"].isna().all():
        arr_X["dep_delay"] = dep
    arr = float(bundle["arr_delay_hgb"].predict(arr_X)[0])
    proba = float(bundle["dep_delayed_hgb"].predict_proba(clf_X)[0, 1])
    return {
        "pred_dep_delay": dep,
        "pred_arr_delay": arr,
        "p_dep_delayed": proba,
    }
