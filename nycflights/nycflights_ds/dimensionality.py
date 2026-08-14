"""Dimensionality reduction: correlation pruning, variance, SelectKBest, PCA."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest, f_classif, f_regression, mutual_info_classif
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def numeric_matrix(df: pd.DataFrame, columns: list[str] | None = None) -> tuple[pd.DataFrame, np.ndarray]:
    cols = columns or list(df.select_dtypes(include=[np.number]).columns)
    frame = df[cols].replace([np.inf, -np.inf], np.nan)
    imputed = SimpleImputer(strategy="median").fit_transform(frame)
    return frame, np.asarray(imputed, dtype=float)


def high_correlation_pairs(df: pd.DataFrame, *, threshold: float = 0.85) -> pd.DataFrame:
    """Pairs of numeric features with |Pearson r| above the threshold."""
    num = df.select_dtypes(include=[np.number])
    corr = num.corr(numeric_only=True).to_numpy(dtype=float)
    columns = list(num.columns)
    records: list[dict[str, Any]] = []
    n = len(columns)
    for i in range(n):
        for j in range(i + 1, n):
            r = corr[i, j]
            if np.isfinite(r) and abs(r) >= threshold:
                records.append(
                    {"feature_a": columns[i], "feature_b": columns[j], "pearson_r": float(r)}
                )
    out = pd.DataFrame(records)
    if out.empty:
        return out
    return out.sort_values("pearson_r", key=np.abs, ascending=False).reset_index(drop=True)


def drop_redundant_numerics(df: pd.DataFrame, *, threshold: float = 0.92) -> tuple[pd.DataFrame, list[str]]:
    """Greedy prune: drop the later column in each highly correlated pair."""
    pairs = high_correlation_pairs(df, threshold=threshold)
    drop: list[str] = []
    for _, row in pairs.iterrows():
        b = row["feature_b"]
        if b not in drop and row["feature_a"] not in drop:
            drop.append(str(b))
    kept = df.drop(columns=drop, errors="ignore")
    return kept, drop


def variance_table(df: pd.DataFrame) -> pd.DataFrame:
    num = df.select_dtypes(include=[np.number])
    var = num.var(numeric_only=True)
    return (
        pd.DataFrame({"feature": var.index, "variance": var.to_numpy(dtype=float)})
        .sort_values("variance")
        .reset_index(drop=True)
    )


def fit_pca(df: pd.DataFrame, *, n_components: int = 8) -> dict[str, Any]:
    frame, matrix = numeric_matrix(df)
    n_components = min(n_components, matrix.shape[1], matrix.shape[0])
    pipe = Pipeline(
        [
            ("scale", StandardScaler()),
            ("pca", PCA(n_components=n_components, random_state=42)),
        ]
    )
    transformed = pipe.fit_transform(matrix)
    pca: PCA = pipe.named_steps["pca"]
    loadings = pd.DataFrame(
        pca.components_.T,
        index=frame.columns,
        columns=[f"PC{i + 1}" for i in range(n_components)],
    )
    return {
        "pipeline": pipe,
        "explained_variance_ratio": pca.explained_variance_ratio_.tolist(),
        "cumulative_variance": np.cumsum(pca.explained_variance_ratio_).tolist(),
        "loadings": loadings,
        "transformed": transformed,
        "feature_names": list(frame.columns),
    }


def select_k_best(
    X: pd.DataFrame,
    y: pd.Series,
    *,
    k: int = 12,
    problem: str = "regression",
) -> dict[str, Any]:
    frame, matrix = numeric_matrix(X)
    k = min(k, matrix.shape[1])
    if problem == "classification":
        score_func = f_classif
    else:
        score_func = f_regression
    selector = SelectKBest(score_func=score_func, k=k)
    selector.fit(matrix, y.to_numpy())
    scores = pd.DataFrame(
        {
            "feature": frame.columns,
            "score": selector.scores_,
            "p_value": selector.pvalues_,
            "selected": selector.get_support(),
        }
    ).sort_values("score", ascending=False)
    return {"selector": selector, "scores": scores.reset_index(drop=True)}


def mutual_info_ranks(X: pd.DataFrame, y: pd.Series, *, k: int = 12) -> pd.DataFrame:
    frame, matrix = numeric_matrix(X)
    y_bin = (y.to_numpy() >= 0.5).astype(int) if y.nunique() <= 5 else (y.to_numpy() >= 15).astype(int)
    mi = mutual_info_classif(matrix, y_bin, random_state=42)
    out = pd.DataFrame({"feature": frame.columns, "mutual_info": mi})
    return out.sort_values("mutual_info", ascending=False).head(k).reset_index(drop=True)
