from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def _weighted_mean(x: np.ndarray, w: np.ndarray) -> float:
    return float(np.sum(w * x) / np.sum(w))


def _smd_binary(x: np.ndarray, t: np.ndarray, w: np.ndarray | None = None) -> float:
    x = np.asarray(x, dtype=float)
    t = np.asarray(t, dtype=int)
    if w is None:
        w = np.ones_like(x, dtype=float)
    m1 = _weighted_mean(x[t == 1], w[t == 1])
    m0 = _weighted_mean(x[t == 0], w[t == 0])
    v1 = _weighted_mean((x[t == 1] - m1) ** 2, w[t == 1])
    v0 = _weighted_mean((x[t == 0] - m0) ** 2, w[t == 0])
    denom = np.sqrt((v1 + v0) / 2)
    return float((m1 - m0) / denom) if denom > 0 else 0.0


def propensity_att_sensitivity(
    df: pd.DataFrame,
    *,
    treatment_col: str,
    outcome_col: str,
    categorical_covariates: list[str],
    numeric_covariates: list[str] | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, float | int | str]]:
    """Observed-covariate ATT weighting sensitivity analysis.

    This analysis targets the average treatment effect among students observed
    with use beyond the PPA threshold. It addresses only *observed* imbalance;
    it does not identify a causal effect under unmeasured motivation/need.
    """
    numeric_covariates = numeric_covariates or []
    covariates = categorical_covariates + numeric_covariates
    cols = [treatment_col, outcome_col] + covariates
    d = df[cols].dropna(subset=[treatment_col, outcome_col]).copy()

    if not covariates:
        return pd.DataFrame(), pd.DataFrame(), {"status": "skipped_no_covariates"}

    t = d[treatment_col].astype(int).to_numpy()
    if len(np.unique(t)) < 2:
        return pd.DataFrame(), pd.DataFrame(), {"status": "skipped_single_treatment_level"}

    transformers = []
    if categorical_covariates:
        cat_pipe = Pipeline([
            ("impute", SimpleImputer(strategy="most_frequent")),
            ("encode", OneHotEncoder(handle_unknown="ignore")),
        ])
        transformers.append(("cat", cat_pipe, categorical_covariates))
    if numeric_covariates:
        num_pipe = Pipeline([
            ("impute", SimpleImputer(strategy="median")),
            ("scale", StandardScaler()),
        ])
        transformers.append(("num", num_pipe, numeric_covariates))

    pre = ColumnTransformer(transformers)
    model = Pipeline([
        ("pre", pre),
        ("logit", LogisticRegression(max_iter=3000, solver="lbfgs")),
    ])
    model.fit(d[covariates], t)
    ps = model.predict_proba(d[covariates])[:, 1]
    ps = np.clip(ps, 0.02, 0.98)

    # ATT weights: treated=1; controls=e/(1-e).
    w = np.where(t == 1, 1.0, ps / (1.0 - ps))
    y = d[outcome_col].to_numpy(float)
    effect = _weighted_mean(y[t == 1], w[t == 1]) - _weighted_mean(y[t == 0], w[t == 0])

    d_out = d[[treatment_col, outcome_col]].copy()
    d_out["propensity"] = ps
    d_out["att_weight"] = w

    fitted_pre = model.named_steps["pre"]
    X = fitted_pre.transform(d[covariates])
    if hasattr(X, "toarray"):
        X = X.toarray()
    names = fitted_pre.get_feature_names_out()
    balance = []
    for j, name in enumerate(names):
        x = np.asarray(X[:, j]).ravel()
        balance.append({
            "covariate_level": str(name),
            "smd_unweighted": _smd_binary(x, t),
            "smd_att_weighted": _smd_binary(x, t, w),
        })
    balance_df = pd.DataFrame(balance)

    ess_control = float((w[t == 0].sum() ** 2) / np.sum(w[t == 0] ** 2)) if np.any(t == 0) else np.nan
    meta = {
        "status": "ok",
        "n": int(len(d)),
        "n_treated": int(t.sum()),
        "n_control": int((1 - t).sum()),
        "att_weighted_effect_z": float(effect),
        "propensity_min": float(ps.min()),
        "propensity_max": float(ps.max()),
        "effective_control_n_att": ess_control,
        "max_abs_smd_unweighted": float(balance_df["smd_unweighted"].abs().max()) if len(balance_df) else np.nan,
        "max_abs_smd_att_weighted": float(balance_df["smd_att_weighted"].abs().max()) if len(balance_df) else np.nan,
        "categorical_covariates": categorical_covariates,
        "numeric_covariates": numeric_covariates,
    }
    return d_out, balance_df, meta
